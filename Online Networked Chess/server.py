import socket
import threading

HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

addresses = {}
colour_clients = {"1" : "white", "2" : "black"}

color_sent = False
nothing_sent = True
playing = False

color = "white"
board = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global nothing_sent, color_sent, board, color, playing
    print(f"[NEW CONNECTION] {addr} connected.")

    addresses[str(threading.activeCount() - 1)] = addr

    connected = True
    while connected:
        nothing_sent = True
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f"[DISCONNECTED] {addr} disconnected")
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
                connected = False

            if msg != "Hello" and msg != DISCONNECT_MESSAGE:
                board = msg
                
                if not playing:
                    if color == "white": color = "black"
                    else: color = "white"

            conn.send(f"{color}.{board}".encode(FORMAT))

    conn.close()


def start():
    global colour_clients, addresses
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        color = colour_clients[str(threading.activeCount() - 1)]
        conn.sendto(color.encode(FORMAT), addresses[str(threading.activeCount() - 1)])



print("[STARTING] server is starting...")
start()
