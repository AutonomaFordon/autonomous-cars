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


class Protocol():
    def __init__(self, sender="unknown"):
        self.sender = sender
        self.id_count = 0
        self.sent = {}
        self.recieved = {}
        
    def mkptc(self, ID=-1, sender="", rec="", typeof="", data=""):

		if (ID==-1): ID = self.id_count

		if (sender==""): sender==self.sender
		
        msg = str(ID)
        msg += "|"
        msg += sender
        msg += "|"
        msg += rec
        msg += "|"
        
        if (typeof=="req_pos" or typeof=="hs_req"):
            msg += typeof
        elif (typeof=="send_pos" or typeof=="hs_res"):
            msg += typeof
            msg += "|"
            msg += data
        else:
            print("requested protocol does not exist")
            return 0
        
        if (sender == self.sender):
            self.sent[self.id_count] = msg
            self.id_count += 1
        else:
            self.recieved[sender+"|"+ID] = msg
        
        return msg
        
    def interpret(self, msg):
        splitted = msg.split("|")
        ID = splitted[0]
        sender = splitted[1]
        reciever = splitted[2]
        typeof = splitted[3]
        if (len(splitted) == 5):
            data = splitted[4]
            return mkptc(ID, sender, reciever, typeof, data)
        return mkptc(ID, sender, reciever, typeof)

myProtocol = Protocol("127.168.0.5")
print(myProtocol.mkptc(rec="127.168.0.2", typeof="req_pos"))














