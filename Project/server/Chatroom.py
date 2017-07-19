#import random # <-- 3.6 Only
from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):

	def __init__(self, adminAddr, chatroomName):
		GeneralChatroom.__init__(self)
		self.name = chatroomName
		self.admin = adminAddr
		self.curntUsers.append(adminAddr)
		self.blockedUsers = []
		
	def Add_User(self, userAddr):
		if userAddr not in self.blockedUsers:
			GeneralChatroom.Add_User(self, userAddr)
		
	def Remove_User(self, userAddr):
		
		GeneralChatroom.Remove_User(self, userAddr)
		
		if userAddr == self.admin:
			if len(self.curntUsers) != 0:
				self.admin = self.curntUsers[0] #<-- Python 2.7
			else:
				self.admin = None
		
	def Block_User(self, userAddr, blkrAddr):
		
		if blkrAddr == self.admin:
			if userAddr in self.curntUsers:
				self.blockedUsers[userAddr] = self.curntUsers[userAddr]
				
	def Unblock_User(self, userAddr, unblkrAddr):
		
		if unblkrAddr == self.admin:
			if userAddr in self.blockedUsers:
				del self.blockedUsers[userAddr]

