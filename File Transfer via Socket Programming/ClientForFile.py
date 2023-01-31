import socket
import os

IP = socket.gethostbyname(socket.gethostname())
print(str(IP))
PORT = 1244
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
server_download = "client_data"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
        elif cmd == "DOWNLOAD":
            newpath=str(data[1]) 
            newmsg=f"{cmd}@{newpath}"
            client.send(newmsg.encode(FORMAT))
            rcv=client.recv(SIZE).decode(FORMAT)
            rcv=rcv.split("@")
            name, text = rcv[1], rcv[2]
            #name = "server_data/"+name
            filepath = os.path.join(server_download, name)
            with open(filepath, "w") as f:
                f.write(text)
                f.close()
            print("downloaded...")
            #continue
            
    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()