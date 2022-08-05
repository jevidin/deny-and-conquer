import socket
import argparse
import threading

# Defaults
SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128

COLOR = None
LISTENING = True

class Client():
    def __init__(self):
        self.LISTENING = True

        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.connect((SERVER_IP, PORT))
        print(f"[CONNECTED] to {SERVER_IP}")

        self.COLOR = self.SOCKET.recv(BUFFER).decode('utf-8')
        print(self.COLOR)

        threading.Thread(target=self.startListener, args=()).start()
        threading.Thread(target=self.startInput, args=()).start()

    def fillerFunc():
        print("blah")

    def sendMessage(self, msg):
        self.SOCKET.send(msg.encode('utf-8'))

    def startInput(self):
        while self.LISTENING:
            msg = input()
            if (self.LISTENING):
                self.SOCKET.send(msg.encode('utf-8'))

    def startListener(self):
        while self.LISTENING:
            receive = self.SOCKET.recv(BUFFER).decode('utf-8')
            arg = receive.split(' ')
            if (arg[0] == "DISCONNECT" or arg[0] == "STOP"):
                # Stop listener thread
                print("Press enter again to stop...")
                self.LISTENING = False
                break
            elif (arg[0] == "LOCK"):
                # Server tells client that square at (x,y) is locked
                # LOCK x y
                x = arg[1]
                y = arg[2]
                # ...code here for client to lock square at (x,y)
                # ...call functions in Client_GUI.py to manipulate GUI
            elif (arg[0] == "UNLOCK"):
                # Server tells client that square at (x,y) is unlocked
                # UNLOCK x y
                x = arg[1]
                y = arg[2]
                # ...code here for client to unlock square at (x,y)
                # ...call functions in Client_GUI.py to manipulate GUI
            elif (arg[0] == "CLAIM"):
                # Server tells client that square at (x,y) is claimed by (color)
                # CLAIM x y color
                x = arg[1]
                y = arg[2]
                color = arg[3]
                # ...code here for client to lock square at (x,y) and color it
                # ...call functions in Client_GUI.py to manipulate GUI
            elif (arg[0] == "START"):
                # Server tells client that game has started
                self.fillerFunc()
                # ...call functions in Client_GUI.py to manipulate GUI
            elif (arg[0] == "RESTART"):
                # Server tells client to restart game (reset GUI)
                self.fillerFunc()
                # ...call functions in Client_GUI.py to manipulate GUI
            elif (arg[0] == "END"):
                # Server tells client that game has ended and which color won the game
                # END color
                color = arg[1]
                # ...call functions in Client_GUI.py to manipulate GUI
            else:
                print(receive)
