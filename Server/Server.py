import socket
import argparse
import sys
import threading

# Defaults
PORT = 9999
BUFFER = 128
SERVER_IP = socket.gethostname()
END = 'end'

# Set of clients and lock (not used now but will be needed for sending to all clients)
clients_set = set()
clients_set_lock = threading.Lock()


# Thread for and also store clients
def new_client(client, address):
    print(f"[CONNECTED] {address}")
    with clients_set_lock:
        clients_set.add(client)

    try:
        ######          TESTING WITH TEXT READ-BACKS            #########
        while True:
            msg = client.recv(BUFFER).decode('utf-8')
            print(f"[{address}] says: {msg}")
            reply_msg = f"\n[SERVER] received from {address}: {msg}"  # echo received texts
            with clients_set_lock:
                client.send(reply_msg.encode('utf-8'))
            if msg == END:
                break
        ###### ^ Replace with relevent data (e.g gui info) ^ ###########
    finally:
        with clients_set_lock:
            # Close client connection and client thread
            clients_set.remove(client)
            client.close()
            print(f"[DISCONNECTED] {address}")
            sys.exit()  # for closing threads


def main():
    # Parse arguments
    # (usage example: Server.py --ip 192.168.0.1 --port 9999, type --help to show usage)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default=SERVER_IP,
                        help="provide server ip which the clients will connect to.")
    parser.add_argument('--port', type=int, default=PORT, help="provide server port.")
    args = parser.parse_args()

    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the server address
    server.bind((args.ip, args.port))
    server.listen(4)
    print(f"[SERVER LIVE] listening on {args.ip} and port {args.port}")

    while True:
        client, address = server.accept()

        # create thread for each client
        thread = threading.Thread(target=new_client, args=(client, address))
        thread.start()

        # TODO: break and close server for some condition (e.g, when active thread reach 0)
        # TODO: til now server runs forever
        # if threading.active_count() < 1:
        #     break

    server.close()


if __name__ == "__main__":
    main()
