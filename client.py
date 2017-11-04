#client.py
import socket
from time import gmtime, strftime
import sys
import select
import clientUtilities.authentication as authenticate
import clientUtilities.broadcast as broadcast

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
print("User OPTIONS are :\n1. Login, 2. Broadcast, 3. Exit")
Authenticated = False

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

            # If the user chooses Login Option, can't be choose after authenticated
            if message == "Login\n":
                if Authenticated:
                    print("Already Loggedin\n")
                else:
                    username, Authenticated = authenticate.authenticate(s)
                if not Authenticated:
                    s.close()
                    exit()
                continue

            # If the user wants to exit
            elif message == "Exit\n":
                s.send("Exit".encode("ascii"))
                msg = s.recv(1024)
                s.close()
                exit()

            # If the user wants to broadcast his message
            elif message == "Broadcast\n":
                if not Authenticated:
                    print("First Login  !!!")
                else:
                    broadcast.broadcast(s, username)

            # When user entered an invalid option
            else:
                print("Invalid Option\n")

s.close()


