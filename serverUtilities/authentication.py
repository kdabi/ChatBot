import os
# Defines the function to authenticate the users

path = os.path.abspath("./database/authenticationDetails.txt")
# taking authentication credentials from the database
with open(path) as f:
    credentials = [x.strip().split(' ') for x in f.readlines()]
f.close()

def authenticate(clientSocket):
    for i in [1,2,3]:
        myUsername = clientSocket.recv(1024).decode('ascii')
        message = "Password"
        clientSocket.send(message.encode('ascii'))
        myPassword = clientSocket.recv(1024).decode('ascii')
        for username, password in credentials:
            if username == myUsername and myPassword == password:
                message = "Authenticated!!"
                clientSocket.send(message.encode('ascii'))
                return username, True
        message = "Authentication Failed!!"
        clientSocket.send(message.encode('ascii'))
    return username, False

