import socket
import threading
import sys
import os

sys.path.append("D:\Hackathon\hack\Lib\site-packages\rsa")
import rsa
from dotenv import load_dotenv
load_dotenv()
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = 65432

public_key, private_key = rsa.newkeys(2048) # generating public and private access keys.
#only the private keys is sent to the server


def receive_messages(sock):
    while True:
        try:
            encrypted_data = sock.recv(4096)
            if not encrypted_data:
                break
            decrypted_data = rsa.decrypt(encrypted_data, private_key).decode()
            print(f"\nReceived: {decrypted_data}")
        except:
            break
    print("Disconnected from server")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

    server_public_key = rsa.PublicKey.load_pkcs1(s.recv(4096))
    s.send(public_key.save_pkcs1())

    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    receive_thread.start()

    while True:
        message = input("Enter message to send (or 'quit' to exit): ")
        if message.lower() == 'quit':
            break
        encrypted_message = rsa.encrypt(message.encode(), server_public_key)
        s.sendall(encrypted_message)