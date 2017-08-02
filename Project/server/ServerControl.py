# Sever Control.py
# SENG 299
# Chatroom project


#The server will be the central data structure for the chatroom porject
import socket, urllib2, random, sys, threading
from GeneralChatroom import GeneralChatroom
from Chatroom import Chatroom
import re
class ServerControl(object):
	'''
	It controls the sending of messages and construction of new chat rooms
	Will also keep a list of connected clients and their relative information
	Attributes:
		currentClientIPs
		currentClientAliases
		chatroomNames
	'''
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = urllib2.urlopen(word_site)
	txt = response.read()
	WORDS = txt.splitlines()
	
	def __init__(self):
		#return objects with no populated lists
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = 9999 #int(sys.argv[1])
		self.address = (self.host, self.port)
		self.s.bind(self.address)
		self.s.listen(20)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.generalChatroom = GeneralChatroom()

		self.currentClients = {} #a dictionary of ClientAddress:[chatroom name, alias]
		self.chatrooms = {} #dictionary of chatroom name: chatroom object
		self.currentaliases = [] #list of current aliases used by the clients
		self.chatrooms['general'] = self.generalChatroom


	# This function returns a chatroom based on its name, and returns None is it doesn't exist.
	def getChatroom(self, chatroomName):

		if chatroomName in self.chatrooms:
			return self.chatrooms.get(chatroomName)
		else:
			print("Error: chatroom not found.")
			return None
	
	# This function sends the completed, formatted message to everyone in the given list of clients.
	def sendmessage(self, message, chatroomname, alias):
		clients = self.chatrooms[chatroomname].currentClients
		print ('[%s]:[%s] %s' % (chatroomname, alias, message))
		for i in clients:
			i.sendall('[%s]:[%s]: %s ' % (chatroomname, alias, message))
		return
	
	def servermessage(self, message, chatroomname):
		clients = self.chatrooms[chatroomname].currentClients
		print ('[%s]:[Server]: %s ' % (chatroomname, message))
		for i in clients:
			print(i)
			i.sendall('[%s]:[Server]: %s ' % (chatroomname, message))
		return
 		
	def returnmessage(self, message, client):
		client.sendall('\n' + message)

	# This function returns the alias of a given IP.
	def getUserAlias(self,clientSocket):
	
		if self.currentClients.has_key(clientSocket) == False:
			print("Error: invalid clientSocket inputted.")
			return
		
		return self.currentClients.get(clientSocket)
	
	# This function returns true if the user is the admin of the chatroom and false if they aren't.
	def isAdmin(self,clientSocket,chatroom):
		if chatroom.name == 'general':
			return False
		elif chatroom.adminSocket == clientSocket:
			return True
		else:
			return False

	# This puts a client within a chatroom if they are not banned.

	def generatealias(self):

		alias = random.choice(self.WORDS)
		flag = False

		while not flag:

			if alias not in self.currentaliases:
				self.currentaliases.append(alias)
				flag = True
			else:
				alias = random.choice(self.WORDS)

		return alias

	def connectuser(self, clientAddress, chatroomName, clientSocket):


		#1. connect to general chat on startup
		#2. try to connect to room if it exists
		#3. if not print a message
		if clientAddress not in self.currentClients:
			alias = self.generatealias()

			self.generalChatroom.addUser(clientSocket)
			self.currentClients[clientAddress] = ['general', alias, clientSocket]
			
			print ('%s Connected' % (alias))
			self.servermessage(('%s Connected' % (alias)), chatroomName)
			connectionmessage = ('You connected to the general chatroom!\nYour current alias is: %s (Use /set_alias to change it!)' % (alias))
			self.returnmessage(connectionmessage, clientSocket)
			
			#print (self.currentClients)
			#print (self.chatrooms)
			#print (self.chatrooms['general'].currentClients)

		elif chatroomName in self.chatrooms:


			#remove from old list of users
			oldChatroomName = self.currentClients[clientAddress][0]
			
			oldChatroom = self.getChatroom(oldChatroomName) #find the chatroom name and remove them
			oldChatroom.removeUser(clientSocket)

			#add to new chatroom list of users
			newChatroom = self.getChatroom(chatroomName)
			self.currentClients[clientAddress][0] = chatroomName
			newChatroom.addUser(clientSocket)
			
			print (self.currentClients)
			print (self.chatrooms)
			print (self.chatrooms['general'].currentClients)
			self.servermessage("You've joined %s" %(chatroomName), chatroomName)
			
		else:
			clientSocket.sendall("Error: chatroom does not exist.")
		
		return

	# This disconnects a user from the server.
	def disconnectuser(self, clientSocket):

		#remove user from chatroom list
		currentchatroomname = self.currentClients[clientSocket][0]
		currentchatroomobj = self.chatrooms[currentchatroomname]
		currentchatroomobj.removeUser(clientSocket)
		#remove user from current Clients
		self.currentClients.pop(clientSocket)
		clientSocket.sendall("You have been disconnected from the server.")
		clientSocket.close()
		
		if len(currentchatroomobj.currentClients) == 0 and currentchatroomname != 'general':
			self.currentClients.pop(currentchatroomname)

	# This creates a new chatroom if the name is not taken and assigns the client who issued the command as the admin.
	def createchatroom(self, clientAddress, chatroomName, clientSocket):
	
		# This checks if the chatroom name is taken.
		if(self.getChatroom(chatroomName) != None):
			clientSocket.sendall("Error: this chatroom name is already taken.")
			return
		
		newChatroom = Chatroom(clientSocket, chatroomName, clientSocket)
		self.chatrooms[chatroomName] = newChatroom
		self.connectuser(clientAddress, chatroomName, clientSocket)
		return

	# This deletes a chatroom if it's not General and the client trying to delete it is the admin.
	def deletechatroom(self, clientSocket, chatroomName):

		chatroom = self.getChatroom(chatroomName)
		if chatroom == None:
			clientSocket.sendall("Error: chatroom not found.")
			return
		
		if self.isAdmin(clientSocket,chatroom):
			for i in chatroom.currentClients:
				self.connectuser(i)
				i.sendall("You have been moved to general because this chatroom has been deleted.")	
			self.chatrooms.pop(chatroomName)
		else:
			clientSocket.sendall("Error: you cannot delete this chatroom.")
		return

	# This blocks a user from a chatroom if it's not General, the admin is trying to ban someone and they are not bannign themselves.
	def blockuser(self, clientAddress, clientSocket, bannedAlias):
		#there's probably a better way to do this
		bannedSocket = None
		for i in self.currentClients:
			if self.currentClients[i][1] == bannedAlias:
				bannedSocket = self.currentClients[i][2]
				bannedAddress = i
				break
		if bannedSocket == None:
			clientSocket.sendall('Error: alias not found.')
			return
	
		chatroomName = self.currentClients[clientAddress][0]
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientSocket,chatroom) and clientSocket != bannedSocket:
			chatroom.blockUser(bannedSocket)
			chatroom.removeUser(bannedSocket)
			self.connectuser(bannedAddress, 'general', bannedSocket)
			bannedSocket.sendall('You have been banned from %s' % (chatroomName))
			clientSocket.sendall('You have banned %s from %s' % (bannedAlias,chatroomName))
		
		else:
			clientSocket.sendall('Error: you cannot ban this user.')
		return

	# This unblocks a user if it's not General and the admin is trying to unblock someone.
	def unblockuser(self, clientSocket, bannedAlias):

		bannedSocket = None
		for i in self.currentClients:
			if self.currentClients[i][1] == bannedAlias:
				bannedSocket = self.currentClients[i][2]
				bannedAddress = i
				break
		if bannedSocket == None:
			clientSocket.sendall('Error: alias not found.')
			return
	
		chatroomName = self.currentClients[clientSocket][0]
		chatroom = self.getChatroom(chatroomName)
		
		if self.isAdmin(clientSocket,chatroom):
			chatroom.unblockUser(bannedSocket)
			clientSocket.sendall("%s has been unbanned from %s." % (bannedAlias,chatroomName))
			bannedSocket.sendall("You have been unbanned from %s." % (chatroomName))
		
		else:
			clientSocket.sendall("Error: you are not the admin of %s" % (chatroomName))
		return

	# This sets a client's alias

	def setalias(self,clientAddress,newAlias):


		#check if not in the master list of aliases
		oldAlias = self.currentClients[clientAddress][1]
		
		if newAlias not in self.currentaliases:

			self.currentClients[clientAddress][1] = newAlias

			#self.returnmessage(('[Server]: New alias %s' % newAlias), client)
			self.servermessage(('%s Changed Their Alias To: %s' % (oldAlias, newAlias)), self.currentClients[clientAddress][0])

			self.currentaliases.append(newAlias)
			self.currentaliases.remove(oldAlias)
			
		else:
			clientSocket = self.currentClients[clientAddress][2]
			clientSocket.sendall("Alias is currently in use!")
		return

	def parseinput(self, message, clientAddress, clientSocket):


		command = ''
		arguement = ''
		if message.startswith('/'):
			command = message.split(' ', 1)[0]
			print (command)
			arguement = message.split(' ', 1)[1]


		else:
			#send message, but need the clientIP
			print("no command found")

			if clientAddress not in self.currentClients:
				print ("please connect to general first")

			else:
				chatroom = self.getChatroom(self.currentClients[clientAddress][0])
				alias = self.currentClients[clientAddress][1]



				self.sendmessage(message,chatroom.name,alias)

			return


		if command == '/create':
			self.createchatroom(clientAddress, arguement, clientSocket)

		elif command == '/delete':
			self.deletechatroom(clientAddress, arguement, clientSocket)
		elif command == '/connect':
			self.connectuser(clientAddress, arguement, clientSocket)
		elif command == '/set_alias':
			self.setalias(clientAddress, arguement)
		elif command == '/block':
			self.blockuser(clientAddress, clientSocket, arguement)
		elif command == '/unblock':
			self.unblockuser(clientAddress,clientSocket, arguement)



	def listen(self):

		print ('Chat Server is Online...\nConnect on Port %s' % (self.port))
		print ('_' * 80 + '\n')
		
		while True:

			# client = socket
			# address = (IP,port)
			clientSocket, clientAddress = self.s.accept()
			print("Found a new connection")

			clientSocket.settimeout(None)
			print("Spawning a thread")

			thread = threading.Thread(target = self.controlloop, args = (clientSocket, clientAddress))
			thread.start()

	def controlloop(self, clientSocket, clientAddress):
		# type: () -> object

		#address[0] = local IP
		#address[1] = port
		#message = message
		#self.generalChatroom.addUser(client)
		
		while True:
			#print("2")
			sys.stdout.flush()
			message = clientSocket.recv(1024)


			#print ('%s:%s says >> %s' % (address[0], address[1], message))

			if message is not None:
				self.parseinput(message, clientAddress, clientSocket)
				#print("inside of loop, waiting for input")


			#print ("outside of loop")

def main():

	server = ServerControl()
	server.listen()

if __name__ == "__main__":
	main()
