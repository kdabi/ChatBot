import socket
import getpass
from time import gmtime, strftime

def update(mySocket, username):
    mySocket.send("Update_Password".encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = getpass.getpass()
    if len(message) == 0:
        message = "-"
    mySocket.send(message.encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = getpass.getpass()
    if len(message) == 0:
        message = "-"
    mySocket.send(message.encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s\n" % msg.decode('ascii'))
