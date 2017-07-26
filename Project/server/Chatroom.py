#import random # <-- 3.6 Only
from GeneralChatroom import GeneralChatroom

class Chatroom(GeneralChatroom):

	def __init__(self, adminSocket, chatroomName, clientSocket):
		GeneralChatroom.__init__(self)
		self.name = chatroomName
		self.adminSocket = adminSocket
		self.currentClients.append(clientSocket)
		# This is a list of banned sockets.
		self.blockedUsers = []
		
	def addUser(self, userSocket):
		if userSocket not in self.blockedUsers:
			GeneralChatroom.addUser(self, userSocket)
		
	def removeUser(self, userSocket):
		
		GeneralChatroom.removeUser(self, userSocket)
		
		if userSocket == self.adminSocket:
			if len(self.currentClients) != 0:
				self.admin = self.currentClients[0] #<-- Python 2.7
			else:
				self.admin = None
		
	def blockUser(self, userSocket, blkrSocket):
		
		if blkrSocket == self.adminSocket:
			if userSocket in self.currentClients:
				self.blockedUsers[userSocket] = self.currentClients[userSocket]
				
	def unblockUser(self, userSocket, unblkrSocket):
		
		if unblkrSocket == self.adminSocket:
			if userSocket in self.blockedUsers:
				del self.blockedUsers[userSocket]
