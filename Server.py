import socket
import argparse
import threading

# Defaults
SERVER_IP = socket.gethostname()
SERVER = None
PORT = 9999
BUFFER = 128

MAX_CLIENTS = 4
CURR_CLIENTS = 0
CLIENTS = {}
LISTENING = {}

COLORS = ["RED", "BLUE", "GREEN", "YELLOW"]
PLAYER_COLOR = {}

def startServer(ip, port):
    global SERVER, LISTENING, CURR_CLIENTS

    # Create a TCP socket
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the server address and listen
    SERVER.bind((ip, port))
    SERVER.listen(4)
    print(f"[SERVER LIVE] listening on {ip} and port {port}")

    while CURR_CLIENTS < MAX_CLIENTS:
        # Blocking line for accepting client connection request
        client, addr = SERVER.accept()

        # Assign client a color
        color = COLORS.pop(0)
        PLAYER_COLOR[client.fileno()] = color
        msg = color
        client.send(msg.encode('utf-8'))

        # Store reference to each client and whether they are listening
        CLIENTS[client.fileno()] = client
        LISTENING[client.fileno()] = True

        # Have a listener for each client run on separate threads
        threading.Thread(target=startListener, args=(client,)).start()

        # Increment CURR_CLIENTS
        CURR_CLIENTS += 1

        # TODO: close clients, decrement curr_client, remove from CLIENTS{}, stop respective client thread (if needed)

    
def startListener(client):
    global SERVER, LISTENING, CURR_CLIENTS
    while LISTENING[client.fileno()]:
        receive = client.recv(BUFFER).decode('utf-8')
        arg = receive.split(' ')

        if (arg[0] == "STOP"):
            # Will cause exception messages
            msg = "STOP"
            LISTENING[client.fileno()] = False
            client.send(msg.encode('utf-8'))
            for client in CLIENTS.values():
                client.close()
            SERVER.close()
            break
        elif (arg[0] == "DISCONNECT"):
            # User disconnects
            msg = "DISCONNECT"
            CURR_CLIENTS -= 1
            COLORS.append(PLAYER_COLOR[client.fileno()])
            LISTENING[client.fileno()] = False
            client.send(msg.encode('utf-8'))
            client.close()
            break
        elif (arg[0] == "PRINT"):
            # Test function
            for data in arg:
                if (data != "PRINT"):
                    print(data)
        elif (arg[0] == "PING"):
            # Test function
            msg = "PONG!"
            client.send(msg.encode('utf-8'))
        elif (arg[0] == "LOCK"):
            # Client tells server that square at (x,y) is locked
            # LOCK x y
            x = arg[1]
            y = arg[2]
            # ...code for locking square at (x,y) in game state
        elif (arg[0] == "UNLOCK"):
            # Client tells server that square at (x,y) is unlocked
            # UNLOCK x y
            x = arg[1]
            y = arg[2]
            # ...code for unlocking square at (x,y) in game state
        elif (arg[0] == "CLAIM"):
            # Client tells server that they claim the square at (x,y)
            # CLAIM x y
            x = arg[1]
            y = arg[2]
            # ...code for claiming square at (x,y) in game state
            # check for whether client has claimed 50% of the square should be done on client side(?)


def broadcast(msg):
    for client in CLIENTS.values():
        client.send(msg.encode('utf-8'))


def main():
    # Parse arguments
    # (usage example: Server.py --ip 192.168.0.1 --port 9999, type --help to show usage)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default=SERVER_IP,
                        help="provide server ip which the clients will connect to.")
    parser.add_argument('--port', type=int, default=PORT, help="provide server port.")
    args = parser.parse_args()

    startServer(args.ip, args.port)


if __name__ == "__main__":
    main()
