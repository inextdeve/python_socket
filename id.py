from urllib.parse import urlparse

url = "/submit?identifier:8c8ad017-afe2-41%0A%0ACongrats!%20You%20have%20reached%20the%20final%20challenge.%0ATo%20get%20it%20is%20registered,%20just%20send%20'8c8ad017-afe2-41'%20to%0Athe%20TCP%20server%20at%20'rick:33333'%0AIf%20everything%20is%20ok,%20cake%20will%20be%20served.%0A%0A"

print(url[:url.find("%0")])