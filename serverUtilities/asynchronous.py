import os
import socket

def deliverMessage(username , clientSocket):
    path = os.path.abspath("./database/" + username + ".txt")
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    f = open(path, "w")
    f.close()
    for line in lines:
        clientSocket.send(line.encode('ascii'))

    path = os.path.abspath("./database/block/" + username + ".txt")
    f = open(path, "r")
    blockedUsers = [x.strip() for x in f.readlines()]
    f.close()
    return blockedUsers
