#import random # <-- 3.6 Only
from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):

	def __init__(self, adminSocket, chatroomName):
		GeneralChatroom.__init__(self)
		self.name = chatroomName
		self.admin = adminSocket
		self.currentClients.append(adminSocket)
		self.blockedUsers = []
		
	def addUser(self, userSocket):
		if userSocket not in self.blockedUsers:
			GeneralChatroom.addUser(self, userSocket)
		
	def removeUser(self, userSocket):
		
		GeneralChatroom.removeUser(self, userSocket)
		
		if userSocket == self.admin:
			if len(self.currentClients) != 0:
				self.admin = self.currentClients[0]
			else:
				self.admin = None
		
	def blockUser(self, userSocket, blkrSocket):
		
		if blkrSocket == self.admin and if userSocket in self.currentClients:
			if userSocket in self.currentClients:
				self.currentClients.remove(userSocket)
			self.blockedUsers.append(userSocket)
				
	def unblockUser(self, userSocket, unblkrSocket):
		if unblkrSocket == self.admin and if userSocket in self.blockedUsers:
			self.blockedUsers.remove(userSocket)
