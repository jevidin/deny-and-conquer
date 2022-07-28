from re import L
import socket
import _thread
import threading

print("Starting server...")

SERVER_IP = socket.gethostname()
SERVER = None
PORT = 9999
BUFFER = 128

MAX_CLIENTS = 4
CURR_CLIENTS = 0
CLIENTS = {}
LISTENING = {}

def startServer():
    global SERVER, LISTENING, CURR_CLIENTS
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((SERVER_IP, PORT))
    SERVER.listen(4)

    while CURR_CLIENTS < MAX_CLIENTS:
        c, addr = SERVER.accept()
        CLIENTS[c.fileno()] = c
        LISTENING[c.fileno()] = True
        threading.Thread(target=startListener, args=(c,)).start()
        CURR_CLIENTS += 1

def startListener(c):
    global SERVER, LISTENING, CURR_CLIENTS
    while LISTENING[c.fileno()] == True:
        receive = c.recv(BUFFER).decode('utf-8')
        arg = receive.split(' ')
        if (arg[0] == "STOP"):
            msg = "STOP"
            c.send(msg.encode('utf-8'))
            c.close()
            SERVER.close()
            break
        elif(arg[0] == "PRINT"):
            for data in arg:
                if (data != "PRINT"):
                    print(data)
        elif(arg[0] == "PING"):
            msg = "PONG!"
            c.send(msg.encode('utf-8'))

def broadcast(msg):
    for client in CLIENTS.values():
        client.send(msg.encode('utf-8'))

startServer()