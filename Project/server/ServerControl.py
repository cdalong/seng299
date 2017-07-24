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
		self.currentClients = {} #a dictionary of IP:[chatroom name, alias]
		self.chatrooms = {} #dictionary of chatroom name:object
		self.currentaliases = [] #list of current aliases used by the clients
		self.chatrooms['general'] = self.generalChatroom


	# This function returns a chatroom based on its name, and returns None is it doesn't exist.
	def getChatroom(self, chatroomName):

		if chatroomName in self.chatrooms:
			return self.chatrooms.get(chatroomName)
		else:
			return None
	
	# This function sends the completed, formatted message to everyone in the given list of clients.
	def sendmessage(self, message, clients, chatroomname, alias):

		print("sending....")
		print (message)
		for i in clients:
			print("client:     ")
			print(i)

			i.sendall('%s in %s: %s ' % (alias, chatroomname, message))
		return

	# This function returns the alias of a given IP.
	def getUserAlias(self,clientIP):
		return self.currentClients.get(clientIP)
	
	# This function returns true if the user is the admin of the chatroom and false if they aren't.
	def isAdmin(self,clientIP,chatroom):
		if chatroom.name == 'general':
			return False
		elif chatroom.admin == clientIP:
			return True
		else:
			return False
	
	# This function gets a message from a client and sends it if the person is not banned.
	def receivemessage(self, message, clientIP, chatroomName):
		chatroom = self.getChatroom(chatroomName)
		
		self.sendmessage(message, chatroom.currentClients)

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
	def connectuser(self, clientIP, chatroom, client):

		#1. connect to general chat on startup
		#2. try to connect to room if it exists
		#3. if not print a message
		if clientIP not in self.currentClients:
			alias = self.generatealias()
			self.generalChatroom.addUser(client)
			self.currentClients[clientIP] = ['general', alias, client]
			print(alias)
			print (self.currentClients)
			print (self.chatrooms)
			print (self.chatrooms['general'].currentClients)


		elif chatroom in self.chatrooms:

			#remove from old list of users
			currentchatroom = self.chatrooms[self.currentClients[clientIP][0]] #find the chatroom name and remove them
			currentchatroom.removeUser(clientIP)

			#add to new chatroom list of users
			self.currentClients[clientIP][0] = chatroom

			print (self.currentClients)
			print (self.chatrooms)
			print (self.chatrooms['general'].currentClients)
		return

	def disconnectuser(self, clientIP):

		#remove user from chatroom list
		currentchatroomname = self.currentClients[clientIP][0]
		currentchatroomobj = self.chatrooms[currentchatroomname]
		currentchatroomobj.removeUser(clientIP)
		#remove user from current Clients
		self.currentClients.pop(clientIP)

		print("you have been disconnected")
		if len(currentchatroomobj.currentClients) == 0 and currentchatroomname != 'general':
			self.currentClients.pop(currentchatroomname)

	# This creates a new chatroom if the name is not taken and assigns the client who issued the command as the admin.
	def createchatroom(self, clientIP, chatroomName, client):
	
		# This checks if the chatroom name is taken.
		if(self.getChatroom(chatroomName) != None):
			return
		
		newChatroom = Chatroom(clientIP,chatroomName, client)
		self.chatrooms[chatroomName] = newChatroom
		return

	# This deletes a chatroom if it's not General and the client trying to delete it is the admin.
	def deletechatroom(self, clientIP, chatroomName, client):

		chatroom = self.getChatroom(chatroomName)
		if self.isAdmin(clientIP,chatroom):
			self.chatrooms.pop(chatroomName)

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
	def setalias(self,clientIP,newAlias, client):

		#check if not in the master list of aliases
		oldAlias = self.currentClients[clientIP][1]
		
		if newAlias not in self.currentaliases:
			self.currentClients[clientIP][1] = newAlias

			print('New alias %s' % newAlias)

			self.currentaliases.append(newAlias)
			self.currentaliases.remove(oldAlias)

			return
		else:
			print("alias is in use!")

	def parseinput(self, message, address, client):

		# I don't want to do a bunch of elifs
		command = ''
		if message.startswith('/'):
			command = message.split(' ', 1)[0]
			print (command)



		else:
			#send message, but need the clientIP
			print("no command found")

			if address not in self.currentClients:
				print "please connect to general first"

			else:
				chatroom = self.getChatroom(self.currentClients[address][0])
				alias = self.currentClients[address][1]
				clientlist = chatroom.currentClients


			self.sendmessage(message, clientlist, chatroom.name, alias)

			return



		options = {
			'/create': self.createchatroom,
			'/delete': self.deletechatroom,
			'/connect': self.connectuser,
			'/set_alias': self.setalias
		}[command](address, message.split(' ',1)[1], client)

		if 'block' in command:
			blocks = {

			'/block' : self.blockuser,
			'/unblock' : self.unblockuser
			}[command](address, message.split(' ', 1)[1], message.split(' ', 1)[2])

		return


	def listen(self):

		print("1")
		while True:
			client, address = self.s.accept()
			print("Found a new connection")

			client.settimeout(60)
			print("spawning a thread")

			thread = threading.Thread(target = self.controlloop, args = (client, address))
			thread.start()
	def controlloop(self, client, address):
		# type: () -> object

		#address[0] = local IP
		#address[1] = socket
		#message = message obviously
		#self.generalChatroom.addUser(client)
		while True:
			print("2")
			sys.stdout.flush()
			message = client.recv(1024)


			print ('%s:%s says >> %s' % (address[0], address[1], message))

			if message is not None:
				self.parseinput(message, address, client)
				print("inside of loop, waiting for input")

			print ("outside of loop")

def main():

	server = ServerControl()
	server.listen()

if __name__ == "__main__":
	main()
