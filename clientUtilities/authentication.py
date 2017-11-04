import socket
from time import gmtime, strftime

# following section do the authentication part
def authenticate(s):
    s.send("Login".encode('ascii'))
    msg = s.recv(1024)
    Authenticated = False
    for i in [1,2,3]:
        print("SERVER: | %s | %s Login Attempts Left \n" %( strftime("%d-%m-%Y %H:%M:%S", gmtime()), str(4 - i)))
        username = raw_input("Enter the Username: ")
        password = raw_input("Enter the password: ")
        s.send(username.encode('ascii'))
        ack = s.recv(1024)
        s.send(password.encode('ascii'))
        ack = s.recv(1024)
        print("SERVER: %s\n" % ack.decode('ascii'))
        if ack == "Authenticated!!":
            Authenticated = True
            break
    return (username, Authenticated)

