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

    socket = socket.socket()

    host = socket.gethostname()

    port = 9999

    address = (host, port)

    socket.bind(address)

    socket.listen(5)

    def __init__(self, currentClientIPs, currentClientAliases, chatroomNames):
        #return objects with no populated lists

        self.currentClientIPs = []
        self.currentClientAliases = []
        self.chatroomNames = []

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


    def controlloop(self):

        while True:
            client, address = socket.accept()
            message = client.recv(1024)
            print ('%s:%s says >> %s' % (address[0], address[1], message))
