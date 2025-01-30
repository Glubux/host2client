import socket
import threading
import sys
import os

os.system("Client")


def receive_messages(client_socket):
    """Empfängt Nachrichten vom Server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Verbindung zum Server verloren.")
            break

def start_client():
    """Startet den Client."""
    host = '127.0.0.1'
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Verbindung herstellen
    client_socket.connect((host, port))

    # Namen eingeben und senden
    name = input("Gib deinen Namen ein: ")
    client_socket.send(name.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')

    if "INFO" in response:  # Name bereits vergeben
        print(response)
        client_socket.close()  # Verbindung sofort schließen
        return  # Beende den Code

    print(response)  # Willkommen-Nachricht anzeigen

    # Starte Thread zum Empfang von Nachrichten
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Nachrichten senden
    while True:
        message = input("")
        if message.lower() == "exit":
            print("Du hast die Verbindung getrennt.")
            client_socket.close()
            break
        # Nachricht ohne den eigenen Namen senden
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
