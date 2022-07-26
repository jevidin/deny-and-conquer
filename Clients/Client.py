import socket
import argparse

# Defaults
BUFFER = 128
PORT = 9999
SERVER_IP = socket.gethostname()
END = "end"


def main():
    # Parse arguments
    # (usage example: Client.py --ip 192.168.0.1 --port 9999)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default=SERVER_IP)
    parser.add_argument('--port', type=int, default=PORT)
    args = parser.parse_args()

    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\

    # Connect the socket to the server address (IP, PORT)
    client.connect((args.ip, args.port))

    while True:
        msg = input("For Server: ")
        client.send(msg.encode('utf-8'))
        reply_msg = client.recv(BUFFER).decode('utf-8')
        print(reply_msg)
        if msg == END:
            break

    print(f"[DISCONNECTED] Closing client.")
    client.close()


if __name__ == "__main__":
    main()
