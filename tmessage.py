
from queue import Queue

class MessageNode():
    def __init__(self, msg_id, wparam = None, lparam = None):
    	self.msg_id = msg_id
    	self.wparam = wparam 
    	self.lparam = lparam

def createMessageQueue():
	queue = Queue()
	return queue

class Looper:
	def __init__(self):
		self.queue = Queue()

	def sendMessage(self, msg):
		self.queue.put(msg)

	def obtainMessage(self):
		return self.queue.get()
