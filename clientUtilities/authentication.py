import socket
import getpass
from time import gmtime, strftime

# following section do the authentication part
def authenticate(s):
    s.send("Login".encode('ascii'))
    msg = s.recv(1024)
    Authenticated = False
    for i in [1,2,3]:
        print("SERVER: | %s | %s Login Attempts Left \n" %( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(4 - i)))
        username = raw_input("Username: ")
        if len(username) < 3 or len(username) > 15:
            username = "a"
        password = getpass.getpass()
        if len(password) < 3 or len(password) > 15:
            password = "a"
        s.send(username.encode('ascii'))
        ack = s.recv(1024)
        s.send(password.encode('ascii'))
        ack = s.recv(1024)
        print("SERVER: %s\n" % ack.decode('ascii'))
        if ack == "Authenticated!!":
            Authenticated = True
            break
    return (username, Authenticated)

