import socket
import os
from time import gmtime, strftime


def sendBlockData(clientSock, message):
    #size = len(message)
    #clientSock.send(size.encode('ascii'))
    while message:
        sentSize = clientSock.send(message.encode('ascii'))
        message = message[sentSize:]

def storeMessage(receiver, message):
    filePath = os.path.abspath("./database/" + receiver + ".txt")
    receiverFile = open(filePath, 'a')
    receiverFile.write(message)
    receiverFile.close()

def getBlockedUsers(username):
    path = os.path.abspath("./database/block/" + username + ".txt")
    f = open(path, "r")
    blockedUsers = [x.strip() for x in f.readlines()]
    f.close()
    return blockedUsers


def PersonalMessage (onlineUsers, sender, receiver, message, extra = ""):
    message = sender + extra + " " + message
    blockedUsers = getBlockedUsers(receiver)
    myBlockedUsers = getBlockedUsers(sender)

    if receiver in myBlockedUsers:
        message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": User " + receiver +" is BLOCKED by you.\n"
        return message

    elif sender in blockedUsers:
        message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": User " + receiver +" has BLOCKED you.\n"
        return message

    elif receiver in onlineUsers.keys():
        clientSock = onlineUsers[receiver]
        try:
            sendBlockData(clientSock, message)
        except:
            clientSock.close()
            onlineUsers.pop(receiver)
            storeMessage(receiver, message)
    else:
        storeMessage(receiver, message)
    message = "SERVER "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +": sent your message\n"
    return message












