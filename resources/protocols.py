class Protocol():
	def __init__(self, sender, reciever, typeof, ID=0):
		try:
			int(sender.replace(".", ""))
			self.sender = sender
		except:
			print("Invalid sender")
			return None
			
		try:
			int(reciever.replace(".", ""))
			self.reciever = reciever
		except:
			print("Invalid reciever")
			return None
		
		if(typeof and type(typeof) == type("")):
			self.typeof = typeof
		else:
			print("Invalid type")
			return None
		
		if(type(ID)==type(1)):
			self.ID = ID
		else:
			print("Invalid ID")
			return None
			
		print(typeof+" protocol with ID "+str(ID)+" was created | Sender "+sender+" | Reciever "+reciever)
	
	def get_sender(self):
		return self.sender
	
	def get_reciever(self):
		return self.reciever
	
	def get_typeof(self):
		return self.typeof
		
	def get_id(self):
		return self.ID
	
	def __del__(self):
		try:
			print(typeof + " protocol with ID " + str(ID) + " was deleted!")
		except:
			print("a protocol was deleted")


class starttime(Protocol):
	def __init__(self, sender, reciever, starttime, action,ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="starttime", ID=ID)
		
		if(type(starttime)==type(1.1)):
			self.starttime = starttime
		else:
			try:
				self.starttime = float(starttime)
			except:
				print("invalid datatype for starttime")
				return None
		
		actions = ["start", "stop"]
		if(type(action)==type("") and bool([a for a in actions if(a in action)])):
			self.action=action
		else:
			print("Invalid action")
			return None
		
	def get_action():
		return action
	
	def get_starttime():
		return starttime
	
	def __del__(self):
		super().__del__()


class hs_req(Protocol):
	def __init__(self, sender, reciever, nxt_action,ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="hs_req", ID=ID)
		
		nxt_actions = ["start", "stop", "establish_conn"]
		for a in nxt_actions:
			if (a==nxt_action):
				self.nxt_action=nxt_action
				break
		else:
			print("Invalid nxt_action")
			return None
	
	def respond(msg):
		if(super().typeof=="establish_conn"):
			return msg
		
	def __del__(self):
		super().__del__()


class hs_res(Protocol):
	def __init__(self, sender, reciever, res_to, res, ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="hs_res", ID=ID)
		
		if(res and type(res)==type(1)):
			self.res = res
		else:
			print("Invalid res")
			return None
		
	def __del__(self):
		super().__del__()


class req_info(Protocol):
	def __init__(self, sender, reciever, info, ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="req_info", ID=ID)
		
		if(type(info)==type([0,0])):
			try:
				acceptable=["pos", "dis", "pace"]
				result=[]
				for i in info:
					for j in acceptable:
						if(i == j):
							result.append(i)
							break
				if(len(result)):
					self.info=result
				else:
					print("No valid info requests")
					return None
			except:
				print("Invalid info requested")
				return None
		else:
			print("Invalid info requested")
			return None


class res_info(Protocol):
	def __init__(self, sender, reciever, info, ID=0):
		super().__init__(sender=sender, reciever=reciever, typeof="res_info", ID=ID)
		
		if(type(info)==type({"":""})):
			try:
				acceptable=["pos", "dis", "pace"]
				result={}
				for i in info:
					for j in acceptable:
						if (i==j):
							if (type(info[i])==type("")):
								result[i]=info[i]
				if(len(result)):
					self.info=result
				else:
					print("No valid info to respond")
					return None
			except:
				print("Invalid info sent")
				return None
		else:
			print("Invalid info sent")
			return None


def convert_json_protocol(json):
	typeof=json["typeof"]
	if (typeof == "hs_req"):
		return hs_req(sender=json["sender"],reciever=json["reciever"],ID=json["ID"],nxt_action=json["nxt_action"])
	elif (typeof == "hs_res"):
		return hs_res(sender=json["sender"],reciever=json["reciever"],ID=json["ID"],res_to=json["res_to"],res=json["res"])
	elif (typeof == "req_info"):
		return req_info(sender=json["sender"],reciever=json["reciever"],ID=json["ID"],info=json["info"])
	elif (typeof == "res_info"):
		return res_info(sender=json["sender"],reciever=json["reciever"],ID=json["ID"],info=json["info"])
	elif (typeof == "starttime"):
		return req_info(sender=json["sender"],reciever=json["reciever"],ID=json["ID"],starttime=json["sterttime"], action=json["action"])
        
        



















