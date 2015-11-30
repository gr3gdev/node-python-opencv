import socket
from base64 import decodestring

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 4004)
print 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    data = sock.recv(8092*8)
    print 'received "%s"' % data
    
    with open("foo.png","wb") as f:
        f.write(decodestring(data))

finally:
    print 'closing socket'
    sock.close()
