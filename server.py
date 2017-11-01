# server.py
import socket, sys
import time, os
import utilities.authentication as authentication
import utilities.broadcast as broadcast
from thread import *

# create a socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checking number of arguments given
if len(sys.argv) != 3:
    print("Incorrect number of arguments")
    exit()

# get local machine name
host = sys.argv[1]

port = sys.argv[2]

#bind to the port
serverSocket.bind((host, int(port)))

# queue up to 100 requests i.e. it can handle maximum of 100 online clients as of now
serverSocket.listen(100)

# this dictionary contain username to their respective client socket for all active users
onlineUsers = []

def clientThread(clientSocket, addr):
    userData = []
    username, status = authentication.authenticate(clientSocket)
    if not status:
        clientSocket.close()
        return
    userData.append(username)
    userData.append(clientSocket)
    onlineUsers.append(userData)
    print("Got a connection from %s [%s]" % ( str(username), str(addr)))
    while True:
        msg = clientSocket.recv(1024).decode('ascii')
        if msg == "Broadcast":
            message = "SERVER: Give message to be Broadcasted"
            clientSocket.send(message.encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')
            broadcast.BroadcastMessage(onlineUsers, username, msg)
            message = "SERVER: Broadcasted your message"
            clientSocket.send(message.encode('ascii'))


while True:
    # establish a connection
    clientSocket, addr = serverSocket.accept()
    welcomeString = "Welcome to the chatting room\n Please provide username and password\n"
    clientSocket.send(welcomeString.encode('ascii'))
    start_new_thread(clientThread, (clientSocket, addr))

clientSocket.close()
serverSocket.close()
