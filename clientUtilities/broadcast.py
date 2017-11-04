import socket
from time import gmtime, strftime

def broadcast(mySocket, username):
    mySocket.send("Broadcast".encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = raw_input("give message - ")
    message = strftime("%d-%m-%Y %H:%M:%S", gmtime())+ " : "+message+"\n"
    mySocket.send(message.encode('ascii'))
    return
