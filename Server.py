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


def startServer(ip, port):
    global SERVER, LISTENING, CURR_CLIENTS

    # Create a TCP socket
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the server address and listen
    SERVER.bind((ip, port))
    SERVER.listen(4)
    print(f"[SERVER LIVE] listening on {ip} and port {port}")

    while CURR_CLIENTS < MAX_CLIENTS:
        # Blocking line
        client, addr = SERVER.accept()
        CLIENTS[client.fileno()] = client
        LISTENING[client.fileno()] = True
        threading.Thread(target=startListener, args=(client,)).start()
        CURR_CLIENTS += 1

        # receive = c.recv(BUFFER).decode('utf-8')
        # print("Client " + str(CURR_CLIENTS) + ": " + receive)
        # broadcast("Hello")

        # TODO: close clients, decrement curr_client, remove from CLIENTS{}, stop respective client thread (if needed)


def startListener(c):
    global SERVER, LISTENING, CURR_CLIENTS
    while LISTENING[c.fileno()]:
        receive = c.recv(BUFFER).decode('utf-8')
        arg = receive.split(' ')

        if (arg[0] == "STOP"):
            msg = "STOP"
            c.send(msg.encode('utf-8'))
            c.close()
            break
        elif (arg[0] == "PRINT"):
            for data in arg:
                if (data != "PRINT"):
                    print(data)
        elif (arg[0] == "PING"):
            msg = "PONG!"
            c.send(msg.encode('utf-8'))

    SERVER.close()


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
