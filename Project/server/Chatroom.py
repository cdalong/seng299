from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):


	def __init__(self,AdminIP,ChatroomName):
		GeneralChatroom.__init__(self)
		self.AdminIP = AdminIP
		self.ChatroomName = ChatroomName
		self.blockedClients = []
	
	def addUser(self,ip):
		if ip not in self.blockedClients:
			self.currentClients.append(ip)
			if len(self.currentClients) == 1:
				self.AdminIP = ip
		return
	
	def blockUser(self,bannedIP):
		self.blockedClients.append(bannedIP)
		self.removeUser(bannedIP)
		return
	
	def unblockUser(self,unbannedIP):
		self.blockedClients.remove(unbannedIP)
		return
	
	def removeUser(self,ip):
		GeneralChatroom.removeUser(self,ip)
		if ip == self.AdminIP and len(self.currentClients) != 0:
			self.AdminIP = self.currentClients[0]
		return
