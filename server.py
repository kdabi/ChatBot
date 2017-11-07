# server.py
import socket, sys
import os
from time import gmtime, strftime
import serverUtilities.authentication as authentication
import serverUtilities.broadcast as broadcast
import serverUtilities.message as personal
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
onlineUsers = {}

path = os.path.abspath("./database/authenticationDetails.txt")
# taking authentication credentials from the database
with open(path) as f:
    credentials = [x.strip().split(' ') for x in f.readlines()]
f.close()

usernames = []

for username, password in credentials:
    usernames.append(username)

def clientThread(clientSocket, addr):
    Authenticated = False
    while not Authenticated:
        msg = clientSocket.recv(1024).decode('ascii')
        clientSocket.send("pass".encode("ascii"))

        if msg == "Exit" :
            clientSocket.close()
            return

        elif msg == "Login":
            username, Authenticated = authentication.authenticate(clientSocket)
            if not Authenticated:
                clientSocket.close()
                return
            onlineUsers[username] = clientSocket
            print("%s | Got a connection from %s [%s]" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(username), str(addr)))



    while Authenticated:

        msg = clientSocket.recv(1024).decode('ascii')

        if msg == "Exit" :
            print("%s | Disconnected from %s [%s]" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(username), str(addr)))
            clientSocket.close()
            return

        elif msg == "Broadcast":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give message to be Broadcasted"
            clientSocket.send(message.encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')
            broadcast.BroadcastMessage(onlineUsers, username, msg)
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": Broadcasted your message"
            clientSocket.send(message.encode('ascii'))

        elif msg == "Message":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give message"
            clientSocket.send(message.encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')

            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give user id of receiver"
            clientSocket.send(message.encode('ascii'))
            receiver = clientSocket.recv(1024).decode('ascii')

            if receiver in usernames:
                personal.PersonalMessage(onlineUsers, username, receiver, msg)
                message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": sent your message"
                clientSocket.send(message.encode('ascii'))
            else:
                message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": User \'" + receiver + "\' doesn't exist."
                clientSocket.send(message.encode('ascii'))


while True:
    # establish a connection
    clientSocket, addr = serverSocket.accept()
    welcomeString =  strftime("%d-%m-%Y %H:%M:%S", gmtime()) +"  Welcome to the chatting room\n"
    clientSocket.send(welcomeString.encode('ascii'))
    start_new_thread(clientThread, (clientSocket, addr))

clientSocket.close()
serverSocket.close()
