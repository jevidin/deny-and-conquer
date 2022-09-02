import socket
import threading
import ipaddress
from tkinter import *
import tkinter.font as font
import math

from Server import SERVER, receiveMsg

# Defaults
SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128
SOCKET = None

class Client():
    # def __init__(self, ip, port):
    #     self.ip = ip
    #     self.port = port

    def connect(self, ip, port):
        self.LISTENING = True
        # Create TCP socket and connect to server with IP and PORT
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if len(ip) == 0:
            ip = SERVER_IP
            self.SOCKET.connect((SERVER_IP, int(port)))
            print(f"[CONNECTED] to {SERVER_IP}")
            # Receive color assigned by server
            self.COLOR = receiveMsg(self.SOCKET)
            # Start thread to listen for messages from server
            threading.Thread(target=self.startListener, args=()).start()
            threading.Thread(target=self.startInput, args=()).start()
            return True
        else:
            try:
                ipAddress = ipaddress.ip_address(ip)
                self.SOCKET.connect((ip, int(port)))
                print(f"[CONNECTED] to {ip}")
                # Receive color assigned by server
                self.COLOR = receiveMsg(self.SOCKET)
                # Start thread to listen for messages from server
                threading.Thread(target=self.startListener, args=()).start()
                threading.Thread(target=self.startInput, args=()).start()
                ret = True
            except ValueError:
                print("IP address {} is not valid".format(ip)) 
                ret = False
            return ret

    def sendMessage(self, msgContent):
        msgLen = len(msgContent)
        msg = f'{msgLen} {msgContent}'
        self.SOCKET.send(msg.encode('utf-8'))

    def getColor(self):
        return self.COLOR

    def startInput(self):
        while self.LISTENING:
            msgContent = input()
            if (self.LISTENING):
                msgLen = len(msgContent)
                msg = f'{msgLen} {msgContent}'
                self.SOCKET.send(msg.encode('utf-8'))

    def setGameWindow(self, gameWindow):
        self.GAME_WINDOW = gameWindow

    def setEndWindow(self, endWindow):
        self.END_WINDOW = endWindow

    def startListener(self):
        while self.LISTENING:
            receiveData = self.receiveMsg(self.SOCKET)
            arg = receiveData.split(' ')
            if (arg[0] == "DISCONNECT" or arg[0] == "STOP"):
                # Stop listener thread
                print("Press enter again to stop...")
                self.LISTENING = False
                break
            elif (arg[0] == "LOCK"):
                # Receive message from server to lock square at (x,y) for other player color
                x = arg[1]
                y = arg[2]
                color = arg[3]
                if (color != self.COLOR):
                    self.GAME_WINDOW.lockPlayersBox(x, y, color)
            elif (arg[0] == "UNLOCK"):
                # Receive message from server to unlock square at (x,y)
                x = arg[1]
                y = arg[2]
                if (color != self.COLOR):
                    self.GAME_WINDOW.unlockPlayersBox(x, y)
            elif (arg[0] == "CLAIM"):
                # Receive message from server to permanently claim square at (x,y) for other player color
                x = arg[1]
                y = arg[2]
                color = arg[3]
                self.GAME_WINDOW.fillBox(x, y, color)
            elif (arg[0] == "ENDPAGE"):
                # Receive message from server to display winner
                self.END_WINDOW.winUpdate(arg[1])
                # Receive message from server to bring up end screen
                if (color != self.COLOR):
                    self.GAME_WINDOW.bringUpEnd()
            elif (arg[0] == "END"):
                # Receive message from server to print winner
                print(f"[DISCONNECTED] Winner: {arg[1]}. Press any key to exit program.")
                self.LISTENING = False
                break
            else:
                print(receiveData)

    def receiveMsg(self, client):
        c = client.recv(1).decode('utf-8')
        charStr = ""
        while c != " ":
            charStr += c
            c = client.recv(1).decode('utf-8')
        size = int(charStr)
        data = ""
        while len(data) < size:
            receive = client.recv(size - len(data))
            if not receive:
                return None
            data += receive.decode('utf-8')
        return data
