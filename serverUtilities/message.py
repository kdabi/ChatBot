import socket
import os


def sendBlockData(clientSock, message):
    #size = len(message)
    #clientSock.send(size.encode('ascii'))
    while message:
        sentSize = clientSock.send(message.encode('ascii'))
        message = message[sentSize:]

def storeMessage(receiver, message):
    filePath = os.path.abspath("./database/" + receiver + ".txt")
    with open(filePath, 'w') as receiverFile:
        receiverFile.write(message + "\n")
    receiverFile.close()

def PersonalMessage (onlineUsers, sender, receiver, message):
    message = sender + " " + message
    if receiver in onlineUsers.keys():
        clientSock = onlineUsers[receiver]
        try:
            sendBlockData(clientSock, message)
        except:
            clientSock.close()
            onlineUsers.pop(receiver)
            storeMessage(receiver, message)
    else:
        storeMessage(receiver, message)












