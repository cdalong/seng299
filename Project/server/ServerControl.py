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


	
	def __init__(self):
		#return objects with no populated lists
		s = socket.socket()
		host = socket.gethostname()
		port = 9999
		address = (host, port)
		s.bind(address)
		s.listen(5)

		self.generalChatroom = GeneralChatroom()
		self.currentClients = {}
		self.chatrooms = []

		self.controlloop(s)
	
	# This function returns a chatroom based on its name, and returns None is it doesn't exist.
	def getChatroom(self, chatroomName):
		if chatroomName == 'general':
			return self.generalChatroom
		else:
			for i in self.chatrooms:
				if self.chatrooms[i].chatroomName == chatroomName:
					return self.chatrooms[i]
			return None
	
	# This function sends the completed, formatted message to everyone in the given list of clients.
	def sendmessage(self, message, clients):
		for i in clients:
			clients[i].receiveMessage(message)
		return

	# This function returns the alias of a given IP.
	def getUserAlias(self,clientIP):
		return self.currentClients[clientIP]
	
	# This function returns true if the user is the admin of the chatroom and false if they aren't.
	def isAdmin(self,clientIP,chatroom):
		if chatroom.chatroomName == 'general':
			return False
		elif chatroom.adminIP == clientIP:
			return True
		else:
			return False
	
	# This function gets a message from a client and sends it if the person is not banned.
	def receivemessage(self, message, clientIP, chatroomName):
		chatroom = self.getChatroom(chatroomName)
		
		self.sendmessage(message, chatroom.currentClients)

	# This puts a client within a chatroom if they are not banned.
	def connectuser(self, clientIP, chatroom):

		#1. connect to general chat on startup
		#2. try to connect to room if it exists
		#3. if not print a message

		# This part needs work
		if chatroom == 'general':
			self.generalChatroom.addUser(clientIP)
		elif chatroom in self.chatroomNames:
			chatroom.addUser(clientIP)
		return

	def disconnectuser(self, clientIP):
		print("disconnect")

	# This creates a new chatroom if the name is not taken and assigns the client who issued the command as the admin.
	def createchatroom(self, clientIP, chatroomName):
	
		# This checks if the chatroom name is taken.
		if(self.getChatroom(chatroomName) != None):
			return
		
		newChatroom = Chatroom(clientIP,chatroomName)
		self.chatrooms.append(newChatroom)
		return

	# This deletes a chatroom if it's not General and the client trying to delete it is the admin.
	def deletechatroom(self, clientIP, chatroomName):
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientIP,chatroom):
			self.currentClients.remove(chatroom)

	# This blocks a user from a chatroom if it's not General, the admin is trying to ban someone and they are not bannign themselves.
	def blockuser(self, clientIP, chatroomName, bannedIP):
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientIP,chatroom) and clientIP != bannedIP:
			chatroom.blockUser(bannedIP)
		return

	# This unblocks a user if it's not General and the admin is trying to unblock someone.
	def unblockuser(self, clientIP, chatroomName, bannedIP):
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientIP,chatroom):
			chatroom.unblockUser(bannedIP)
		return

	# This sets a client's alias
	def setalias(self,clientIP,newAlias):
		self.currentClients[clientIP] = newAlias
		return

	def parseinput(self, message, address):

		# I don't want to do a bunch of elifs

		if message.startswith('/'):
			command = message.split(' ', 1)[0]
			print (command)

		else:
			#send message, but need the clientIP
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
