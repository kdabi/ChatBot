import socket
from time import gmtime, strftime

def create(mySocket, username):
    mySocket.send("Create_Group".encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = raw_input("Group Name - ")
    if len(message) == 0:
        message = "-"
    mySocket.send(message.encode('ascii'))
    return
