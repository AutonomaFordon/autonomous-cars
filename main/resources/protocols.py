class Protocol():
	def __init__(self, sender="unknown"):
		self.sender = sender
		self.id_count = 0
		self.sent = {}
		self.recieved = {}
    
	def mkptc(self, ID=-1, sender="", rec="", typeof="", data=""):
		if (ID==-1): ID = self.id_count
		if (sender==""): sender=self.sender
		
		msg = bytes(ID)
		msg += "|"
		msg += sender
		msg += "|"
		msg += rec
		msg += "|"
        
		if (typeof=="req_pos" or typeof=="hs_req" or typeof=="est_req"):
			msg += typeof
		elif (typeof=="send_pos" or typeof=="hs_res" or typeof=="est_res"):
			msg += typeof
			msg += "|"
			msg += data
		else:
			print("requested protocol does not exist")
			return 0

		if (sender == self.sender):
			self.sent[self.id_count] = [msg, ID, sender, rec, typeof, data]
			self.id_count += 1
		else:
			self.recieved[sender+"|"+str(ID)] = [msg, ID, sender, rec, typeof, data]

		return msg, ID
    

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
