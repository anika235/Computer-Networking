import socket
import threading
import struct

IP = ''
PORT = 1195
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
ROOT_ADDR = ('127.0.0.1', 1194)
TLD_ADDR = ('127.0.0.1', 1195)
AUTH_ADDR = ('127.0.0.1', 1196)

dns_records = {}

def getDnsRecords():
    with open('dns_records.txt', 'r') as f:
        # loop through each line in the file
        for line in f:
            words = line.split()
            if words[2] == "NS" or words[2] == "MX":
                
                dns_records[words[0]+"*"+words[2]]=[]
                print(words[0]+"*"+words[2])
                dns_records[words[0]+"*"+words[2]].append((words[1],words[3],words[4]))
                
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
    return ms[1],ms[4]

def handle_client(data, addr, server):
    while True:
        
        header = struct.unpack("6H", data[:12])
        ms = data[12:].decode(FORMAT)
        print('\n After Decoding')
        print({header},{ms})
        ms = ms.split()
        print(f"ms = {ms}")
        
        print(f"[RECEIVED MESSAGE] {data} from {addr}.")

        data = ms
        print(data[0])
        print(data[1])
        str = data[0]+"*"+data[1]
        print(str)
        if str in dns_records :
            print(dns_records[str])
            name = data[0]
            value = dns_records[str][0][0]
            type = data[1]
            ttl = dns_records[str][0][1]
            addrs = dns_records[str][0][2]
            
            flag = 0
            q = 0
            a = 1
            auth_rr = 0
            add_rr = 0
            
            # Pack DNS header fields and message into the same buffer
            ms = (name + ' ' + value + ' ' + type + ' ' + ttl + ' ' + addrs).encode('utf-8')
            packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)
            
            if addrs=="X" :
                server.sendto(packed_data, addr)
                
            elif addrs=="AUTH":
                client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                print("Sendig to TLD server")
                packed_data = encode_msg(value+" A")
                client.sendto(packed_data, AUTH_ADDR)
                msg, addrr = client.recvfrom(SIZE)
                val,nxt = decode_msg(msg)
                print(f"val = {val} and nxt = {nxt}")
                ms = (name + ' ' + val + ' ' + type + ' ' + ttl + ' ' + addrs).encode('utf-8')
                packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)
                server.sendto(packed_data, addr)

def main():
    getDnsRecords();
    print("[STARTING] TLD Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] TLD Server is listening on {IP}:{PORT}.")
    
    ok = 0

    while True:
        
        data, addr = server.recvfrom(SIZE)
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()