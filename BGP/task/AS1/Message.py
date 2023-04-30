import socket
import time
import threading

TIMEOUT = 10

class message:
    def __init__(self, ip, port):
        self.PORT = port
        self.IP = ip 
        self.status = "OK"
        thread = threading.Thread(target=self.open)
        thread.start()
        
    def notification(self):
        return "Error"
    
    def open(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.IP,self.PORT))
            client.close()
            print(f"Connected to the AS with IP: {self.IP} and PORT: {self.PORT} and it is open.")
            thread = threading.Thread(target = self.keepalive)
            thread.start()
            return
        except:
            self.status = self.notification()
            print(f"The connection with AS with IP: {self.IP} and PORT: {self.PORT}  can not be opened.")
        
    def keepalive(self):
        starting_time = time.time()
        while(True):
            if(time.time()-starting_time>TIMEOUT):
                starting_time = time.time()
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    client.connect((self.IP,self.PORT))
                    client.close()
                    self.status = "OK"
                except:
                    print(f"The connection with AS with IP: {self.IP} and PORT: {self.PORT}  is closed.")
                    self.status = self.notification()
                    break
                
    def Update(self , payload):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.IP,self.PORT))
            client.sendall(payload)
            client.close()
        except:
            self.status = self.notification()
            