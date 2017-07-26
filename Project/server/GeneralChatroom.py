class GeneralChatroom:
	
	def __init__(self):

		self.name = 'general'
		# This is a list of sockets that are in the chatroom.
		self.currentClients = []
		
	def addUser(self, userSocket):
		self.currentClients.append(userSocket)
		
	def removeUser(self, userSocket):
		if userSocket in self.currentClients:
			del self.currentClients[userSocket]
