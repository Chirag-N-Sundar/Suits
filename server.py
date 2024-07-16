import socket
import threading
import rsa
import base64

HOST = '0.0.0.0'
PORT = 65432

public_key, private_key = rsa.newkeys(2048) # to generate the acceess keys
# the public key is only sent to the server


def handle_client(conn, addr, client_public_key):
    print(f"New connection from {addr}")
    while True:
        try:
            encrypted_data = conn.recv(4096)
            if not encrypted_data:
                break
            decrypted_data = rsa.decrypt(encrypted_data, private_key).decode()
            print(f"Received from {addr}: {decrypted_data}")

            message = f"Client {addr}: {decrypted_data}"
            broadcast(message, conn)

        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    print(f"Connection from {addr} closed")
    conn.close()
    clients.remove((conn, client_public_key))


def broadcast(message, sender_conn):
    for client, client_public_key in clients:
        if client != sender_conn:
            try:
                encrypted_message = rsa.encrypt(message.encode(), client_public_key)
                client.sendall(encrypted_message)
            except:
                client.close()
                clients.remove((client, client_public_key))


def server_input():
    while True:
        message = input("Server message: ")
        broadcast(f"Server: {message}", None)


clients = set()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    server_thread = threading.Thread(target=server_input)
    server_thread.daemon = True
    server_thread.start()

    while True:
        conn, addr = s.accept()
        conn.send(public_key.save_pkcs1())
        client_public_key = rsa.PublicKey.load_pkcs1(conn.recv(4096))
        clients.add((conn, client_public_key))
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_public_key))
        thread.start()