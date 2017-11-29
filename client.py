#client.py
import socket
from time import gmtime, strftime
import sys
import select
import clientUtilities.authentication as authenticate
import clientUtilities.signup as signup
import clientUtilities.broadcast as broadcast
import clientUtilities.message as personal
import clientUtilities.deleteAccount as deleteAccount
import clientUtilities.updatePassword as updatePassword
import clientUtilities.createGroup as createGroup
import clientUtilities.addMember as addMember
import clientUtilities.messageGroup as messageGroup
import clientUtilities.deleteGroup as deleteGroup
import clientUtilities.groupMembers as groupMembers
import clientUtilities.leaveGroup as leaveGroup
import time

#create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# checking number of arguments given
if len(sys.argv) != 3:
    print("Incorrect number of arguments")
    exit()

#get local machine name
host = sys.argv[1]

port = sys.argv[2]

# connection to hostname on the port
s.connect((host,(int)(port)))

# Receive no more than 1024 bytes
tm = s.recv(1024)

print("%s" % (tm.decode('ascii')))
print("User OPTIONS are :\n0. Options, 1. Signup, 2. Login, 3. Broadcast, 4. Message, 5. Online_Users, 6. Block, 7. Unblock, 8. Check_User, 9. Logout, 10. Update_Password, 11. Delete_Account, 12. Create_Group, 13. Add_Member, 14. Message_Group, 15. Delete_Group, 16. Group_List, 17. Group_Members, 18. Leave_Group, 19. Exit\n")

Authenticated = False
wait = 0
future = int(time.time())

while(True):
    socketsList = [sys.stdin, s]
    readSockets, writeSockets, errorSockets = select.select(socketsList,[],[])

    for socks in readSockets:
        if socks == s:
            # Sever is giving some output
            msg = s.recv(1024)
            print("%s" % msg.decode('ascii'))
            message = "pass"
            s.send(message.encode('ascii'))
        else:
            message = sys.stdin.readline()

            # If the user chooses Signup Option, can't be choose after Loggedin
            if message == "Signup\n" or message == "1\n":
                if Authenticated:
                    print("Already Loggedin\n")
                elif future > int(time.time()):
                    print("Can't login or signup for %s more seconds.\n" % str(future +1 - int(time.time())))
                else:
                    username, Authenticated = signup.Signup(s)

            # if user wants to print options
            elif message == "Options\n" or message == "0\n" or message == "\n":
                print("User OPTIONS are :\n0. Options, 1. Signup, 2. Login, 3. Broadcast, 4. Message, 5. Online_Users, 6. Block, 7. Unblock, 8. Check_User, 9. Logout, 10. Update_Password, 11. Delete_Account, 12. Create_Group, 13. Add_Member, 14. Message_Group, 15. Delete_Group, 16. Group_List, 17. Group_Member, 18. Leave_Group, 19. Exit\n")

            # If the user chooses Login Option, can't be choose after authenticated
            elif message == "Login\n" or message == "2\n":
                if Authenticated:
                    print("Already Loggedin\n")
                elif future > int(time.time()):
                    print("Can't login or signup for %s more seconds.\n" % str(future - int(time.time()) ))
                else:
                    username, Authenticated = authenticate.authenticate(s)
                    if not Authenticated:
                        if wait == 0:
                            wait = 30
                            future = int(time.time()) + wait
                        else:
                            wait = 2*wait
                            future = int(time.time()) + wait
                        print("Can't login or signup for %s more seconds.\n" % str(wait))
                    else:
                        wait = 0
                        future = int(time.time())

            # If user wants to log out
            elif message == "Logout\n" or message == "9\n":
                if not Authenticated:
                    print("First Login  !!!")
                else:
                    s.send("Exit".encode("ascii"))
                    msg = s.recv(1024)
                    s.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host,(int)(port)))
                    tm = s.recv(1024)
                    print("Logged Out Successfully")
                    print("%s" % (tm.decode('ascii')))
                    Authenticated = False
                    continue


            # If the user wants to exit
            elif message == "Exit\n" or message == "19\n":
                s.send("Exit".encode("ascii"))
                msg = s.recv(1024)
                s.close()
                exit()

            # If the user wants to block another user
            elif message == "Block\n" or message == "6\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    userToBlock = raw_input("Mention user to be blocked : ")
                    if len(userToBlock) < 3 or len(userToBlock) >15:
                        userToBlock = "a"
                    s.send("Block".encode("ascii"))
                    msg = s.recv(1024)
                    s.send(userToBlock.encode("ascii"))
                    msg = s.recv(1024)
                    print("Server | %s | %s" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to unblock other blocked user
            elif message == "Unblock\n" or message == "7\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    userToBlock = raw_input("Mention user to unblock : ")
                    if len(userToBlock) < 3 or len(userToBlock) >15:
                        userToBlock = "a"
                    s.send("Unblock".encode("ascii"))
                    msg = s.recv(1024)
                    s.send(userToBlock.encode("ascii"))
                    msg = s.recv(1024)
                    print("Server | %s | %s" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to check when the other user was online last time
            elif message == "Check_User\n" or message == "8\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    userToBlock = raw_input("Mention user you whose last active you want to see : ")
                    if len(userToBlock) < 3 or len(userToBlock) >15:
                        userToBlock = "a"
                    s.send("Check_User".encode("ascii"))
                    msg = s.recv(1024)
                    s.send(userToBlock.encode("ascii"))
                    msg = s.recv(1024)
                    print("Server | %s | %s" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to get list of all online users
            elif message == "Online_Users\n" or message == "5\n":
                s.send("Online_Users".encode("ascii"))
                msg = s.recv(1024)
                s.send("pass".encode("ascii"))
                msg = s.recv(1024)
                print("Server | %s | Online Users are %s\n" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to get list of all his groups
            elif message == "Group_List\n" or message == "16\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    s.send("Group_List".encode("ascii"))
                    msg = s.recv(1024)
                    s.send("pass".encode("ascii"))
                    msg = s.recv(1024)
                    print("Server | %s | List of your Group is %s\n" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to create new group
            elif message == "Create_Group\n" or message == "12\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    createGroup.create(s, username)

            # If the user wants to add new members to a group
            elif message == "Add_Member\n" or message == "13\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    addMember.add(s, username)

            # If the user wants to message to a group
            elif message == "Message_Group\n" or message == "14\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    messageGroup.message(s, username)

            # If the user wants to delete group
            elif message == "Delete_Group\n" or message == "15\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    deleteGroup.deleteGroup(s, username)

            # If the user wants to view members of a group
            elif message == "Group_Members\n" or message == "17\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    groupMembers.getMembers(s, username)

            # If the user wants to leave a group
            elif message == "Leave_Group\n" or message == "18\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    leaveGroup.leave(s, username)

            # If the user wants to broadcast his message
            elif message == "Broadcast\n" or message == "3\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    broadcast.broadcast(s, username)

            # If the user wants to send his message
            elif message == "Message\n" or message == "4\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    personal.personalMessage(s, username)

            # If the user wants to delete his account
            elif message == "Delete_Account\n" or message == "11\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    isDeleted = deleteAccount.Remove(s, username)
                    if isDeleted:
                        s.send("Exit".encode("ascii"))
                        msg = s.recv(1024)
                        s.close()
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((host,(int)(port)))
                        tm = s.recv(1024)
                        print("%s" % (tm.decode('ascii')))
                        Authenticated = False
                        continue

            # If the user wants to update his password
            elif message == "Update_Password\n" or message == "10\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    updatePassword.update(s, username)

            # When user entered an invalid option
            else:
                print("Invalid Option\n")

s.close()


