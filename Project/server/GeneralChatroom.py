class GeneralChatroom:
	
	currentClients = []
	chatroomName = ''
	
	def __init__(self):
		chatroomName = 'general'
		return
	
	def addUser(self,ip):
		self.currentClients.append(ip)
		return
	
	def removeUser(self,ip):
		if ip in self.currentClients:
			self.currentClients.remove(ip)
		return
