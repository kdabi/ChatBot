# server.py
import socket, sys
import os
from time import gmtime, strftime
import serverUtilities.authentication as authentication
import serverUtilities.signup as signup
import serverUtilities.broadcast as broadcast
import serverUtilities.message as personal
import serverUtilities.deleteAccount as deleteAccount
import serverUtilities.asynchronous as asynchronous
import serverUtilities.updatePassword as updatePassword
import serverUtilities.createGroup as createGroup
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
lastTimeActive = {}

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

        elif msg == "Online_Users" :
            msg = clientSocket.recv(1024).decode('ascii')
            message = str(onlineUsers.keys())
            clientSocket.send(message.encode('ascii'))

        elif msg == "Login":
            username, Authenticated = authentication.authenticate(onlineUsers, clientSocket)
            if not Authenticated:
                continue
            onlineUsers[username] = clientSocket
            print("%s | Got a connection from %s [%s]" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(username), str(addr)))
            blockedUsers = asynchronous.deliverMessage(username, clientSocket)

        elif msg == "Signup":
            username, Authenticated = signup.Signup(clientSocket)
            if not Authenticated:
                continue
            onlineUsers[username] = clientSocket
            usernames.append(username)
            print("%s | Got a connection from %s [%s]" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(username), str(addr)))
            blockedUsers = []


    while Authenticated:

        lastTimeActive[username] = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        msg = clientSocket.recv(1024).decode('ascii')

        if msg == "Block" :
            clientSocket.send("Pass".encode('ascii'))
            userToBlock = clientSocket.recv(1024).decode('ascii')
            if not userToBlock in usernames:
                message = "No such user exists.\n"
            elif userToBlock in blockedUsers:
                message = "user "+ userToBlock +" already blocked.\n"
            else:
                message = "user " + userToBlock + " blocked.\n"
                blockedUsers.append(userToBlock)
                f = open("./database/block/" + username + ".txt", "a")
                f.write(userToBlock + "\n")
                f.close()
            clientSocket.send(message.encode('ascii'))

        elif msg == "Exit" :
            onlineUsers.pop(username)
            print("%s | Disconnected from %s [%s]" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(username), str(addr)))
            clientSocket.close()
            lastTimeActive[username] = strftime("%d-%m-%Y %H:%M:%S", gmtime())
            return

        elif msg == "Unblock" :
            clientSocket.send("Pass".encode('ascii'))
            userToBlock = clientSocket.recv(1024).decode('ascii')
            if not userToBlock in usernames:
                message = "No such user exists.\n"
            elif not userToBlock in blockedUsers:
                message = "user "+ userToBlock +" is not blocked by you.\n"
            else:
                message = "user " + userToBlock + " unblocked.\n"
                blockedUsers.remove(userToBlock)
                f = open("./database/block/" + username + ".txt", "w")
                f.close()
                f = open("./database/block/" + username + ".txt", "a")
                for userToBlock in blockedUsers:
                    f.write(userToBlock + "\n")
                f.close()
            clientSocket.send(message.encode('ascii'))

        elif msg == "Check_User" :
            clientSocket.send("Pass".encode('ascii'))
            userToCheck = clientSocket.recv(1024).decode('ascii')
            if not userToCheck in usernames:
                message = "No such user exists.\n"
            elif userToCheck in onlineUsers:
                message = "user \'"+ userToCheck +"\' is active now.\n"
            elif userToCheck in lastTimeActive.keys():
                message = "user \'"+ userToCheck +"\' was last time active at " + lastTimeActive[userToCheck] + ".\n"
            else:
                message = "user \'"+ userToCheck +"\' was never active in this session.\n"
            clientSocket.send(message.encode('ascii'))

        elif msg == "Online_Users" :
            clientSocket.send("Pass".encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')
            message = str(onlineUsers.keys())
            clientSocket.send(message.encode('ascii'))

        elif msg == "Broadcast":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give message to be Broadcasted"
            clientSocket.send(message.encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')
            broadcast.BroadcastMessage(onlineUsers, username, msg)
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": Broadcasted your message\n"
            clientSocket.send(message.encode('ascii'))

        elif msg == "Create_Group":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give name of the group you want to create."
            clientSocket.send(message.encode('ascii'))
            groupName = clientSocket.recv(1024).decode('ascii')
            message = createGroup.create(username, groupName)
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": " + message
            clientSocket.send(message.encode('ascii'))

        elif msg == "Message":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give message"
            clientSocket.send(message.encode('ascii'))
            msg = clientSocket.recv(1024).decode('ascii')

            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Give user id of receiver"
            clientSocket.send(message.encode('ascii'))
            receiver = clientSocket.recv(1024).decode('ascii')

            if receiver in usernames:
                message = personal.PersonalMessage(onlineUsers, username, receiver, msg)
                clientSocket.send(message.encode('ascii'))
            else:
                message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": User \'" + receiver + "\' doesn't exist.\n"
                clientSocket.send(message.encode('ascii'))

        elif msg == "Delete_Account":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Enter Current Password"
            clientSocket.send(message.encode('ascii'))
            currPassword = clientSocket.recv(1024).decode('ascii')

            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Enter Confirm Password"
            clientSocket.send(message.encode('ascii'))
            confirmPassword = clientSocket.recv(1024).decode('ascii')

            message = deleteAccount.Remove(username, currPassword, confirmPassword)
            clientSocket.send(message.encode('ascii'))
            if message == "User \'" + username + "\' deleted.\n":
                usernames.remove(username)

        elif msg == "Update_Password":
            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Enter Current Password"
            clientSocket.send(message.encode('ascii'))
            currPassword = clientSocket.recv(1024).decode('ascii')

            message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) + ": Enter New Password"
            clientSocket.send(message.encode('ascii'))
            newPassword = clientSocket.recv(1024).decode('ascii')

            message = updatePassword.update(username, currPassword, newPassword)
            clientSocket.send(message.encode('ascii'))


while True:
    # establish a connection
    clientSocket, addr = serverSocket.accept()
    welcomeString =  strftime("%d-%m-%Y %H:%M:%S", gmtime()) +"  Welcome to the chatting room\nPlease Login or Signup\n"
    clientSocket.send(welcomeString.encode('ascii'))
    start_new_thread(clientThread, (clientSocket, addr))

clientSocket.close()
serverSocket.close()
