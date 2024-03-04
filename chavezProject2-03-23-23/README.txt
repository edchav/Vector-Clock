1. Run the 'vectorClock.py' file in a terminal with the command python vectorClock.py pid, port number, total number of processers.

2. repeat the process in other terminals using the corresponding pid, the same port number and the same total number of processers as in the first terminal.

3. Here is a following example of the correct commands:
	Terminal 1: python vectorClock.py 0 3000 3
	Terminal 2: python vectorClock.py 1 3000 3
	Terminal 3: python vectorClock.py 2 3000 3

4. Lastly after running those commands you should see 'Running proccess 0' and 'Enter 'u' for unicast or 'b' for broadcast: ' in the first terminal and the same in the other termianls with their respective pid

5. Enter u or b for unicast or broadcast in any of the following terminals to see the results
