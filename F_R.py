
import zmq 
import threading
from config import get_config

class brokers(object):
    def __init__(self, config):
        self.SUBSCRIBERS_EXPECTED = config.nc
        
        
    def forwarder_tom(self):
        try:
            self.context = zmq.Context() # Socket facing clients
            self.frontend = self.context.socket(zmq.SUB)
            self.frontend.bind("tcp://*:5559")
            self.frontend.setsockopt(zmq.SUBSCRIBE, b"")
            # Socket facing servics
            self.backend = self.context.socket(zmq.PUB)
            self.backend.bind("tcp://*:5560")
    

            # Socket to receive signals
            self.syncservice = self.context.socket(zmq.REP)
            self.syncservice.bind('tcp://*:5561')

            # Get synchronization from subscribers
            subscribers = 0
            while subscribers < self.SUBSCRIBERS_EXPECTED:
                # wait for synchronization request
                msg = self.syncservice.recv()
                # send synchronization reply
                self.syncservice.send(b'')
                subscribers += 1
                print("+1 subscriber (%i/%i)" % (subscribers, self.SUBSCRIBERS_EXPECTED))
            self.backend.send("start".encode())  

            zmq.proxy(self.frontend, self.backend)

        except e:
            print(e)
            print("bringing down zmq device") 
        finally:
            pass
            self.frontend.close()
            self.backend.close()
            self.context.term()
        
        
    def router_uno(self):
        self.context = zmq.Context()
        self.router = self.context.socket(zmq.ROUTER)
        self.router.bind("tcp://*:5562")

        # Initialize poll set
        self.poller = zmq.Poller()
        self.poller.register(self.router, zmq.POLLIN)

        # Switch messages between sockets
        while True:
            self.socks = dict(self.poller.poll())

            if self.socks.get(self.router) == zmq.POLLIN:
                sender_id, empty, receiver_id, message = self.router.recv_multipart()
                print("Received ", message.decode("ascii"), " from ", sender_id.decode("ascii"), "!")
                print( "Forwarding to ", receiver_id.decode("ascii"))
                self.router.send_multipart([receiver_id, b'',sender_id, message])
        

if __name__ == "__main__":
    
    config, _ = get_config()
    
    b = brokers(config)
    threading.Thread(target = b.forwarder_tom , args = ()).start()
    threading.Thread(target = b.router_uno , args = ()).start()
