# import socket
#
# HOST = '0.0.0.0'  # Listen on all available interfaces
# PORT = 65432      # Port to listen on (non-privileged ports are > 1023)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     print(f"Server listening on {HOST}:{PORT}")
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:

#                 break
#             print(f"Received: {data.decode()}")
#             message = input("Enter message to send: ")
#             conn.sendall(message.encode())

import socket
import threading
import asyncio
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from {addr}: {data.decode()}")

            message = f"Client {addr}: {data.decode()}"
            broadcast(message, conn)

        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    print(f"Connection from {addr} closed")
    conn.close()
    clients.remove(conn)


def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode())
            except:
                client.close()
                clients.remove(client)


clients = set()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()