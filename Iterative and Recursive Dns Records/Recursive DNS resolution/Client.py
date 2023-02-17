import socket
import struct

ROOT_ADDR = ('127.0.0.1', 1194)
TLD_ADDR = ('127.0.0.1', 1195)
AUTH_ADDR = ('127.0.0.1', 1196)
SIZE = 1024
FORMAT = 'utf-8'

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

def main():
    x = 0;
    cur_addr= ""
    cur_type=""
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = input("Enter a domain name to send to the server: ")
        if message == "EXIT":
            break
        message = encode_msg(message)
        print("Sendig to root server")
        
        client.sendto(message, ROOT_ADDR)
        
        msg, addr = client.recvfrom(SIZE)
        print("paisi")
        val,nxt = decode_msg(msg)
        cur_addr = val
        print(f"The Ip for the given domain is : {cur_addr}")
    

if __name__ == '__main__':
    main()
