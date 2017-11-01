#client.py
import socket
import sys

#create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = sys.argv[1]

port = 9999

# connection to hostname on the port
s.connect((host,port))

# Receive no more than 1024 bytes
tm = s.recv(1024)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))


