import socket
import os
from time import gmtime, strftime

def update(username, currPassword, newPassword):
    if len(newPassword) < 3 or len(newPassword) >15:
        message = "Password must be of length 3-15.\n"
        return message
    path = os.path.abspath("./database/authenticationDetails.txt")
    f = open(path, "r")
    credentials = [x.strip().split(' ') for x in f.readlines()]
    f.close()
    f = open(path, "w")
    message = "Wrong password given\n"
    for user, password in credentials:
        if user == username and password == currPassword:
            f.write(user + " " + newPassword + "\n")
            message = "Updated the password of User \'" + user + "\'.\n"
        else:
            f.write(user + " " + password + "\n")
    f.close()
    return message












