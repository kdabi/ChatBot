# server.py
import socket, sys
import time, os
import utilities.authentication as authentication

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

while True:
    # establish a connection
    clientSocket, addr = serverSocket.accept()

    print("Got a connection from %s" % str(addr))
    welcomeString = "Welcome to the chatting room\n Please provide username and password\n"
    clientSocket.send(welcomeString.encode('ascii'))
    userData = []
    username, status = authentication.authenticate(clientSocket)
    if not status:
        continue
    userData.append(username)
    userData.append(clientSocket)
    onlineUsers.append(userData)

clientSocket.close()
serverSocket.close()
