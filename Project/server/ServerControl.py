# Sever Control.py
#SENG 299
#Chatroom project


#The server will be the central data structure for the chatroom porject
import socket


class ServerControl(object):
    '''
    It controls the sending of messages and construction of new chat rooms

    Will also keep a list of connected clients and their relative information
    Attributes:

        currentClientIPs
        currentClientAliases
        chatroomNames

    '''
    #this could be moved to the class atrributes set bu the user



    def __init__(self):
        #return objects with no populated lists

        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        address = (host, port)
        s.bind(address)
        s.listen(5)

        self.currentClientIPs = []
        self.currentClientAliases = []
        self.chatroomNames = ['general']
        
        self.controlloop(s)

    def sendmessage(self, message, clientIP, chatroomName):
        print("sendmeassage")

    def receivemessage(self, message, clientIP, chatroomName):
        print("receivemessage")

    def connectuser(self, clientIP):
        print("connect")

    def disconnectuser(self, clientIP):
        print("disconnect")

    def createchatroom(self, clientIP, chatroomName):
        print("createchatroom")

    def deletechatroom(self, clientIP, chatroomName):
        print("deletechatroom")

    def blockuser(self, clientIP, chatroomName, bannedIP):

        print("blockuser")

    def unblockuser(self, clientIP, chatroomName, bannedIP):

        print("unblockuser")

    def parseinput(self, message, address):


        options = {
            "/block" : self.blockuser(address[0], "test", address[0]),
            "/create" : self.createchatroom,
            "/unblock" : self.unblockuser,
            "/delete" : self.deletechatroom
        }

        if message.startswith('/'):
            command = message.split(' ', 1)[0]

            options[command]

        else:
            #send message, but need the clientIP and shit
            print("no command found")
            self.sendmessage(message)

    def controlloop(self, s):
        # type: () -> object

        #address[0] = local IP
        #address[1] = socket
        #message = message obviously

        while True:
            client, address = s.accept()
            message = client.recv(1024)
            print ('%s:%s says >> %s' % (address[0], address[1], message))

            if message is not None:
                self.parseinput(message, address)
            message = None
            address = None


def main():

    server = ServerControl()

if __name__ == "__main__":
    main()