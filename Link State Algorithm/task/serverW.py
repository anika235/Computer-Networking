import socket
import threading
from queue import PriorityQueue
import time
import random

IP = "localhost"
PORT = 1237

IP1 = ""
ADDR = (IP1, PORT)
SIZE = 1024
FORMAT = "utf-8"
TIMEOUT = 30

adj={}
dist={}
parent={}
def Dijkstra():
    dist.clear()
    parent.clear()
    dist[(IP,PORT)]=0
    Q = PriorityQueue()
    Q.put((dist[(IP,PORT)],(IP,PORT)))
    while(Q.empty()==False):
        d,u = Q.get()
        for v in adj[u]:           # v is a tuple of ((IP,PORT),weight)
            if  v[0] not in dist or dist[v[0]]>v[1]+d:
                parent[v[0]] = u
                dist[v[0]] = v[1]+dist[u]
                Q.put((dist[v[0]],v[0]))

#printing the distances and the parent of each node
def print_dist():
    for v in dist:
        if v==(IP,PORT):
            continue
        print(f"The distance from this device to ({v[0]},{v[1]}) is  = {dist[v]}")
        print(f"The parent of the node {v} is = {parent[v]}")


def make_top():
    file = open("Path.txt")
    content = file.readlines()
    for line in content :
        word = line.split()
        if word[0]==IP and PORT == int(word[1]): 
            
            #adj[(U_IP,U_PORT)].append(((V_IP,V_PORT),weight))
            if((word[0],int(word[1])) not in adj):
                adj[(word[0],int(word[1]))]=[]
                
            adj[(word[0],int(word[1]))].append(((word[2],int(word[3])),int(word[4])))
            
    file.close()


def recv_msg(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    data = conn.recv(SIZE).decode(FORMAT)
    data = data.split()
    print(f"The new incoming message is : {data}")
    
    msg=""
    
    got_IP = data[0]
    got_PORT = int(data[1])
    ttl = int(data[2])
    
    #extracting the information of the incoming message
    
    for i in range(3,len(data),3):
        tmpIP = data[i]
        tmpPORT = int(data[i+1])
        tmpWeight = int(data[i+2])
        msg+=tmpIP+" "+str(tmpPORT)+" "+str(tmpWeight)+" "
        
        if (got_IP,got_PORT) in adj:
            for v in adj[(got_IP,got_PORT)]: #v is a tuple of ((IP,PORT),weight)
                if(v[0]==(tmpIP,tmpPORT)):
                    adj[(got_IP,got_PORT)].remove(v)
                    break
        else:
            adj[(got_IP,got_PORT)]=[]
            
        adj[(got_IP,got_PORT)].append(((tmpIP,tmpPORT),tmpWeight))
        
        if (tmpIP,tmpPORT) in adj:
            for v in adj[(tmpIP,tmpPORT)]: #v is a tuple of ((IP,PORT),weight)
                if(v[0]==(got_IP,got_PORT)):
                    adj[(tmpIP,tmpPORT)].remove(v)
                    break
        else:
            adj[(tmpIP,tmpPORT)]=[]
        adj[(tmpIP,tmpPORT)].append(((got_IP,got_PORT),tmpWeight)) 
    
    print(f"The new adjacency list is : {adj}")  
    Dijkstra()
    print(f"The new distances are :")
    print_dist()
    if(ttl-1>0):
        #forwarding the message to its neighbors if the ttl value is greater than 0
        ttl-=1
        msg = got_IP+" "+str(got_PORT)+" "+str(ttl)+" "+msg
        for v in adj[(IP,PORT)]:
            if v[0]!=(got_IP,got_PORT):
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    client.connect((v[0][0],v[0][1]))
                    client.send(msg.encode(FORMAT))
                    client.close()
                except:
                    print("Error in connecting to the server")
                    client.close()
            
    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def send_msg():
    
    #making a payload where id = (IP , PORT) and ttl = 5 and the next info is the information about neighborings nodes
    
    payload=""
    for v in adj[(IP,PORT)]:
        payload+=v[0][0]+" "+str(v[0][1])+" "+str(v[1])+" "
        
    payload = IP+" "+str(PORT)+" "+str(5)+" "+payload
        
    for v in adj[(IP,PORT)]:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((v[0][0],v[0][1]))
            client.send(payload.encode(FORMAT))
            client.close()
        except:
            print("Error in connecting to the server, May be the server is down...")
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
            
            x = random.randint(0,1000)%len(adj[(IP,PORT)])
            before = adj[(IP,PORT)][x][1]
            
            # changing the weight of the edge
            tmp = list(adj[(IP,PORT)][x])
            tmp[1] = random.randint(0,1000)%100
            adj[(IP,PORT)][x] = tuple(tmp)
            if adj[(IP,PORT)][0] in adj:
                for v_node in adj[adj[(IP,PORT)][0]]:
                    if(v_node==(IP,PORT)):
                        tmp = list(v_node)
                        tmp[1] = adj[(IP,PORT)][x][1]
                        v_node=tuple(tmp)

if __name__=="__main__":
    main()