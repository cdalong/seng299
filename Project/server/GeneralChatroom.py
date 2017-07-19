class GeneralChatroom:
	
	def __init__(self):

		self.name = 'general'
		self.currentClients = []
		
	def addUser(self, userAddr):
		self.currentClients.append(userAddr)
		
	def removeUser(self, userAddr):
		if userAddr in self.currentClients:
			del self.currentClients[userAddr]

