import socket


def sendBlockData(clientSock, message):
    #size = len(message)
    #clientSock.send(size.encode('ascii'))
    while message:
        sentSize = clientSock.send(message.encode('ascii'))
        message = message[sentSize:]


def BroadcastMessage (onlineUsers, sender, message):
    message = sender + " Broadcasted at " + message
    for username, clientSock in onlineUsers:
        if username != sender:
            try:
                sendBlockData(clientSock, message)
            except:
                clientSock.close()
                onlineUsers.pop(username)












