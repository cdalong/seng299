# Client.py
# SENG 299 chatroom project

import sys, socket
from ServerControl import disconnectuser, connectuser, generatealias

class Client():
	def __init__(self):
		##
		## instance of Client stores info:
		##		ip - user's IP address
		##		alias - user's current alias
		## when new Client first created, by default they are assigned an alias of a random alphanumeric string
		##
		self.ip = gethostbyname(gethostname())
		#self.alias = os.urandom(16)
		self.alias = generatealias(ServerControl)
		self.port = random.randint(5000, 90000)
		self.host = gethostname()
		self.chatroomID = 'general'
		
	server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_conn.connect((server_conn.gethostname(), random.randint(5000, 90000)))

	list_sockets = [sys.stdin, server_conn]

	def changeAlias(self,newAlias):     
		self.alias = newAlias

	def updateChatroom(self,chatroomName)
		self.chatroomID = chatroomName

	## listen to receive messages
	while True:
		read_sockets, write_sockets, error_sockets = select.select(list_sockets, [], [])
		for sock in read_sockets:
			if sock is server_conn:
				msg = sock.recv()
				print(msg)
		for wr in write_sockets:
			server_conn.sendall(sys.stdin.readline())

	def connect(self,chatroom):
		connectuser(ServerControl, self.ip, chatroom)

	def disconnect(self):
		disconnectuser(ServerControl, self.ip)
		sys.exit()
