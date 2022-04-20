class Protocol:
	def __init__(self, sender, reciever, typeof, ID=0):
		try:
			int(sender.replace(".", ""))
			self.sender = sender
		except:
			print("Invalid sender")
			self.__del__()
		
		try:
			int(reciever.replace(".", ""))
			self.reciever = reciever
		except:
			print("Invalid reciever")
			self.__del__()
		
		if(typeof and type(typof)==type(str)):
			self.typeof = typeof
		else:
			print("Invalid type")
			self.__del__()
		
		if(ID and type(ID)==type(int))
			self.ID = ID
		else:
			print("Invalid ID")
			self.__del__()
			
		print(typeof+" protocol with ID "+str(ID)+" was created | Sender "+sender+" | Reciever "+reciever)
	
	def get_sender(self):
		return sender
	
	def get_reciever(self):
		return reciever
	
	def __del__(self):
		print(typeof + " protocol with ID " + str(ID) + " was deleted!"


class starttime(Protocol):
	def __init__(self, sender, reciever, starttime, action,ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="starttime", ID=ID)
		
		if(type(starttime)==type(float)):
			self.starttime = starttime
		else:
			try:
				self.starttime = float(starttime)
			except:
				print("invalid datatype for starttime")
				self.__del__()
		
		actions = ["start", "stop"]
		if(type(action)==type(str) and bool([a for a in actions if(a in action)])):
			self.action=action
		else:
			print("Invalid action")
			self.__del__()
		
	def __del__(self):
		super().__del__()

class hs_req(Protocol):
	def __init__(self, sender, reciever, nxt_action,ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="hs_req", ID=ID)
		
		nxt_actions = ["start", "stop"]
		if(type(nxt_action)==type(str) and bool([a for a in nxt_actions if(a in nxt_action)])):
			self.nxt_action=nxt_action
		else:
			print("Invalid nxt_action")
			self.__del__()
		
	def __del__(self):
		super().__del__()

class hs_res(Protocol):
	def __init__(self, sender, reciever, res,ID=0):
		super().__init__(sender=sender, reciever=reciever, res_to, res, typeof="hs_res", ID=ID)
		
		nxt_actions = ["start", "stop"]
		if(type(nxt_action)==type(str) and bool([a for a in nxt_actions if(a in nxt_action)])):
			self.nxt_action=nxt_action
		
	def __del__(self):
		super().__del__()
