import socket
import threading

print("Starting client...")

SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128

LISTENING = True

def startListener(s):
    global LISTENING
    while LISTENING == True:
        receive = s.recv(BUFFER).decode('utf-8')
        arg = receive.split(' ')
        if (arg[0] == "STOP"):
            LISTENING = False
            s.close()
            break
        else:
            print(receive)

def startInput(s):
    global LISTENING
    while LISTENING == True:
        msg = input()
        s.send(msg.encode('utf-8'))

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))

    threading.Thread(target=startListener, args=(s,)).start()
    threading.Thread(target=startInput, args=(s,)).start()

connect()