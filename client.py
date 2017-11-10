#client.py
import socket
from time import gmtime, strftime
import sys
import select
import clientUtilities.authentication as authenticate
import clientUtilities.signup as signup
import clientUtilities.broadcast as broadcast
import clientUtilities.message as personal
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
print("User OPTIONS are :\n1. Signup, 2. Login, 3. Broadcast, 4. Message, 5. Online_Users, 6. Logout, 7. Exit")
Authenticated = False
wait = 0
future = round(time.time() ,3)

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
                elif future > round(time.time(), 3):
                    print("Can't login or signup for %s more seconds.\n" % str(round(future, 3) - round(time.time(), 3)))
                else:
                    username, Authenticated = signup.Signup(s)
                    if not Authenticated:
                        if wait == 0:
                            wait = 30
                            future = round(time.time(), 3) + wait
                        else:
                            wait = 2*wait
                            future = round(time.time(), 3) + wait
                        print("Can't login or signup for %s more seconds.\n" % str(wait))
                    else:
                        wait = 0
                        future = round(time.time(), 3)

            # If the user chooses Login Option, can't be choose after authenticated
            elif message == "Login\n":
                if Authenticated:
                    print("Already Loggedin\n")
                elif future > round(time.time(), 3):
                    print("Can't login or signup for %s more seconds.\n" % str(future - round(time.time(),3) ))
                else:
                    username, Authenticated = authenticate.authenticate(s)
                    if not Authenticated:
                        if wait == 0:
                            wait = 30
                            future = round(time.time(), 3) + wait
                        else:
                            wait = 2*wait
                            future = round(time.time(), 3) + wait
                        print("Can't login or signup for %s more seconds.\n" % str(wait))
                    else:
                        wait = 0
                        future = round(time.time(), 3)

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

            # If the user wants to get list of all online users
            elif message == "Online_Users\n":
                s.send("Online_Users".encode("ascii"))
                msg = s.recv(1024)
                s.send("pass".encode("ascii"))
                msg = s.recv(1024)
                print("Server | %s | Online Users are %s" % ( strftime("%d-%m-%Y %H:%M:%S", gmtime()), msg.decode('ascii')))

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

            # When user entered an invalid option
            else:
                print("Invalid Option\n")

s.close()


