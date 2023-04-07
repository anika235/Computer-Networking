import socket
import threading
from queue import PriorityQueue
import time
import random

IP = "localhost"
PORT = 1236

IP1 = ""
ADDR = (IP1, PORT)
SIZE = 1024
FORMAT = "utf-8"
TIMEOUT = 30
INF = 10000000000000000

adj={}
dist={}
parent={}
def UPDATE():
    for x in adj: # x == (ipx,portx)
        for y in adj[x]:
            for v in adj:
                if v not in adj[x]:
                    adj[x][v]=INF
                    adj[v][x]=INF
                if y not in adj[v]:
                    adj[v][y]=INF
                    adj[y][v]=INF

                if adj[x][y]>adj[x][v]+adj[v][y]:
                    adj[x][y] = min(adj[x][y],adj[x][v]+adj[v][y])  
                    parent[y] = v;              



#printing the distances and the parent of each node
def print_dist():
    for v in adj[(IP,PORT)]:
        print(f"The distance from this device to ({v[0]},{v[1]}) is  = {adj[(IP,PORT)][v]}")
        print(f"The parent of the node {v} is = {parent[v]}")


def make_top():
    file = open("Path.txt")
    content = file.readlines()
    for line in content :
        word = line.split()
        if word[0]==IP and PORT == int(word[1]): 
            
            #adj[(U_IP,U_PORT)].append(((V_IP,V_PORT),weight))
            if((word[0],int(word[1])) not in adj):
                adj[(word[0],int(word[1]))]={}
                
            adj[(word[0],int(word[1]))][(word[2],int(word[3]))] = int(word[4])

            if (word[2],int(word[3])) not in adj:
                adj[(word[2],int(word[3]))]={}
            adj[(word[2],int(word[3]))][(word[0],int(word[1]))] = int(word[4])


            
    file.close()


def recv_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    data = conn.recv(SIZE).decode(FORMAT)
    data = data.split()
    print(f"The new incoming message is : {data}")
        
    got_IP = data[0]
    got_PORT = int(data[1])
    ttl = int(data[2])
    
    #extracting the information of the incoming message
    
    for i in range(3,len(data),3):
        tmpIP = data[i]
        tmpPORT = int(data[i+1])
        tmpWeight = int(data[i+2])
        

        if (got_IP,got_PORT) not in adj:
            adj[(got_IP,got_PORT)]={}
        if (tmpIP,tmpPORT) not in adj:
            adj[(tmpIP,tmpPORT)] = {}

        adj[(got_IP,got_PORT)][(tmpIP,tmpPORT)] = tmpWeight
        adj[(tmpIP,tmpPORT)][(got_IP,got_PORT)] = tmpWeight
        if tmpWeight == INF:
            for xy in adj[(tmpIP,tmpPORT)]:
                adj[(tmpIP,tmpPORT)][xy]=INF
                adj[xy][(tmpIP,tmpPORT)]=INF
        
    
    print(f"The new adjacency list is :")  
    for u in adj:
        print(f'For {u} : {adj[u]}')
    UPDATE()
    print(f"The new distances are :")
    print_dist()
            
    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def send_msg():
    
    #making a payload where id = (IP , PORT) and ttl = 5 and the next info is the information about neighborings nodes
    
    payload=""
    for v in adj[(IP,PORT)]:
        if v != (IP,PORT):
            payload+=v[0]+" "+str(v[1])+" "+str(adj[(IP,PORT)][v])+" "
        
    payload = IP+" "+str(PORT)+" "+str(5)+" "+payload
        
    for v in adj[(IP,PORT)]:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((v[0],v[1]))
            client.send(payload.encode(FORMAT))
            client.close()
        except:
            if(adj[(IP,PORT)][v]!=INF):
                print(f'Error in connecting to the server, May be the server with IP {v[0][1]} is down...')
            if v not in adj:
                adj[v] = {}
            for x in adj:
                for y in adj[x]:
                    if x==v or y==v:
                        adj[x][y]=INF
                        adj[y][x]=INF
            print(f'{v} should be updated')
            client.close()
    

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

def handle_send():
    thread1 = threading.Thread(target=send_msg,args=())
    thread1.start()


def main():
    #creating the adjacency list from the file
    make_top()
    
    #creating the a new thread for receiving messages
    thread = threading.Thread(target=handle_recv, args=())
    thread.start()
    
    
    starting_time = time.time()
    
    #whenever the timeout is reached, a random edge is chosen and its weight is changed
    while True:
        if(time.time()-starting_time>TIMEOUT):
            starting_time = time.time()
            #sending the new Graph to the network
            threadsend = threading.Thread(target=handle_send, args=())
            threadsend.start()
            
            # changing the weight of the edge
            cntt = 0
            
            for v in adj[(IP,PORT)]:
                if adj[(IP,PORT)][v]!=INF and v != (IP,PORT):
                    cntt+=1
            x = random.randint(0,1000)%cntt

            for v in adj[(IP,PORT)]:
                if adj[(IP,PORT)][v]!=INF and v != (IP,PORT):
                    if x==0:
                        cng = random.randint(1,50)
                        adj[(IP,PORT)][v] = cng
                        adj[v][(IP,PORT)] = cng
                    x-=1
            

if __name__=="__main__":
    main()