import socket
import getpass
from time import gmtime, strftime

def Remove(mySocket, username):
    mySocket.send("Delete_Account".encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = getpass.getpass()
    if len(message) == 0:
        message = "~!@#@!~"
    mySocket.send(message.encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = getpass.getpass()
    if len(message) == 0:
        message = "~!@#@!~"
    mySocket.send(message.encode('ascii'))
    msg = mySocket.recv(1024)
    message = "User \'" + username + "\' deleted.\n"
    print("%s\n" % msg.decode('ascii'))
    if msg == message:
        return True
    return False
