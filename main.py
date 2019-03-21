
from config import get_config
from client import client_
from queue import Queue
import threading
import time
import csv
import numpy as np


if __name__ == "__main__":

    config, _ = get_config()
    c = client_(config)
    
    if config.id == "sequencer":
        g_seq_num = 0  # global sequence number (initial value set to 0)
        while True:
            msg = c.recv_tom()
            if len(msg) == 1:
                g_seq_num += 1
                c.send_tom(msg[0], str(g_seq_num).encode())
    
    
    else:
        q1 = Queue(100)  # queue for storing unorderd messages
        q2 = Queue(100)  # quese for storing totally ordered messages

        def rcv1(q):
            while True:
                msg = c.recv_uno()
                q.put(msg)

        def rcv2(q):
            while True:
                msg = c.recv_tom()
                q.put(msg)

        def send_commands():
            with open(config.com, 'r') as f:   # opening command files
                reader = csv.reader(f)
                cmd = list(reader)
                for item in cmd:
                    if item[0] == "Multicast":  # checking to see if it is a multicast message
                        if item[1] == config.id:
                            c.send_tom((config.id + "###" +item[2]).encode())
                    elif item[0] == "sleep":  
                        time.sleep(np.float(item[1]))
                    else:                              
                        if item[0] == config.id:
                            c.send_uno(item[1].encode(), (config.id + "###" + item[2]).encode())

    
        def tom_uno():
            cmd_list = []
            seq_list = []
            l_seq_num = 0    # local sequence number (initial value set to 0)

            with open(config.o + "/test_result_" + config.id +"_tom.txt", 'wb', 0) as g, \
                         open(config.o + "/test_result_" + config.id +"_uno.txt", 'wb', 0) as h:
                while True:

                    if not q1.empty():     # checking for unorderd messages
                        #print(item1)
                        item1 = q1.get()
                        h.write((item1.decode("ascii") + "\n").encode()) # write received uorderd messages in the file

                    if not q2.empty(): # checking for totally orderd messages
                        #print(item2)
                        item2 = q2.get() 
                        if len(item2) == 1:         # checking whether it is from a client or the sequencer
                            cmd_list.append(item2)
                        else:
                            seq_list.append(item2)
                    if len(seq_list) > 0:         # checking to see if there is any uprocessed message from sequencer
                        if int(seq_list[0][1].decode("ascii")) == (l_seq_num + 1):
                            if [seq_list[0][0]] in cmd_list:
                                idx = cmd_list.index([seq_list[0][0]])
                                g.write((cmd_list[idx][0].decode("ascii") + "\n").encode()) # delivering the received 
                                del cmd_list[idx]                                           # message to the application
                                del seq_list[0]
                                l_seq_num += 1           
                    time.sleep(0.01)           # For preventing from high cpu usage
            
            
            
        # threads for receiving messages and sending commands                    
        threading.Thread(target = rcv1  , args = (q1,)).start()
        threading.Thread(target = rcv2 , args = (q2,)).start()
        threading.Thread(target = send_commands , args = ()).start()
        threading.Thread(target = tom_uno, args = ()).start()   
