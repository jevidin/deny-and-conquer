from re import L
import socket
import threading 
from threading import Thread

SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))

server.listen(4)


def client_Thread(c):
    connection = True

    while connection:
        msg = c.recv(BUFFER).decode('utf-8')
        print(msg)

        if msg=="Disconnect":
            connection = False
            print("DISCONNECTING")

        rply = "Connected"
        c.send(rply.encode('utf-8'))
    
    c.close()


listen = True
while listen:
    #Blocking line
    c, addr = server.accept()

    new_Thread = threading.Thread(target=client_Thread, args=(c,))
    new_Thread.start()

server.close()
