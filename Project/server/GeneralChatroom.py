class GeneralChatroom:
	
	def __init__(self):	
		self.currentClients = {}
		self.name = 'general'
		return
	
	def sendMessage(self,message):
		MessageList = self.currentClients.keys()
		return message + MessageList
	
	def receiveMessage(self,message,ClientIP):
		alias = self.currentClients[ClientIP]
		outputMessage = alias + ": " + message
		return outputMessage
	
	def addUser(self,ip,alias):
		self.currentClients[ip] = alias
		return
	
	def removeUser(self,ip):
		del self.currentClients[ip]
		return
