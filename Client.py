import socket
import argparse
import threading

# Defaults
SERVER_IP = socket.gethostname()
PORT = 9999
BUFFER = 128

COLOR = None
LISTENING = True

def startListener(s):
    global LISTENING

    while LISTENING:
        receive = s.recv(BUFFER).decode('utf-8')
        arg = receive.split(' ')
        if (arg[0] == "DISCONNECT" or arg[0] == "STOP"):
            print("Press enter again to stop...")
            LISTENING = False
            break
        elif (arg[0] == "LOCK"):
            # Server tells client that square at (x,y) is locked
            # LOCK x y
            x = arg[1]
            y = arg[2]
            # ...code here for client to lock square at (x,y)
        elif (arg[0] == "UNLOCK"):
            # Server tells client that square at (x,y) is unlocked
            # UNLOCK x y
            x = arg[1]
            y = arg[2]
            # ...code here for client to unlock square at (x,y)
        elif (arg[0] == "CLAIM"):
            # Server tells client that square at (x,y) is claimed by (color)
            # CLAIM x y color
            x = arg[1]
            y = arg[2]
            color = arg[3]
            # ...code here for client to lock square at (x,y) and color it
        else:
            print(receive)

    s.close()


def startInput(s):
    global LISTENING

    while LISTENING:
        msg = input()
        if (LISTENING):
            s.send(msg.encode('utf-8'))


def connect(ip, port):
    global COLOR

    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect socket to the server
    s.connect((ip, port))
    print(f"[CONNECTED] to {ip}")

    # Store assigned color on client side
    COLOR = s.recv(BUFFER).decode('utf-8')
    print(COLOR)

    # Run separate threads for listening to server payloads, and receiving input from user (for testing)
    threading.Thread(target=startListener, args=(s,)).start()
    threading.Thread(target=startInput, args=(s,)).start()


def main():
    # Parse arguments
    # (usage example: Client.py --ip 192.168.0.1 --port 9999)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default=SERVER_IP)
    parser.add_argument('--port', type=int, default=PORT)
    args = parser.parse_args()

    connect(args.ip, args.port)


if __name__ == "__main__":
    main()
