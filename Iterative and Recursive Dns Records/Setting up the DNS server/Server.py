import socket
import threading
import struct

IP = ''
PORT = 1234
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

dns_records = {}

def getDnsRecords():
    x = 0;
    with open('dns_records.txt', 'r') as f:
        # loop through each line in the file
        for line in f:
            # print the line
            if x :
                words = line.split()
                dns_records[words[0]+"*"+words[2]]=[]
                print(words[0]+"*"+words[2])
                dns_records[words[0]+"*"+words[2]].append((words[1],words[3]))
            x = 1

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
            
            flag = 0
            q = 0
            a = 1
            auth_rr = 0
            add_rr = 0
            
            # Pack DNS header fields and message into the same buffer
            ms = (name + ' ' + value + ' ' + type + ' ' + ttl).encode('utf-8')
            packed_data = struct.pack(f"6H{len(ms)}s", 50, flag, q, a, auth_rr, add_rr, ms)
            
            server.sendto(packed_data, addr)

def main():
    getDnsRecords();
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")
    
    ok = 0

    while True:
        
        data, addr = server.recvfrom(SIZE)
        thread = threading.Thread(target=handle_client, args=(data, addr,server))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()