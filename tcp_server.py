import socket
import threading

HEADER = 64
PORT = 5050

# gethostbyname() get the ip address of the host by it's name
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "10.0.2.15"

ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
    # We need to close the connection when receiving a "DISCONNECT_MESSAGE"
    conn.close()
    print(f"[CONNECTION CLOSED] {addr} connected.")

# Start listening for the connection
def start():

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    # For infinitely listening to new client request
    while True:
        conn, addr = server.accept()
        # Using thread for avoid code blocking and handling more clients not waiting for a client to finish for handling a new one
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting ....")

start()