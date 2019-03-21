
import zmq
import random
import sys
import time

class client_(object):
    def __init__(self, config):
        self.identity = config.id
        self.c_socket()
        
    def c_socket(self):
        self.context = zmq.Context()
        
        # Multicasting
        self.client_receiver = self.context.socket(zmq.SUB)
        self.client_receiver.connect("tcp://localhost:5560")
        self.client_receiver.setsockopt(zmq.SUBSCRIBE, b'')
        
        self.client_sender = self.context.socket(zmq.PUB)
        self.client_sender.connect("tcp://localhost:5559")
        
        # unordered messaging
        self.client_deal = self.context.socket(zmq.DEALER)
        self.client_deal.setsockopt(zmq.IDENTITY, (self.identity).encode())
        self.client_deal.connect("tcp://localhost:5562")
        
        # synchronization with publisher
        self.syncclient = self.context.socket(zmq.REQ)
        self.syncclient.connect('tcp://localhost:5561')
        
        # sending a synchronization request
        self.syncclient.send(b'')
        
        # waiting for synchronization reply
        self.syncclient.recv()
        while True:
            self.msg = self.client_receiver.recv()
            if (self.msg).decode("ascii") == "start":  # All clients are connected, Start!
                break
        
    def send_tom(self, msg, seq_num = None):
        print("sending ", msg.decode("ascii"), " from ", self.identity,  " to all!")
        if seq_num != None:
            self.client_sender.send_multipart([self.identity.encode(), seq_num ,msg])  # to be able to send sequence number
        else:                                                                           # using sequencer
            self.client_sender.send_multipart([self.identity.encode(), b'', msg])
            
    def recv_tom(self):
        sender_id, seq_num ,msg = self.client_receiver.recv_multipart()
        print ("Received ", msg.decode("ascii"), " from ", sender_id.decode("ascii"), "!")
        if seq_num.decode("ascii") == "":
            return [msg]
        else:
            return [msg, seq_num]   # to be able to receive sequence number sent by sequencer
            
    def send_uno(self, receiver_id, msg):
        print("Sending ", msg.decode("ascii"), " to ", receiver_id.decode("ascii"), "!" )
        self.client_deal.send_multipart([b'', receiver_id, msg])
            
    def recv_uno(self):
        empty, sender_id, msg = self.client_deal.recv_multipart()
        print ("Received ", msg.decode("ascii"), " from ", sender_id.decode("ascii") , "!")
        return msg

            
