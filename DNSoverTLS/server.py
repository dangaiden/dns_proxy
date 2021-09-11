import socket
import threading

#### SERVER DEFINITION


# Define port and IP (network addr)
HEADER= 64 #64 bytes for the 1st message

PORT = 5353
SERVER = "192.168.1.229"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# Create socket with INET (IPv4) and SOCK_STREAM (Socket type for TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind socket with Network address
server.bind (ADDR)

def handle_client (conn, addr):
    print(f"[NEW CONNECTION {addr} connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}]:{msg}")

    conn.close()




def start ():
    server.listen()
    print(f"Listening on {SERVER}")
    while True: #Listening while TRUE (basically infinite)
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")



print ("STARTING Server...")