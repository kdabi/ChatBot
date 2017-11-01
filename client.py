#client.py
import socket, time
import sys
import select

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

print("SERVER: %s" % tm.decode('ascii'))

# following section do the authentication part
username = raw_input("Enter the Username: ")
password = raw_input("Enter the password: ")

s.send(username.encode('ascii'))
ack = s.recv(1024)
s.send(password.encode('ascii'))
ack = s.recv(1024)
print("SERVER: %s" % ack.decode('ascii'))
if ack == "Authentication Failed!!":
    s.close()
    exit()

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
            if not message == "Broadcast\n":
                print("Invalid Option")
                continue
            s.send("Broadcast".encode('ascii'))
            print("%s: %s" % (username, message))
            msg = s.recv(1024)
            print("%s" % msg.decode('ascii'))
            message = raw_input("give message - ")
            s.send(message.encode('ascii'))
            print("%s: %s" % (username, message))


s.close()


