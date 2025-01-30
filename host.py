import socket
import threading
import sys
import os

os.system("Server")

clients = {}

def handle_client(client_socket, client_address):
    """Behandelt Nachrichten eines Clients."""
    name = client_socket.recv(1024).decode('utf-8')

    if name in clients:
        client_socket.send("INFO: Name bereits vergeben.".encode('utf-8'))
        client_socket.close()
        return

    clients[name] = client_socket
    print(f"{name} hat sich verbunden.")

    # Willkommensnachricht
    client_socket.send(f"Willkommen, {name}! Du bist jetzt verbunden.".encode('utf-8'))

    # Nachrichtenempfang vom Client
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == 'exit':
                print(f"{name} hat die Verbindung getrennt.")
                break
            elif message == "":
                break
            else:
                # Nachricht an alle anderen Clients senden
                broadcast(message, client_socket, name)
                # Server zeigt auch die Nachricht an
                print(f"Nachricht von {name}: {message}")
        except (ConnectionResetError, OSError):
            print(f"{name} hat die Verbindung unerwartet getrennt.")
            break

    # Nach dem Beenden
    clients.pop(name, None)
    client_socket.close()

def broadcast(message, client_socket, name):
    """Sendet eine Nachricht an alle Clients."""
    for client_name, client in clients.items():
        if client != client_socket:
            try:
                client.send(f"{name}: {message}".encode('utf-8'))
            except (ConnectionResetError, OSError):
                pass

def start_server():
    """Startet den Server und wartet auf Verbindungen."""
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server läuft auf {host}:{port}")

    # Thread, der eingehende Verbindungen verarbeitet
    def accept_connections():
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
            except Exception as e:
                print(f"Fehler bei der Verbindung: {e}")
                break

    # Thread für eingehende Verbindungen starten
    threading.Thread(target=accept_connections, daemon=True).start()

    # Direkt nach dem Start des Servers wird auf Befehle gewartet
    while True:
        command = input()
        if command.lower() == 'exit':
            print("*** Server wird heruntergefahren. ***")
            shutdown_server(server_socket)
            break

def shutdown_server(server_socket):
    """Beendet den Server und schließt alle Verbindungen."""
    # Eine Kopie der clients-Liste erstellen, um über sie zu iterieren
    for client_socket in list(clients.values()):  # Liste der Sockets kopieren
        client_socket.send("*** Server wird heruntergefahren. ***".encode('utf-8'))
        client_socket.close()

    # Schließe den Server-Socket
    server_socket.close()
    sys.exit(0)  # Beendet den gesamten Server-Prozess

if __name__ == "__main__":
    start_server()
