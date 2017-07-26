# Sever Control.py
#SENG 299
#Chatroom project


#The server will be the central data structure for the chatroom porject
import socket, urllib2, random, sys, threading
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
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = urllib2.urlopen(word_site)
	txt = response.read()
	WORDS = txt.splitlines()
	
	def __init__(self):
		#return objects with no populated lists
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.port = 9999
		self.address = (self.host, self.port)
		self.s.bind(self.address)
		self.s.listen(20)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.generalChatroom = GeneralChatroom()
		self.currentClients = {} #a dictionary of ClientSocket:[chatroom name, alias]
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
	def sendmessage(self, message, clients, chatroomname, alias):

		print("sending....")
		print (message)
		for i in clients:
			print("client:     ")
			print(i)

			i.sendall('%s in %s: %s' % (alias, chatroomname, message))
		return

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
		
	def connectuser(self, clientSocket, chatroomName):

		#1. connect to general chat on startup
		#2. try to connect to room if it exists
		#3. if not print a message
		if clientSocket not in self.currentClients:
			alias = self.generatealias()
			clientSocket.sendall("Your alias is %s. You can change this at any time." % (alias))
			self.generalChatroom.addUser(clientSocket)
			self.currentClients[clientSocket] = ['general', alias]
			print(alias)
			print (self.currentClients)
			print (self.chatrooms)
			print (self.chatrooms['general'].currentClients)

		elif self.chatrooms.get_key(chatroomName):

			#remove from old list of users
			oldChatroomName = self.currentClients[clientSocket][0]
			
			oldChatroom = self.getChatroom(oldChatroomName) #find the chatroom name and remove them
			oldChatroom.removeUser(clientSocket)

			#add to new chatroom list of users
			newChatroom = self.getChatroom(chatroomName)
			self.currentClients[clientSocket][0] = chatroomName
			newChatroom.addUser(clientSocket)
			
			print (self.currentClients)
			print (self.chatrooms)
			print (self.chatrooms['general'].currentClients)
			
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
	def createchatroom(self, clientSocket, chatroomName):
	
		# This checks if the chatroom name is taken.
		if(self.getChatroom(chatroomName) != None):
			clientSocket.sendall("Error: this chatroom name is already taken.")
			return
		
		newChatroom = Chatroom(clientSocket,chatroomName, clientSocket)
		self.chatrooms[chatroomName] = newChatroom
		self.connectuser(clientSocket,chatroomName)
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
	def blockuser(self, clientSocket, bannedAlias):
	
		bannedSocket = None
		for i in self.currentClients:
			if i[1] == bannedAlias:
				bannedSocket = i
				break
		if bannedSocket == None:
			clientSocket.sendall('Error: alias not found.')
			return
	
		chatroomName = self.currentClients[clientSocket][0]
		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientSocket,chatroom) and clientSocket != bannedSocket:
			chatroom.blockUser(bannedSocket)
			chatroom.disconnectuser(bannedSocket)
			chatroom.connectuser(bannedSocket,'general')
			bannedSocket.sendall('You have been banned from %s' % (chatroomName))
			clientSocket.sendall('You have banned %s from %s' % (bannedAlias,chatroomName))
		
		else:
			clientSocket.sendall('Error: you cannot ban this user.')
		return

	# This unblocks a user if it's not General and the admin is trying to unblock someone.
	def unblockuser(self, clientSocket, bannedAlias):
	
		bannedSocket = None
		for i in self.currentClients:
			if i[1] == bannedAlias:
				bannedSocket = i
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
	def setalias(self,clientSocket,newAlias):

		#check if not in the master list of aliases
		oldAlias = self.currentClients[clientSocket][1]
		
		if newAlias not in self.currentaliases:
		
			self.currentClients[clientSocket][1] = newAlias
			clientSocket.sendall('New alias: %s' % newAlias)
			self.currentaliases.append(newAlias)
			self.currentaliases.remove(oldAlias)
			
		else:
			clientSocket.sendall("Alias is currently in use!")
		return

	def parseinput(self, message, address, clientSocket):

		matchobj = re.match('/\[(.+)\] \[(.+)\]',message)
		
		if matchobj is None:
			
			currentChatroomName = self.currentClients[clientSocket][0]
			currentChatroomObj = self.getChatroom(currentChatroomName)
			
			if currentChatroomName == 'general' or clientSocket not in currentChatroomObj.blockedUsers:	
				self.sendMessage(message,currentChatroomObj.CurrentClients)
			
			return
			
		else:
			function, parameter = matchobj.groups()
			if function == 'join':
				self.connectuser(clientSocket,parameter)
			elif function == 'create':
				self.createchatroom(clientSocket,parameter)
			elif function == 'set_alias':
				self.setalias(clientSocket,parameter)
			elif function == 'block':
				self.block(clientSocket,parameter)
			elif function == 'unblock':
				self.unblock(clientSocket,parameter)
			elif function == 'delete':
				self.deletechatroom(clientSocket,parameter)
			else:
				clientSocket.sendall("Error: incorrect command.")
			return


	def listen(self):

		print("1")
		while True:
		
			# client = socket
			# address = (IP,port)
			clientSocket, clientAddress = self.s.accept()
			print("Found a new connection")

			clientSocket.settimeout(60)
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
			print("2")
			sys.stdout.flush()
			message = client.recv(1024)

			print ('%s:%s says >> %s' % (clientAddress[0], clientAddress[1], message))

			if message is not None:
				self.parseinput(message, clientAddress, clientSocket)
				print("inside of loop, waiting for input")

			print ("outside of loop")

def main():

	server = ServerControl()
	server.listen()

if __name__ == "__main__":
	main()
