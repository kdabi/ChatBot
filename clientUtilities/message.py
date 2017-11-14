import socket
from time import gmtime, strftime

def personalMessage(mySocket, username):
    mySocket.send("Message".encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    message = raw_input("give message - ")
    if len(message) == 0:
        message = "-"
    message = strftime("%d-%m-%Y %H:%M:%S", gmtime())+ " : "+message+"\n"
    mySocket.send(message.encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('ascii'))
    reciever = raw_input("send message to - ")
    if len(reciever) == 0:
        reciever = "-"
    mySocket.send(reciever.encode('ascii'))
    msg = mySocket.recv(1024)
    print("%s\n" % msg.decode('ascii'))
    return
