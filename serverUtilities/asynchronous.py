import os
import socket

path = os.path.abspath("./database/authenticationDetails.txt")

def deliverMessage(username , clientSocket):
    path = os.path.abspath("./database/" + username + ".txt")
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    f = open(path, "w")
    f.close()
    for line in lines:
        clientSocket.send(line.encode('ascii'))
