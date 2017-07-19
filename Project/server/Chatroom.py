#import random # <-- 3.6 Only
from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):

	def __init__(self, adminAddr, chatroomName):
		GeneralChatroom.__init__(self)
		self.name = chatroomName
		self.admin = adminAddr
		self.currentClients.append(adminAddr)
		self.blockedUsers = []
		
	def addUser(self, userAddr):
		if userAddr not in self.blockedUsers:
			GeneralChatroom.addUser(self, userAddr)
		
	def removeUser(self, userAddr):
		
		GeneralChatroom.removeUser(self, userAddr)
		
		if userAddr == self.admin:
			if len(self.currentClients) != 0:
				self.admin = self.currentClients[0] #<-- Python 2.7
			else:
				self.admin = None
		
	def blockUser(self, userAddr, blkrAddr):
		
		if blkrAddr == self.admin:
			if userAddr in self.currentClients:
				self.blockedUsers[userAddr] = self.currentClients[userAddr]
				
	def unblockUser(self, userAddr, unblkrAddr):
		
		if unblkrAddr == self.admin:
			if userAddr in self.blockedUsers:
				del self.blockedUsers[userAddr]
