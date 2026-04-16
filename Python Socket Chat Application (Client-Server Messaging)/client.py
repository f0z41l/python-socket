import socket
import threading
import time
import sys


def typing_animation():
    """Displays a simple 'Typing...' animation."""
    for _ in range(3):
        sys.stdout.write("\rTyping.")
        time.sleep(0.3)
        sys.stdout.write("\rTyping..")
        time.sleep(0.3)
        sys.stdout.write("\rTyping...")
        time.sleep(0.3)
    # Clear the typing animation line
    sys.stdout.write("\r                  \r")


def receive_msg(sock):
    """Receives and processes messages from the server."""
    while True:
        try:
            msg = sock.recv(1024).decode()
            if "typing" in msg.lower():
                typing_animation()
            else:
                # Print message on a new line to avoid conflicting with input()
                print("\n" + msg)
        except:
            # Connection closed or error
            print("\nDisconnected from server.")
            sock.close()
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Using localhost (127.0.0.1) for testing
    HOST = "127.0.0.1" 
    PORT = 9999
    
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {HOST}:{PORT}. Ensure the server is running.")
        return

    # Receive the initial client ID/name from the server
    client_id = sock.recv(1024).decode()
    print(f"Connected as {client_id}")

    # Start the thread to continuously receive messages
    threading.Thread(target=receive_msg, args=(sock,), daemon=True).start()

    # Main loop for sending messages
    while True:
        try:
            msg = input("")
            # The server will handle prepending the client_id to the message
            sock.send(msg.encode())
        except EOFError:
            # Handle Ctrl+D/Ctrl+Z
            break
        except Exception:
            break


if __name__ == "__main__":
    main()