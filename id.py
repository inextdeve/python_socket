import re

requested_rfc = re.search(r'/rfc(\d+)\.txt', "GET /rfc1952.txt HTTP/1.1")

print(requested_rfc)