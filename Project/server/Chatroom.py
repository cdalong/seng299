from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):

	def __init__(self,AdminIP,ChatroomName):
		GeneralChatroom.__init__(self)
		self.AdminIP = AdminIP
		self.ChatroomName = ChatroomName
		self.blockedClients = {}
	
	def addUser(self,ip,alias):
		if self.blockedClients.has_key(ip) is False:
			self.currentClients[ip] = alias
		return
	
	def blockUser(self,alias):
		ip = None
		for i in self.currentClients:
			if self.currentClients[i] == alias:
				ip = i
		if ip == self.AdminIP:
			return
		self.blockedClients[ip] = alias
		self.removeUser(ip)
		return
	
	def unblockUser(self,alias):
		ip = None
		for i in self.blockedClients:
			if self.blockedClients[i] == alias:
				ip = i
		del self.blockedClients[ip]
		return
	
	def removeUser(self,ip):
		GeneralChatroom.removeUser(self,ip)
		if len(self.currentClients) == 0:
			self.deleteChatroom(ip)
			return
		if ip == self.AdminIP:
			self.AdminIP = self.currentClients.keys()[0]
		return
	
	def deleteChatroom(self,DeleterIP):
		if DeleterIP is not self.AdminIP:
			return
		else:
			del self.currentClients
