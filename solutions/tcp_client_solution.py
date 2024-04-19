import socket

FORMAT = "utf-8"
PORT = 2000
SERVER = "rick"
ADDR = (SERVER, PORT)

CHAMBRE_2ID = ""

def extractId(text):
   identifier_index = text.find("identifier:")
   # Check if the identifier is found
   if identifier_index != -1:
      # Extract the identifier by slicing the text
      identifier = text[identifier_index + len("identifier:"):].strip().split("\n")[0]
      # print("This is ID: ", identifier)
      return identifier
   else:
      return False
def parseLoveChar(id,text):
   # Find the index of "╭(◉)╮"
   index = text.find("╭(◉)╮")

   if index != -1:
      # Parse all char before "╭(◉)╮"
      substring = text[:index]

      # Count occurrences of "[❤]" in the substring
      loveChar = "[❤]" * substring.count("[❤]")
      
      return f"{id} {loveChar} --"
   else:
      return False

   


def Chambre_2(id):
   print("Chambre_2(), id:", id)
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 3006))

   try:
      # Read data from the socket
      received_data = b''
      while True:
         data_chunk = client_socket.recv(1024)  # Adjust buffer size as needed
         print("Chunk len", len(data_chunk))
         if len(data_chunk) == 96:
            print(data_chunk.decode("utf-8"))
         if not data_chunk:
               break  # No more data available
         received_data += data_chunk

      # Decode the received bytes using the correct encoding
      decoded_data = received_data.decode('utf-8')

      print(decoded_data)

      # Send the response
      response = parseLoveChar(id, decoded_data)
      print("Response:", response)
      client_socket.send(bytes(response, FORMAT))
   finally:
      # Close the socket
      client_socket.close()


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
      
      if recv_message.find("identifier") > -1:
         print("ID FOUND:", recv_message)
         Chambre_2(extractId(recv_message))


      

      

# Create starting socket
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