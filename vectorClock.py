import socket
import threading
import json
import sys 

class VectorClock:
    def __init__(self, num):
        self.clock = [0] * num
    
    def increment(self, pid):
        self.clock[pid] += 1
    
    def update(self, otherClock):
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], otherClock[i])
    
    def __str__(self):
        return str(self.clock)

def  listenerThread(pid, vectorClock, UDPsocket):
    while True:
        data, _ = UDPsocket.recvfrom(1024)
        msg = json.loads(data.decode('utf-8'))

        senderId = msg['pid']
        senderClock = msg['clock']
        vectorClock.update(senderClock)
        
        #print(f"Process {pid} received a message from process {senderId}")
        #print(f"Vector clock before: {vectorClock}")
        #vectorClock.update(senderClock)
        #print(f"Vector clock after: {vectorClock}")

        print(f"Process {pid} received a message from process {senderId}")
        print(f"Vector clock before: {senderClock}")
        print(f"Vecotr clock after: {vectorClock}")

        #senderId = msg['pid']
        #senderClock = msg['clock']
        #vectorClock.update(senderClock.copy())

        #print(f"Process {pid} received a message from process {senderId}")
        #print(f"Vector clock before: {senderClock}")
        #print(f"Vector clock after: {vectorClock}")

def senderThread(pid, vectorClock, UDPsocket, processList):
    while True:
        try:
            #ask for user input for unicast or broadcast messaging: unicast ask user for target PID, broadcast sends a message to all other processes minus itself 
            msgType = input("Enter 'u' for unicast or 'b' for broadcast: ")
            if msgType == 'u':
                targetId = int(input("Enter the target PID: "))
                if targetId >= len(processList):
                    print("Invalid PID")
                    continue
                vectorClock.increment(pid)
                msg = {'pid': pid, 'clock': vectorClock.clock}
                UDPsocket.sendto(json.dumps(msg).encode('utf-8'), processList[targetId])
                print(f"Process {pid} sent a unicast message to process {targetId}")
            elif msgType == 'b':
                vectorClock.increment(pid)
                msg = {'pid': pid, 'clock': vectorClock.clock}
                for i, address in enumerate(processList):
                    if i == pid:
                        continue
                    UDPsocket.sendto(json.dumps(msg).encode('utf-8'), address)
                    print(f"Process {pid} sent a broadcast message to process {i}")
        except EOFError as er:
            print(er)

def runProcesses(pid, num, port):
    try:
        #initializes clock
        vectorClock = VectorClock(num)

        #creates and binds the socket to port 
        UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPsocket.bind(('localhost', port + pid))

        #list of processes location
        processList = []
        for i in range(num):
            loc = ('localhost', port + i)
            processList.append(loc)
        
        #creates listner and sender threads
        listener = threading.Thread(target = listenerThread, args = (pid, vectorClock, UDPsocket))
        sender = threading.Thread(target = senderThread, args = (pid, vectorClock, UDPsocket, processList))

        #starts listener and sender 
        listener.start()
        sender.start()
        listener.join()
        sender.join()
    except EOFError as err:
        print(err)

if __name__ == "__main__":
    #three inputs for the command line PID, port number, total number of processes
    pid = int(sys.argv[1])
    port = int(sys.argv[2])
    num = int(sys.argv[3])
    print(f"Running process {pid}")
    runProcesses(pid, num, port)