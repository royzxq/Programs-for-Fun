import sys
sys.path.append('../')
import socket
from threading import Thread
from page_crawler import page_crawler

class Crawler(Thread):
	"""docstring for Crawler"""
	def __init__(self, host, port):
		Thread.__init__(self)
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.crawler = page_crawler()
		self.host = host
		self.port = port

	def run(self):
		self.socket.connect((self.host,self.port))
		while 1:
			url = self.socket.recv(128)
			if  len(url) == 0:
				break
			page = self.crawler.getPage(url)
			self.socket.send(page)
		self.socket.close()
