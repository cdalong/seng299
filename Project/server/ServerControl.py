# Sever Control.py
#SENG 299
#Chatroom project
#The server will be the central data structure for the chatroom porject
import socket
import urllib2
import random

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
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

    response = urllib2.urlopen(word_site)
    WORDS = response.content.splitlines()
    def __init__(self):
        #return objects with no populated lists
        s = socket.socket()
        host = socket.gethostname()
        port = 9999
        address = (host, port)
        s.bind(address)
        s.listen(5)

        general = GeneralChatroom()

        self.connectedClients = {}
        #make a dictionary
        self.chatrooms = [general]

        #TODO make a list of objects
        #Move to a list of Objects
        
        self.controlloop(s)

    def sendmessage(self, message, clientIP, chatroom):
        #receive message with no command
        #find the chatroom that the IP is associated with
        #send the message to the IPs in the room
        print("sendmessage")

    def receivemessage(self, message, clientIP, chatroom):
        print("receivemessage")

    def connectuser(self, clientIP, chatroom):

        #1. connect to general chat on startup
        #2. try to connect to room if it exists
        #3. if not print a message

        if chatroom == 'general':
            alias = random.choice(self.WORDS.keys())
            self.general.CurrentClients['clientIP'] = alias
            self.connectedClients['clientIP'] = alias

            print("added to general")

        elif chatroom in self.chatrooms:
             # add the chatroom

            self.chatrooms[chatroom].currentClients['clientIP'] = self.connectedClients.get('clientIP')

            print("added to something other than general")
        else:

            print("please create a new chatroom with /create")


        print("connected")

    def disconnectuser(self, clientIP):

        #user sends disconnect commnd
        #remove them from the connected clients list in server
        #find the chatroom they are associated with
        #remove from chatroom

        print("disconnect")

    def createchatroom(self, clientIP, chatroom):

        #create a new chatroom object
        #add to list of chatrooms
        #add calling user as admin
        print("createchatroom")

    def deletechatroom(self, clientIP, chatroom):
        #deletechatroom
        #Receive a delete chatroom message
        #check if admin of the room
        #if so, kick everyone out, back to general
        #remove the room
        print("deletechatroom")

    def blockuser(self, clientIP, chatroom, bannedIP):

        #add the user to the chatroom block list

        print("why are you blocking users")

    def unblockuser(self, clientIP, chatroom, bannedIP):

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

    def setalias(self):
        #todo method stub
        pass


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