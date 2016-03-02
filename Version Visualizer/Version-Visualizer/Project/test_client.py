action = raw_input('Action ')
username = raw_input('Username ')
password = raw_input('Password ')
import socket
s = socket.socket()
s.connect(('127.0.0.1', 1356))
s.send('|'.join([action, username, password]))
print s.recv(1024)