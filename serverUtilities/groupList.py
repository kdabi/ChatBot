import socket
import os, sys
import message as personal
from time import gmtime, strftime

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

def getList(username):
    groups = getGroups()
    groupList = []

    for groupName in groups:
        members = getMembers(groupName)
        if username in members:
            groupList.append(groupName)

    return groupList
