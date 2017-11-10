import os
# Defines the function to authenticate the users

path = os.path.abspath("./database/authenticationDetails.txt")
# taking authentication credentials from the database
with open(path) as f:
    credentials = [x.strip().split(' ') for x in f.readlines()]
f.close()

def checkLength(string):
    if len(string) >= 3 and len(string) <= 15:
        return True
    else:
        return False

def isValid(string):
    if ' ' in  string or '\t' in string:
        return False
    else:
        return True

def Signup(clientSocket):
    myUsername = clientSocket.recv(1024).decode('ascii')

    if not checkLength(myUsername):
        message = "Username must be of length 3-15. SIGNUP FAILED!!"
        clientSocket.send(message.encode('ascii'))
        return myUsername, False

    if not isValid(myUsername):
        message = "Username must not contain spaces, tabs or newlines. SIGNUP FAILED!!"
        clientSocket.send(message.encode('ascii'))
        return myUsername, False

    for username, password in credentials:
        if username == myUsername:
            message = "Username already exits. SIGNUP FAILED!!"
            clientSocket.send(message.encode('ascii'))
            return myUsername, False

    message = "Password"
    clientSocket.send(message.encode('ascii'))
    myPassword = clientSocket.recv(1024).decode('ascii')

    if not checkLength(myPassword):
        message = "Password must be of length 3-15. SIGNUP FAILED!!"
        clientSocket.send(message.encode('ascii'))
        return myUsername, False

    if not isValid(myUsername):
        message = "Password must not contain spaces, tabs or newlines. SIGNUP FAILED!!"
        clientSocket.send(message.encode('ascii'))
        return myUsername, False

    message = "Authenticated!!"
    clientSocket.send(message.encode('ascii'))
    f = open(path, 'a')
    f.write(myUsername + " " + myPassword + "\n")
    f.close()
    f = open("./database/"+ myUsername + ".txt", 'w')
    f.close()
    return myUsername, True
