import socket
import os, sys

def getGroups():
    path = os.path.abspath("./database/group/gp.txt")
    f = open(path, "r")
    groups = [x.strip() for x in f.readlines()]
    f.close()
    return groups

def getMembers(groupName):
    path = os.path.abspath("./database/group/"+ groupName +".txt")
    f = open(path, "r")
    members = [x.strip() for x in f.readlines()]
    f.close()
    return members

def deleteGroup(username, groupName):
    groups = getGroups()
    if not groupName in groups:
        return "Group "+ groupName+" doesn't exists.\n"
    members = getMembers(groupName)
    if not username in members:
        return "You are not a member of group "+ groupName+".\n"
    else:
        groups.remove(groupName)
        path1 = os.path.abspath("./database/group/"+ groupName + ".txt")
        os.remove(path1)
        path = os.path.abspath("./database/group/gp.txt")
        f = open(path, "w")
        for group in groups:
            f.write(group + "\n")
        f.close()
        return "Group "+ groupName +" deleted.\n"


