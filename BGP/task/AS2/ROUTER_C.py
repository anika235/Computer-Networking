import socket
import threading
import pickle
from queue import PriorityQueue
import time
import random

IP = "localhost"
PORT = 2237

IP1 = ""
ADDR = (IP1, PORT)
SIZE = 1024
FORMAT = "utf-8"
ROUTER_NAME = "C-AS2"
GATEWAY_NAME = "AS2"
TIMEOUT = 10;

adj={}
dist={}
parent={}
PORT_NAME={}            
NAME_ADDR={} # => ADDR[(hostname,router)] = (IP,PORT)
chk_time = {}

def make_top():
    file = open("NAME.txt")
    content = file.readlines()
    
    for line in content:
        data = line.split()
        PORT_NAME[data[0]] = int(data[1])
        NAME_ADDR[data[0]] = ("localhost",int(data[1]))
        if(data[0]==ROUTER_NAME):
            PORT = int(data[1])
    
    file.close()
    file = open("router_path.txt")
    content = file.readlines()
    for line in content :
        word = line.split()
        if word[0] not in adj:
            adj[word[0]]={}
            
        if word[1] not in adj:
            adj[word[1]]={}
        adj[word[0]][word[1]] = int(word[2])
        adj[word[1]][word[0]] = int(word[2])    
    file.close()


def recv_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    data = conn.recv(SIZE)
    if len(data) == 0 : 
        return
    data = pickle.loads(data)
    
    AS_PATH = data["AS_PATH"]
    if AS_PATH != "Sorry, no path to the destination":
        AS_PATH = AS_PATH.split()
    
        print("-------------------------------")
        
        print("the path is :")
        for path in AS_PATH:
            print(path)
        
        print("-------------------------------")
    else:
        print("-------------------------------")
        print("Sorry, no path to the destination")
        print("-------------------------------")
    
    conn.close()
    chk_time[AS_PATH[0]] = False

def send_msg(inp):
    
    #making a payload where id = (IP , PORT) and ttl = 5 and the next info is the information about neighborings nodes
    if inp in adj[ROUTER_NAME]:
        print("the path is :")
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("localhost",PORT_NAME[inp]))
            print("-------------------------------")
            print(ROUTER_NAME)
            print(inp)
            print("-------------------------------")
            client.close()
        except:
            print("-------------------------------")
            print("Sorry, no path to the destination")
            print("-------------------------------")
        return
        
    pickle_payload={"HOST" : ROUTER_NAME , 
                    "ORIGIN": "IGP" , 
                    "AS_PATH" : ROUTER_NAME , 
                    "NEXT_HOP" : inp , 
                    "METRIC" : adj[ROUTER_NAME][GATEWAY_NAME]}
    payload = pickle.dumps(pickle_payload)
        
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("localhost",PORT_NAME[GATEWAY_NAME]))
        client.sendall(payload)
    except:
        print("The connection to AS1 failed")
    client.close()

    strt_time = time.time()
    chk_time[inp] = True
    while chk_time[inp]:
        if time.time() - strt_time > TIMEOUT:
            print("-------------------------------")
            print("Sorry, no path to the destination")
            print("-------------------------------")
            break
    

def handle_recv():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=recv_msg, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def handle_send(inp):
    thread1 = threading.Thread(send_msg(inp))
    thread1.start()


def main():
    #creating the adjacency list from the file
    make_top()
    
    #creating the a new thread for receiving messages
    thread = threading.Thread(target=handle_recv, args=())
    thread.start()
    time.sleep(.2)
    while True:
        inp = input("Enter the address you want to look for : ")
        if inp == "EXIT":
            break
        inp = inp.split()
        dst = inp[1]+"-"+inp[4]
        threadsend = threading.Thread(handle_send(dst))
        threadsend.start()
            

if __name__=="__main__":
    main()