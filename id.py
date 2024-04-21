import struct
import array
import sys
import base64
FORMAT = "utf-8"
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
# Generate WYP Packet
def wyp_packet(payload, type = 0, code = 0):
   print(struct.pack("H", 0))
   header = struct.pack("3sBHHH", b"WYP",type, code, 0, 0)
   checksum = cksum(header + payload)

   header = struct.pack("3sBHHH", b"WYP",type, code, checksum, 0)
   checksum_b = struct.pack("H", checksum)
   print(checksum_b)
   payload = base64.b64encode(payload.decode(FORMAT).encode())
   return header + payload

# Parse WYP Packet
def wyp_parse(packet): 
   parsed_header = packet[:10]
   message = packet[10:]
   req_type = packet[3:4]
   header = struct.unpack("H H H", parsed_header[4:])
   decoded_msg = base64.b64decode(message).decode()
   print("DECODED MSG", header)

# wyp = wyp_packet(b"aaedb8c32e87-4884efssb")
wyp = b'WYP\x01\x00\x00\x86x\x00\x01aWRlbnRpZmllcjo8c3RheS10dW5uZWQ+CgpNb3JlIGNoYWxsZW5nZXMgd2lsbCBiZSBhZGRlZCBzb29uLCBzdGF5IHR1bmVkIQo='
wyp_parse(wyp)