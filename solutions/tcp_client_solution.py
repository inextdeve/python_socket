import socket
import hashlib
import sys
import struct
import array
import base64
import threading
import re

FORMAT = "utf-8"
PORT = 2000
SERVER = "rick"
ADDR = (SERVER, PORT)

CHAMBRE_2ID = ""

def cksum(pkt):
    # type: (bytes) -> int
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s

    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8

    return s & 0xffff

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
# Generate WYP Packet
# def wyp_packet(payload, type = 0, code = 0):
#    header = struct.pack("3sBHH", b"WYP",type, code, 0)
#    checksum = cksum(header + payload)

#    header =   struct.pack("3sBHHH", b"WYP", type, code, checksum, 0)
#    payload = base64.b64encode(payload.decode(FORMAT).encode())

#    return header + payload

def wyp_packet(payload, type = 0, code = 0):
   payload_base64 = base64.b64encode(payload.encode())
   message_format = f"!3sBHHH{len(payload_base64)}s"
   header = b"WYP"
   sequence = 1

   checksum = cksum(struct.pack(message_format, header, type, code, 0, sequence, payload_base64))

   message = struct.pack(message_format, header, type, code, checksum, sequence, payload_base64)   
   
   return message

# Parse WYP Packet
def wyp_parse(packet): 
   parsed_header = packet[:10]
   message = packet[10:]
   req_type = packet[3:4]
   header = struct.unpack("H H H", parsed_header[4:])
   decoded_msg = base64.b64decode(message).decode()
   return decoded_msg

def http_get_server():
   WEB_PORT = 7702
   SERVER = socket.gethostbyname(socket.gethostname())
   ADDR = (SERVER, WEB_PORT)

   web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   web_socket.bind(ADDR)
   web_socket.listen(1)

   while True:
      print("GET SERVER:")
      # Accept incoming connection
      client_connection, client_address = web_socket.accept()
      print(f"Connection from {client_address}")

      # Receive data from the client
      request = client_connection.recv(1024).decode(FORMAT)
      print("Received request:")
      print(request)

      # Parse the request (for demonstration purposes)
      request_lines = request.split('\r\n')
      if len(request_lines) > 0:
         method, path, _ = request_lines[0].split(' ')
         print(f"Method: {method}")
         print(f"Path: {path}")

         requested_rfc = re.search(r'/rfc(\d+)\.txt', request)
         if requested_rfc:
            rfc_number = requested_rfc.group(1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as web_client:
               web_client.connect(('web', 81))
               
               # print("HELLO", f"GET /rfc/rfc{rfc_number}.txt HTTP/1.1\r\nHost: web\r\n\r\n".encode())
               web_client.sendall(f"GET /rfc/rfc{rfc_number}.txt HTTP/1.1\r\nHost: web\r\n\r\n".encode())
               response = b""
               web_client.settimeout(1)
               while True:
                  try:
                     chunk = web_client.recv(4096)
                     if not chunk:
                        break
                     response += chunk
                  except socket.timeout:
                        break
               
               try:
                  client_connection.sendall(response)
               except:
                  print("Disconnected client")
         


      # Close the connection
      client_connection.close()

def Chambre_6(id):
   WEB_PORT = 7702

   thread = threading.Thread(target=http_get_server)
   thread.start()
   
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   client_socket.connect(("rick", 8003))
   client_socket.send(bytes(f"{id} {WEB_PORT}", FORMAT))

   while True:
      data_chunk = client_socket.recv(4096)
      print(data_chunk.decode(FORMAT))
      if not data_chunk:
         break

   





def Chambre_5(id):

   client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   client_socket.connect((SERVER, 6000))
   client_socket.send(wyp_packet(id))

   while True:
      data_chunk = client_socket.recv(4096)
      print(wyp_parse(data_chunk))
      id = extractId(wyp_parse(data_chunk))
      if(id):
         Chambre_6(id)
      if not data_chunk:
         break

def Chambre_4(id):
   print("ID FROM 4", id)
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   client_socket.connect(("rick", 9003))
   client_socket.send(bytes(id, FORMAT))


   sha1 = hashlib.sha1()

   file_size = 0
   fetched_data_size = 0

   while True:
      data_chunk = client_socket.recv(4096)

      if file_size == 0:
         colon_position = data_chunk.find(b":")
         file_size = int(data_chunk[:colon_position].decode(FORMAT))
         data_chunk = data_chunk[len(data_chunk[:colon_position]) + 1:]
      
      fetched_data_size += len(data_chunk)
      sha1.update(data_chunk)

      if not data_chunk or fetched_data_size == file_size:
         break

   file_sha1 = sha1.digest()
   print("SHA-1", file_sha1)
   client_socket.send(file_sha1)
   print("FILESIZE:", file_size)
   print("FETCHED :", fetched_data_size)
   while True:
      print("SECOND LOOP")
      data_chunk = client_socket.recv(4096) 
      print(data_chunk.decode(FORMAT))
      id = extractId(data_chunk.decode(FORMAT))
      if(id):
         Chambre_5(id)
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