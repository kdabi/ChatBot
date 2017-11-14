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

def message(onlineUsers, usernames, username, groupName, message):
    groups = getGroups()
    if not groupName in groups:
        return "Group "+ groupName+" doesn't exists.\n"
    members = getMembers(groupName)
    if not username in members:
        return username +" is not a member of group " + groupName +".\n"

    for member in members:
        if member in usernames:
            if not member == username:
                msg = personal.PersonalMessage(onlineUsers, username, member, message, extra = " (" + groupName + ") "+ strftime("%d-%m-%Y %H:%M:%S", gmtime()) +" :")
        else:
            members.remove(member)

    path = os.path.abspath("./database/group/"+ groupName +".txt")
    f = open(path, "w")
    for member in members:
        f.write(member + "\n")
    f.close()
    return "your message sent to the group "+ groupName + ".\n"


