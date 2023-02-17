import socket
import struct
import time
from datetime import datetime

ROOT_ADDR = ('127.0.0.1', 1194)
TLD_ADDR = ('127.0.0.1', 1195)
AUTH_ADDR = ('127.0.0.1', 1196)
SIZE = 1024
FORMAT = 'utf-8'

cache = {}

def encode_msg(message):
    data = message.split()
    name = data[0]
    type = data[1]
    
    flag = 0
    q = 0
    a = 1
    auth_rr = 0
    add_rr = 0

    ms = (name + ' ' + type).encode('utf-8')
    packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)
    return packed_data

def decode_msg(msg):
    header = struct.unpack("6H", msg[:12])
    ms = msg[12:].decode('utf-8')
    print('\n After Decoding')
    print({header},{ms})
    ms = ms.split()
    return ms[1],ms[4],ms[3]

def main():
    x = 0;
    cur_addr= ""
    cur_type=""
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = input("Enter a domain name to send to the server: ")
        data = message.split()
        
        chkl = True
        if data[0] in cache:
            diff = datetime.now()- cache[data[0]][2]
            xx = int(diff.total_seconds())
            print(f"data[0] = {data[0]} and diff = {xx} and , cache[data[0]] = {cache[data[0]]}")
            if int(cache[data[0]][1]) > xx :
                cur_addr = cache[data[0]][0]
                chkl = False
            else:
                #deleting from the cache
                del cache[data[0]]
                
        if message == "EXIT":
            break
        if chkl:
            message = encode_msg(message)
            print("Sendig to root server")
            
            client.sendto(message, ROOT_ADDR)
            
            msg, addr = client.recvfrom(SIZE)
            print("paisi")
            val,nxt,ttl = decode_msg(msg)
            cur_addr = val
            cache[data[0]]=(cur_addr,ttl,datetime.now())
        print(f"The Ip for the given domain is : {cur_addr}")
    

if __name__ == '__main__':
    main()
