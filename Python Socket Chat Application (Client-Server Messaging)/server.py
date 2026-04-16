import socket
import threading
import time

clients = {}
client_id_counter = 1
lock = threading.Lock()

def typing_effect(message, conn):
    for ch in message:
        conn.send(ch.encode())
        time.sleep(0.05)   # typing delay

def handle_client(conn, addr, client_id):
    print(f"[CONNECTED] {client_id} from {addr}")

    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"[MESSAGE from {client_id}] {msg}")

        except:
            break

    print(f"[DISCONNECTED] {client_id}")
    conn.close()
    del clients[client_id]


def server_send():
    """Thread to let server send to selected client"""
    while True:
        if len(clients) == 0:
            continue

        print("\nConnected Clients:", list(clients.keys()))
        target = input("Enter client ID to message: ")

        if target not in clients:
            print("Invalid Client ID!")
            continue

        msg = input("Enter message to send: ")

        # typing simulation
        clients[target].send("Server is typing...\n".encode())
        time.sleep(1)

        # send message with typing effect
        typing_effect(f"Server: {msg}\n", clients[target])



def main():
    global client_id_counter

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(16)

    print("[SERVER STARTED] Listening on port 9999")

    threading.Thread(target=server_send, daemon=True).start()

    while True:
        conn, addr = server.accept()
        
        with lock:
            client_id = f"client_{client_id_counter}"
            client_id_counter += 1
            clients[client_id] = conn

        conn.send(client_id.encode())

        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()


if __name__ == "__main__":
    main()
