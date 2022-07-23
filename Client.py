import socket

PORT = 9999
SERVER_IP = socket.gethostname()
BUFFER = 128

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))

msg = "Hello"
s.send(msg.encode('utf-8'))
rply = s.recv(BUFFER).decode('utf-8')
print(rply)
s.close()