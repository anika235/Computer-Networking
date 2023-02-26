import socket
import random
import time

IP = 'localhost'
PORT = 8881
ADDR = (IP,PORT)
FORMAT = 'utf-8'
FILENAME = "send.txt"

def decode_msg(packet):
    seq=packet[:6]
    ack=packet[6:12]
    win=packet[12:16]
    check=packet[16:20]
    return (int(seq.decode(FORMAT)),int(ack.decode(FORMAT)),int(win.decode(FORMAT)),int(check.decode(FORMAT)))

def encode_msg(seq,ack,window,checksum,payload):
    seq = int(seq)
    ack = int(ack)
    window = int(window)
    checksum = int(checksum)
    transport_header = f'{seq:06d}{ack:06d}{window:04d}{checksum:04d}'.encode(FORMAT)[:20].ljust(20)
    
    # Build network layer header
    network_header = b'\x45\x00\x05\xdc'  # IP version 4, header length 20 bytes, total length 1500 bytes
    network_header += b'\x00\x00\x00\x00'  # Identification
    network_header += b'\x40\x06\x00\x00'  # TTL=64, protocol=TCP, checksum=0 (will be filled in by kernel)
    network_header += b'\x0a\x00\x00\x02'  # Source IP address
    network_header += b'\x0a\x00\x00\x01'  # Destination IP address
    
    # Build packet by concatenating headers and payload
    packet = network_header + transport_header + payload
    return packet

def main():
    # Set up server socket
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind(ADDR)
    SERVER.listen(1)

    print('Server is listening for incoming connections')

    # Accept a client connection
    client_socket, address = SERVER.accept()
    client_socket.settimeout(5)

    print(f'Accepted connection from {address}')

    # Set receive window size (in bytes)
    receive_window_size = 1460
    rwnd=5

    # Open file to be sent
    file = open(FILENAME, 'rb')
    timeout=0.4
    # Send packet with transport and network layer headers
    sequence_number = random.randint(0,0)
    ack_number=0
    while True:
        curr_sent=0
        stime=time.time()
        while time.time()-stime<timeout and rwnd>curr_sent:
            print('hi')
            payload = file.read(1460)
            payload_size=len(payload)
            ack_number+=payload_size
            print(payload_size)
            # Check if all file data has been read
            if not payload:
                break
            checksum=50
            packet=encode_msg(sequence_number,ack_number,rwnd,checksum,payload)
            sequence_number+=len(payload)

            print(sequence_number,ack_number,rwnd,checksum)

            client_socket.send(packet)
            curr_sent+=1
            print(f'Sent packet {sequence_number} currsent {curr_sent}')

        
        # Wait for acknowledgment from client

        try:
            acknowledgment = client_socket.recv(1024)
        except socket.timeout:
            print('No acknowledgment received within 5 seconds')
            break
        if acknowledgment:
            # Parse acknowledgment

            network_header = acknowledgment[:20]
            transport_header = acknowledgment[20:40]
            seq,acknowledgment_sequence_number,rwnd,checksum=decode_msg(transport_header)
            print(seq,acknowledgment_sequence_number,rwnd,checksum)

            # Check if all packets up to and including the acknowledged packet have been received
            if acknowledgment_sequence_number == sequence_number+payload_size:
                print(f'Received acknowledgment for packet {sequence_number}')
                sequence_number += payload_size
            else:
                print(f'Received acknowledgment for packet {acknowledgment_sequence_number}, but expected {sequence_number}')
        else:
            print('Did not receive acknowledgment')

    # Close file
    file.close()
        
    # Close sockets
    client_socket.close()
    SERVER.close()
    print('Done')

if __name__ == '__main__':
    strt_time = time.time()
    main()
    end_time = time.time()
    print(f'Total time needed to send a file of 1890kb  is : {end_time-strt_time} second')