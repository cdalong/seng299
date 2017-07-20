# Sever Control.py
#SENG 299
#Chatroom project


#The server will be the central data structure for the chatroom porject
import socket, urllib2, random
from GeneralChatroom import GeneralChatroom
from Chatroom import Chatroom
import re

class ServerControl(object):
	'''
	It controls the sending of messages and construction of new chat rooms
	Will also keep a list of connected clients and their relative information
	Attributes:
		currentClients
		currentAliases
		chatrooms
	'''
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = urllib2.urlopen(word_site)
	txt = response.read()
	WORDS = txt.splitlines()
	
	def __init__(self):
		#return objects with no populated lists
		s = socket.socket()
		host = socket.gethostname()
		port = 9999
		address = (host, port)
		s.bind(address)
		s.listen(5)
		
		#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.generalChatroom = GeneralChatroom()
		self.currentClients = {} #a dictionary of socket:[chatroom name, alias]
		self.chatrooms = {}#dictionary of chatroom name:chatroom object
		self.currentAliases = [] #list of current aliases used by the clients
		self.chatrooms['general'] = self.GeneralChatroom()
		self.controlloop(s)

	# This function returns a chatroom based on its name, and returns None is it doesn't exist.
	def getChatroom(self, chatroomName):

		if chatroomName in self.chatrooms:
			return self.chatrooms[chatroomName]
		else:
			return None
	
	# This function sends the completed, formatted message to everyone in the given list of clients.
	def sendmessage(self, message, clientList):
			
		for i in clientList:
			s.send(message)
		return

	# This function returns the alias of a given IP.
	def getUserAlias(self,clientSocket):
		return self.currentClients[clientSocket][1]
	
	# This function returns true if the user is the admin of the chatroom and false if they aren't.
	def isAdmin(self,clientSocket,chatroom):
		if chatroom.chatroomName == 'general':
			return False
		elif chatroom.adminSocket == clientSocket:
			return True
		else:
			return False
	
	# This function gets a message from a client and sends it if the person is not banned.
	'''def receivemessage(self, message, clientSocket, chatroomName):
		chatroom = self.getChatroom(chatroomName)
		
		self.sendmessage(message, chatroom.currentClients)
	'''
	# This puts a client within a chatroom if they are not banned.

	def generatealias(self):

		alias = random.choice(self.WORDS)
		flag = False

		while not flag:

			if alias not in self.currentAliases:
				self.currentAliases.append(alias)
				flag = True
			else:
				alias = random.choice(self.WORDS)

		return alias
		
	def connectuser(self, clientSocket, chatroomName):

		#1. connect to general chat on startup
		#2. try to connect to room if it exists
		chatroom = self.getChatroom(chatroomName)

		if clientSocket not in self.currentClients:
			alias = self.generatealias()
			generalChatroom = self.getChatroom('general')
			generalChatroom.addUser(clientSocket)
			self.currentClients[clientSocket] = ['general', alias]

		elif chatroom in self.chatrooms:

			#remove from old list of users
			oldChatroom = self.getChatroom(self.currentClients[clientSocket][0]) #find the chatroom name and remove them
			oldChatroom.removeUser(clientSocket)

			#add to new chatroom list of users
			self.currentClients[clientSocket][0] = chatroomName
			chatroom.addUser(clientSocket)
		
		return

	# Disconnects a user from the server.
	def disconnectuser(self, clientSocket):

		#remove user from chatroom list
		currentChatroomName = self.currentClients[clientSocket][0]
		currentChatroomObj = self.getChatroom(currentChatroomName)
		currentchatroomobj.removeUser(clientSocket)
		#remove user from current Clients
		self.currentClients.pop(clientSocket)
		print(clientSocket + " has been disconnected")
		clientSocket.close()

	# This creates a new chatroom if the name is not taken and assigns the client who issued the command as the admin.
	def createchatroom(self, clientSocket, chatroomName):
	
		# This checks if the chatroom name is taken.
		if(self.getChatroom(chatroomName) != None):
			return
		
		newChatroom = Chatroom(clientSocket,chatroomName)
		self.chatrooms[chatroomName] = newChatroom
		return

	# This deletes a chatroom if it's not General and the client trying to delete it is the admin.
	def deletechatroom(self, clientSocket, chatroomName):

		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientSocket,chatroom):
			self.currentClients.pop(chatroomName)
			for i in self.CurrentClients:
				self.disonnectUser(i)
				self.connectUser(i,'general')

	# This blocks a user from a chatroom if it's not General, the admin is trying to ban someone and they are not bannign themselves.
	def blockuser(self, clientSocket, chatroomName, bannedSocket):
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientSocket,chatroom) and clientSocket != bannedSocket:
			chatroom.blockUser(bannedSocket)
		return

	# This unblocks a user if it's not General and the admin is trying to unblock someone.
	def unblockuser(self, clientSocket, chatroomName, bannedSocket):
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientSocket,chatroom):
			chatroom.unblockUser(bannedSocket)
		return

	# This sets a client's alias
	def setalias(self,clientSocket,newAlias):

		oldAlias = self.currentClients[clientSocket][1]
		#check if not in the master list of aliases
		if newAlias not in self.currentaliases:
			self.currentClients[clientSocket][1] = newAlias
			self.currentAliases.remove(oldAlias)
			self.currentAliases.add(newAlias)


	def parseinput(self, message, clientSocket):

		# I don't want to do a bunch of elifs
		'''
		if message.startswith('/'):
			command = message.split(' ', 1)[0]
			print (command)
			return
		else:
			#send message, but need the clientSocket
			print("no command found")

			if address not in self.currentClients:
				print "please connect to general first"

			else:
				chatroomName = self.getChatroom(self.currentClients[address][0])
				chatroom = self.getChatroom(chatroomName)
				clientlist = chatroom.CurrentClients
				self.sendmessage(message, clientlist)
			return

		options = {
			'/create': self.createchatroom,
			'/delete': self.deletechatroom,
			'/connect': self.connectuser
		}[command](address, message.split(' ',1)[1])

		if 'block' in command:
			blocks = {

			'/block' : self.blockuser,
			'/unblock' : self.unblockuser
			}[command](address, message.split(' ', 1)[1], message.split(' ', 1)[2])
		'''
		matchobj = re.match('/\[(.+)\] \[(.+)\]',message)
		if matchobj is None:

			message = self.getUserAlias(clientSocket) + ': ' + message
			
			currentChatroomName = self.currentClients[clientSocket][0]
			currentChatroomObj = self.getChatroom(currentChatroomName)
			
			if currentChatroomName == 'general' or clientSocket not in currentChatroomObj.blockedUsers:	
				self.sendMessage(message,currentChatroomObj.CurrentClients)
				
		else:
			(function, parameter) = matchobj.groups()
			################## FIND FUNCTION ###############
			return
		
	def controlloop(self, s):
		while True:
			clientSocket, clientAddress = s.accept()
			message = client.recv(1024)
			if message is not None:
				print ('%s:%s says >> %s' % (address[0], address[1], message))
				self.parseinput(message, clientSocket)


def main():

	server = ServerControl()

if __name__ == "__main__":
	main()
