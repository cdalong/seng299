# Client.py
# SENG 299 chatroom project

from socket import gethostname, gethostbyname
import ServerControl.py

class Client():
	def __init__(self):
		##
		## instance of Client stores info:
		##		ip - user's IP address
		##		alias - user's current alias
		## when new Client first created, by default they are assigned an alias of a random alphanumeric string
		##
		self.ip = gethostbyname(gethostname())
		self.alias = os.urandom(16)

	#def changeAlias(newAlias):     - update user alias

	def sendMessage(message):
		print('send message')
		ServerControl.receiveMessage(ServerControl, message, ip, chatroomID)

	def receiveMessage(message):
		print('receive message')
		ServerControl.sendMessage(ServerControl, message, ip, chatroomID)

	def connect(chatroom):
		connectUser(ServerControl, ip, chatroom)

	def disconnect():
		disconnectUser(ServerControl, ip)
