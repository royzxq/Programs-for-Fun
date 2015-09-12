import sys
sys.path.append('../')

import socket
from threading import BoundedSemaphore, Thread
from crawler import TaskQueue

class Connector(Thread):
	"""docstring for Connector"""
	def __init__(self, taskQueue, TaskLock, PageQueue, PageLock, event, host, output, port):
		Thread.__init__(self)
		self.taskQueue = taskQueue
		self.TaskLock = TaskLock
		self.PageQueue = PageQueue
		self.PageLock = PageLock
		self.event = event
		self.host = host
		self.output = output
		self.port = port

		self.doneTask = TaskQueue(None)
		self.donePage = TaskQueue(None)

		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
	# @param port is the wanted port 
	def prepare(self):
		self.socket.bind((self.host,self.port))
		print "Listening on the port ", self.port
		self.socket.listen(5)
		self.conn, self.addr = self.socket.accept()
		print 'connected by', self.addr		

	def run(self):
		self.prepare()
		while 1:
			self.event.wait()
			with self.TaskLock:
				task = self.taskQueue.get()
				task.state = "working"
			self.conn.send(task.url)
			page = self.conn.recv(2048)
			if task.type == "list":
				with self.TaskLock:
					for newTask in page:
						self.taskQueue.add(newTask)
					task.state = "done"
					self.doneTask.add(task)
			else:
				with self.PageLock:
					self.PageQueue.add(page)
					self.output.write(page)
				with self.TaskLock:
					task.state = "done"
					self.doneTask.add(task)
			if self.taskQueue.numOfNewTasks == 0:
				self.conn.send("")
				break
		self.conn.close()
		return 



