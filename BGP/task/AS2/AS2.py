import socket
import threading
import pickle
from Message import message
from queue import PriorityQueue
import time
import random

IP = "localhost"
PORT = 2234

IP1 = ""
ADDR = (IP1, PORT)
SIZE = 1024
FORMAT = "utf-8"
TIMEOUT = 30
INF = 10000000000000000
ROUTER_NAME = "AS2"

adj = {}
dist = {}
parent = {}
PORT_NAME = {}
NAME_ADDR = {} # => NAME_ADDR[(hostname,router)] = (IP,PORT)

MSG_PATH_LIST = {}

BGP_CONN = {}

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


def Update_List(data):
    if data["HOST"] in MSG_PATH_LIST:
        if MSG_PATH_LIST[data["HOST"]]["METRIC"] > data["METRIC"]:
            MSG_PATH_LIST[data["HOST"]]=data
            return True
        
        elif MSG_PATH_LIST[data["HOST"]]["METRIC"] == data["METRIC"]:
            tmp1 = MSG_PATH_LIST[data["HOST"]]["AS_PATH"].split()
            tmp2 = data["AS_PATH"].split()
            if len(tmp1) > len(tmp2):
                MSG_PATH_LIST[data["HOST"]]=data
                return True
    else:
        MSG_PATH_LIST[data["HOST"]]=data
        return True
    
    return False

def recv_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    data = conn.recv(SIZE)
    if len(data) == 0 : 
        return
    data = pickle.loads(data)
    if data["ORIGIN"]=="IGP":
        MSG_PATH_LIST[data["HOST"]]=data
        #sending the message to the ASes
        for v in adj[ROUTER_NAME]:
            if (v=="AS2" or v=="AS3" or v=="AS4" or v=="AS1") and v != ROUTER_NAME:
                pickle_payload = {
                    "HOST"      : data["HOST"],
                    "ORIGIN"    : "EGP",
                    "AS_PATH"   : ROUTER_NAME + " " + data["AS_PATH"],
                    "NEXT_HOP"  : data["NEXT_HOP"],
                    "METRIC"    : data["METRIC"] + adj[ROUTER_NAME][v],
                }
                payload = pickle.dumps(pickle_payload)
                
                if v not in BGP_CONN:
                    print(NAME_ADDR[v])
                    tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                    BGP_CONN[v] = tmp
                
                if BGP_CONN[v].status=="OK":
                    BGP_CONN[v].Update(payload)
                else:
                    tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                    BGP_CONN[v] = tmp
                    BGP_CONN[v].Update(payload)
                
    else:
        if data["NEXT_HOP"] in adj[ROUTER_NAME]:
            if data["HOST"] == data["NEXT_HOP"]:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((NAME_ADDR[data["HOST"]][0],NAME_ADDR[data["HOST"]][1]))
                data["ORIGIN"] = "IGP"
                client.send(pickle.dumps(data))
                client.close()
            else:
                if Update_List(data):
                    pickle_payload = MSG_PATH_LIST[data["HOST"]]
                    pickle_payload["ORIGIN"] = "EGP"
                    
                    
                    #check if the destination router is on or off
                    tmp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        tmp_client.connect((NAME_ADDR[pickle_payload["NEXT_HOP"]][0],NAME_ADDR[pickle_payload["NEXT_HOP"]][1]))
                        pickle_payload["AS_PATH"] = pickle_payload["NEXT_HOP"] + " " +ROUTER_NAME + " " + pickle_payload["AS_PATH"]
                        tmp_client.close()
                    except:
                        pickle_payload["AS_PATH"] = "Sorry, no path to the destination"
                        tmp_client.close()
                        
                    pickle_payload["NEXT_HOP"] = data["HOST"]
                    
                    for v in adj[ROUTER_NAME]: # v is the name of the neighbor of AS1 like AS2 etc
                        if (v== "AS1" or v=="AS2" or v=="AS3" or v=="AS4") and v != ROUTER_NAME:
                            pickle_payload1 = pickle_payload
                            pickle_payload1["METRIC"] = pickle_payload["METRIC"] + adj[ROUTER_NAME][v]
                            payload = pickle.dumps(pickle_payload1)
                            
                            if v not in BGP_CONN:
                                tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                                BGP_CONN[v] = tmp
                            
                            if BGP_CONN[v].status=="OK":
                                BGP_CONN[v].Update(payload)
                            else:
                                tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                                BGP_CONN[v] = tmp
                                BGP_CONN[v].Update(payload)
                            
        else:
            if Update_List(data):
                pickle_payload = MSG_PATH_LIST[data["HOST"]]
                pickle_payload["ORIGIN"] = "EGP"
                pickle_payload["AS_PATH"] = ROUTER_NAME + " " + pickle_payload["AS_PATH"]
                
                for v in adj[ROUTER_NAME]:
                    if (v=="AS1" or v=="AS2" or v=="AS3" or v=="AS4") and v != ROUTER_NAME:
                        pickle_payload1 = pickle_payload
                        pickle_payload1["METRIC"] = pickle_payload["METRIC"] + adj[ROUTER_NAME][v]
                        payload = pickle.dumps(pickle_payload1)
                        
                        if v not in BGP_CONN:
                            tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                            BGP_CONN[v] = tmp
                        
                        if BGP_CONN[v].status=="OK":
                            BGP_CONN[v].Update(payload)
                        else:
                            tmp = message(NAME_ADDR[v][0],NAME_ADDR[v][1])
                            BGP_CONN[v] = tmp
                            BGP_CONN[v].Update(payload)
        
    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()
    
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


def main():
    #creating the adjacency list from the file
    make_top()
    thread_recv = threading.Thread(target=handle_recv())
    thread_recv.start()        

if __name__=="__main__":
    main()