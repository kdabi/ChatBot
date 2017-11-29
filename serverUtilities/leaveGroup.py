import socket
import os, sys

def getGroups():
    path = os.path.abspath("./database/group/gp.txt")
    f = open(path, "r")
    groups = [x.strip() for x in f.readlines()]
    f.close()
    return groups

def getMember(groupName):
    path = os.path.abspath("./database/group/"+ groupName +".txt")
    f = open(path, "r")
    members = [x.strip() for x in f.readlines()]
    f.close()
    return members

def leave(username, groupName):
    groups = getGroups()
    if not groupName in groups:
        return "Group "+ groupName+" doesn't exists.\n"
    members = getMember(groupName)
    if not username in members:
        return "You are not a member of group "+ groupName+".\n"
    else:
        members.remove(username)
        path = os.path.abspath("./database/group/"+ groupName + ".txt")
        f = open(path , "w")
        for member in members:
            f.write(member + "\n")
        f.close()
        return "You are no longer a member of group \"" + groupName + "\".\n"


