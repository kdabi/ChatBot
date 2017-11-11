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
print("User OPTIONS are :\n1. Signup, 2. Login, 3. Broadcast, 4. Message, 5. Online_Users, 6. Block, 7. Unblock, 8. Check_User, 9. Logout, 10. Delete_Account, 11. Exit")
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
            if message == "Signup\n":
                if Authenticated:
                    print("Already Loggedin\n")
                elif future > int(time.time()):
                    print("Can't login or signup for %s more seconds.\n" % str(future +1 - int(time.time())))
                else:
                    username, Authenticated = signup.Signup(s)
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

            # If the user chooses Login Option, can't be choose after authenticated
            elif message == "Login\n":
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
            elif message == "Logout\n":
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
            elif message == "Exit\n":
                s.send("Exit".encode("ascii"))
                msg = s.recv(1024)
                s.close()
                exit()

            # If the user wants to block another user
            elif message == "Block\n":
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
            elif message == "Unblock\n":
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
            elif message == "Check_User\n":
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
            elif message == "Online_Users\n":
                s.send("Online_Users".encode("ascii"))
                msg = s.recv(1024)
                s.send("pass".encode("ascii"))
                msg = s.recv(1024)
                print("Server | %s | Online Users are %s\n" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

            # If the user wants to broadcast his message
            elif message == "Broadcast\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    broadcast.broadcast(s, username)

            # If the user wants to send his message
            elif message == "Message\n":
                if not Authenticated:
                    print("First Login  !!!\n")
                else:
                    personal.personalMessage(s, username)

            # If the user wants to delete his account
            elif message == "Delete_Account\n":
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

            # When user entered an invalid option
            else:
                print("Invalid Option\n")

s.close()


