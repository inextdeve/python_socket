import socket

FORMAT = "utf-8"
PORT = 2000
SERVER = "rick"
ADDR = (SERVER, PORT)

def extractId(text):
   identifier_index = text.find("identifier:")
   # Check if the identifier is found
   if identifier_index != -1:
      # Extract the identifier by slicing the text
      identifier = text[identifier_index + len("identifier:"):].strip().split("\n")[0]
      print("This is ID: ", identifier)
      return identifier
   else:
      return False
def parseLoveChar(text):
   # Find the index of "╭(◉)╮"
   index = text.find("╭(◉)╮")

   if index != -1:
      # Parse all char before "╭(◉)╮"
      substring = text[:index]

      # Count occurrences of "[❤]" in the substring
      loveChar = "[❤]" * substring.count("[❤]")
      return f"0a593688-5c26-46ae-ad0 {loveChar} --"
   else:
      return False

   


def Chambre_2():
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 3006))

   while True:
      data = client_socket.recv(1024)
      print(data.decode(FORMAT))
      # decoded_data = parseLoveChar(data.decode(FORMAT))
      # print(decoded_data)
      # client_socket.send(bytes(decoded_data, FORMAT))
      if not data:
         break

def Chambre_1(id):
   PORT = 65498
   SERVER = socket.gethostbyname(socket.gethostname())
   ADDR = (SERVER, PORT)
   ID = id

   server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   server_socket.bind(ADDR)

   server_socket.sendto(bytes(f"{PORT} {ID}", FORMAT), ("rick", 4000))

   while True:
      data, address = server_socket.recvfrom(1024)
      recv_message = data.decode(FORMAT)

      print(f"Received message from {address}: {recv_message}")
      
      if recv_message.find("upper-code") > -1:
         server_socket.sendto(bytes(ID.upper(), FORMAT), address)
         Chambre_2()

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

client.send(bytes("whole_shrimp", FORMAT))

while True:
   data = client.recv(1024)
   id = extractId(data.decode(FORMAT))
   if(id):
      Chambre_1(id)
   
   if not data:
      break