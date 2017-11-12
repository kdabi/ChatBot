import socket
import os, sys

def getGroups():
    path = os.path.abspath("./database/group/gp.txt")
    f = open(path, "r")
    groups = [x.strip() for x in f.readlines()]
    f.close()
    return groups


def create(username, groupName):
    groups = getGroups()
    if len(groupName) < 3 or len(groupName)>15:
        return "Group Name should of length 3-15\n"
    elif groupName in groups:
        return "Group "+ groupName+" already exists.\n"
    else:
        path = os.path.abspath("./database/group/gp.txt")
        path1 = os.path.abspath("./database/group/"+ groupName +".txt")
        f = open(path, "w")
        for gp in groups:
            f.write(gp + "\n")
        f.write(groupName + "\n")
        f.close()
        f = open(path1, "w")
        f.write(username + "\n")
        f.close()
        return "Group "+ groupName +" created.\n"


