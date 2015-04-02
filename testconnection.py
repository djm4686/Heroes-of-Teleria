import socket,ast
import sys
class Header:
    def __init__(self, clientID, reqtype):
        self.clientID = clientID
        self.reqtype = reqtype
    def getClientID(self):
        return self.clientID
    def getReqType(self):
        return self.reqtype
    def toString(self):
        return "{\"clientID\" : \"" + str(self.clientID) + "\", \"reqtype\" : \"" + self.reqtype + "\"}"
class DataFrame:
    def __init__(self, header, d):
        self.dict = d
        self.header = header
    def toString(self):
        string = "{"
        for key in self.dict:
            string += "\"" + str(key) + "\" : \"" + str(self.dict[key]) + "\","
        string = string[0:-1]
        string += "}"
        return "{\"header\" : " + self.header.toString() + ", \"data\" : " + string + "}"
HOST, PORT = "localhost", 9999
data = DataFrame(Header(1, "registerAccount"), {"name" : "guthran", "password" : "add8487ec4"}).toString()

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()
    pass
print received
for x in received:
    pass
