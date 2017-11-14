import socket
import getpass
from time import gmtime, strftime

# following section do the authentication part
def Signup(s):
    s.send("Signup".encode('ascii'))
    msg = s.recv(1024)
    Authenticated = False
    print("SERVER: | %s | Username and Password should be of length 3 - 15 and should not contain spaces or newline characters\n" %( strftime("%d-%m-%Y %H:%M:%S", gmtime())))
    username = raw_input("Username: ")
    if len(username) == 0 :
        username = "-"
    s.send(username.encode('ascii'))
    ack = s.recv(1024)
    if not ack.decode('ascii') == "Password":
        print("SERVER: | %s | %s\n" %( strftime("%d-%m-%Y %H:%M:%S", gmtime()), ack.decode('ascii')))
        return (username, Authenticated)
    else:
        password = getpass.getpass()
        if len(password) == 0 :
            password = "-"
        s.send(password.encode('ascii'))
        ack = s.recv(1024)
        if not ack == "Authenticated!!":
            print("SERVER: %s\n" %  ack.decode('ascii'))
        else:
            print("SERVER: User %s created. Logged In !!\n" % username)
            Authenticated = True
    return (username, Authenticated)

