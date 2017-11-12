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

def add(usernames, username, groupName, username2):
    groups = getGroups()
    if not username2 in  usernames:
        return "User " + username2 +" doesn't exists\n"
    elif not groupName in groups:
        return "Group "+ groupName+" doesn't exists.\n"
    elif not username in getMembers(groupName):
        return username +" is not a member of group " + groupName +".\n"
    elif username2 in getMembers(groupName):
        return username2 +" is already a member of group " + groupName +".\n"
    else:
        path = os.path.abspath("./database/group/"+ groupName +".txt")
        f = open(path, "a")
        f.write(username2 + "\n")
        f.close()
        return "User " + username2 +" added to group "+ groupName + ".\n"


