import socket
import struct

ADDR = ('127.0.0.1', 1234)
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

def main():
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        message = input("Enter a domain name to send to the server: ")
        if message == "EXIT":
            break
        message = encode_msg(message)
        
        client.sendto(message, ADDR)
        
        msg, addr = client.recvfrom(SIZE)
        print('In bytes: ')
        print(msg)

        header = struct.unpack("6H", msg[:12])
        ms = msg[12:].decode('utf-8')
        print('\n After Decoding')
        print({header},{ms})
        ms = ms.split()
        print("The value for given Domain : "+ms[1])
    

if __name__ == '__main__':
    main()
