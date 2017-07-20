class GeneralChatroom:
	
	def __init__(self):

		self.name = 'general'
		self.currentClients = []
		
	def addUser(self, userSocket):
		self.currentClients.append(userSocket)
		
	def removeUser(self, userSocket):
		if userAddr in self.currentClients:
			self.currentClients.remove(userSocket)
