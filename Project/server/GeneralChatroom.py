class GeneralChatroom:
	
	def __init__(self):

		self.name = 'general'
		self.curntUsers = []
		
	def Add_User(self, userAddr):
		self.curntUsers.append(userAddr)
		
	def Remove_User(self, userAddr):
		if userAddr in self.curntUsers:
			del self.curntUsers[userAddr]

