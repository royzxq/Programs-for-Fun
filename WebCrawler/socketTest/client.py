import socket
import time
HOST = ''
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
while 1:
	s.send('Hello')
	data = s.recv(1024)
	print 'Received', repr(data)
	time.sleep(1)
s.close()

print 'Received in raw form ', data
print type(data)