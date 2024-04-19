import socket

PORT = 2000

SERVER = "10.0.2.15"

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

server.listen()

while True:
    clientSocket, address = server.accept()
    clientSocket.send(bytes("Hello", "utf-8"))
    clientSocket.close()