import socket
import os
from time import gmtime, strftime

def Remove(username, currPassword, confirmPassword):
    if not currPassword == confirmPassword :
        message = "Confirm Password doesn't match.\n"
        return message
    path = os.path.abspath("./database/authenticationDetails.txt")
    path1 = os.path.abspath("./database/" + username + ".txt")
    path2 = os.path.abspath("./database/block/" + username + ".txt")
    f = open(path, "r")
    credentials = [x.strip().split(' ') for x in f.readlines()]
    f.close()
    f = open(path, "w")
    message = "Wrong password given\n"
    for user, password in credentials:
        if user == username and password == currPassword:
            message = "User \'" + username + "\' deleted.\n"
            try:
                os.remove(path1)
            except OSERROR:
                pass
            try:
                os.remove(path2)
            except OSERROR:
                pass
        else:
            f.write(user + " " + password + "\n")
    f.close()
    return message












