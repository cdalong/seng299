# Sever Control.py
#SENG 299
#Chatroom project


#The server will be the central data structure for the chatroom porject
import socket
from GeneralChatroom import GeneralChatroom
from Chatroom import Chatroom

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
    general = GeneralChatroom()

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
        #TODO make a list of objects
        #Move to a list of Objects
        
        self.controlloop(s)

    def sendmessage(self, message, clientIP, chatroomName):
        #receive message with no command
        #find the chatroom that the IP is associated with
        #send the message to the IPs in the room
        print("sendmessage")

    def receivemessage(self, message, clientIP, chatroomName):
        print("receivemessage")

    def connectuser(self, clientIP, chatroomName):

        #1. connect to general chat on startup
        #2. try to connect to room if it exists
        #3. if not print a message

        if chatroomName == 'general':
            self.general.CurrentClients.append(clientIP)
            print("added to general")
        elif chatroomName in self.chatroomNames:
             # add the chatroom
            print("added to something other than general")
        else:
            print("please create a new chatroom with /create")


        print("connect")

    def disconnectuser(self, clientIP):
        print("disconnect")

    def createchatroom(self, clientIP, chatroomName):
        print("createchatroom")

    def deletechatroom(self, clientIP, chatroomName):
        #create chatroom
        #deletechatroom
        #
        print("deletechatroom")

    def blockuser(self, clientIP, chatroomName, bannedIP):

        print("why are you blocking users")

    def unblockuser(self, clientIP, chatroomName, bannedIP):

        print("unblockuser")

    def parseinput(self, message, address):


        # I don't want to do a bunch of elifs

        if message.startswith('/'):
            command = message.split(' ', 1)[0]
            print (command)

        else:
            #send message, but need the clientIP and shit
            print("no command found")
            self.sendmessage(message)
            return

        options = {
            '/create': self.createchatroom,
            '/delete': self.deletechatroom,
            '/connect': self.connectuser
        }[command](address[0], message.split(' ',1)[1])

        if command.contains('block'):
            blocks = {

            '/block' : self.blockuser,
            '/unblock' : self.unblockuser
            }[command](address[0], message.split(' ', 1)[1], message.split(' ', 1)[2])

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