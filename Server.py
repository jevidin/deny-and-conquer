from re import L
import socket
import _thread

SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))

server.listen(4)

listen = True
while listen:
    #Blocking line
    c, addr = server.accept()

    msg = c.recv(BUFFER).decode('utf-8')

    rply = " "
    c.send(rply.encode('utf-8'))
    c.close()
    listen = False

server.close()
