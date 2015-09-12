import socket
import time
HOST = ''
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))

s.listen(2)
print 'listening on port ', PORT
conn, addr = s.accept()
print 'connected by', addr

while 1:
	data = conn.recv(1024)
	# if not data:
	# 	break
	conn.send(data)
	time.sleep(1)
conn.close()