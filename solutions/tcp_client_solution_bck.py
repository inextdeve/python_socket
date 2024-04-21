import socket
import hashlib
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
   try:
      text.decode(FORMAT)
   except:
      return False
   else:
      decoded_text = text.decode(FORMAT)
      # Find the index of "╭(◉)╮"
      index = decoded_text.find("╭(◉)╮")

      if index != -1:
         # Parse all char before "╭(◉)╮"
         substring = decoded_text[:index]

         # Count occurrences of "[❤]" in the substring
         loveChar = "[❤]" * substring.count("[❤]")
         
         return f"{id} {loveChar} --"
      else:
         return False
   

def word_before_last_completed_sum(text):
    words = text.split()
    total_sum = 0
    
    for i, item in enumerate(words):
        if item.isdigit():
            total_sum += int(item)
            if total_sum >= 1200:
               j = i - 1
               while words[j].isdigit():
                  j -= 1
               return words[j]
    return None

def Chambre_4(id):
   print("ID FROM 4", id)
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 9003))
   client_socket.send(bytes(id, FORMAT))


   sha1 = hashlib.sha1()

   file_size = 0
   fetched_data_size = 0
   i = 1
   while i > 0:
      data_chunk = client_socket.recv(4096)

      
      if file_size == 0:
         colon_position = data_chunk.find(b":")
         file_size = int(data_chunk[:colon_position].decode(FORMAT))
         fetched_data_size += len(data_chunk[colon_position + 1:])
         # data_chunk = data_chunk[colon_position + 1:]

      if len(data_chunk) + fetched_data_size > file_size:
         cursor = (len(data_chunk) + fetched_data_size) - file_size
         rest_bytes = len(data_chunk) - cursor
         # print("LAST BYTES", data_chunk[rest_bytes:].decode(FORMAT))
         print("FETCHED :", fetched_data_size + len(data_chunk[:rest_bytes]))
         print("FILESIZE:", file_size)
         sha1.update(data_chunk[:rest_bytes])
         sha1.update(data_chunk[rest_bytes:])
         break

      if not data_chunk or fetched_data_size >= file_size:
         print("Fetched data size", fetched_data_size)
         print("File size", file_size)
         break  
      
      sha1.update(data_chunk)
      fetched_data_size += len(data_chunk)

   file_sha1 = sha1.digest()
   print("SHA-1", file_sha1)
   client_socket.send(file_sha1)

   while True:
      print("SECOND LOOP")
      data_chunk = client_socket.recv(4096) 
      print(data_chunk.decode(FORMAT))
      if not data_chunk:
            break 



def Chambre_3(id):
   print("ID FROM 3", id)
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 5500))
   client_socket.send(bytes(extractId(id), FORMAT))
   while True:
      data_chunk = client_socket.recv(1024)
      try:
         data_chunk.decode(FORMAT)
         print(data_chunk.decode(FORMAT))
      except:
         print("False decoding")
      else:
         decoded_text = data_chunk.decode(FORMAT)
         if decoded_text.find("identifier") > -1:
            Chambre_4(extractId(decoded_text))
            client_socket.close()
            break
         check_sum = word_before_last_completed_sum(decoded_text)
         if(check_sum != None):
            client_socket.send(bytes(check_sum, FORMAT))
         

      if not data_chunk:
               break  # No more data available


def Chambre_2(id):
   print("Chambre_2(), id:", id)
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 3006))

   try:
      # Read data from the socket
      received_data = b''
      while True:
         data_chunk = client_socket.recv(1024)  # Adjust buffer size as needed
         try:
            data_chunk.decode(FORMAT)
            print(data_chunk.decode(FORMAT))
         except:
            print("False decoding")
         else:
            find_id = data_chunk.decode(FORMAT)
            if find_id.find("identifier") > -1:
               Chambre_3(find_id)

         if not data_chunk:
               break  # No more data available
         received_data += data_chunk

         if parseLoveChar(id, received_data) != False:
             # Send the response
            response = parseLoveChar(id, received_data)
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
   print(data.decode(FORMAT))
   id = extractId(data.decode(FORMAT))
   if(id):
      Chambre_1(id)
   
   if not data:
      break