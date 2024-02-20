from socket import socket, AF_INET, SOCK_STREAM
import threading


class NetworkServer():
    def __init__(self, output_queue):
        self.server_IP = '127.0.0.1'
        self.server_port = 12345
        self.server_address = (self.server_IP, self.server_port)
        self.server_socket = None 
        self.clients = {}
        self.output_queue = output_queue

    def start_server(self):
        # create TCP socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)

        # bind socket to local IP and port
        #self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.server_address)

        # listen for incoming connections
        self.server_socket.listen(5)
        self.output_queue.put(f"The server is ready to recieve on {self.server_IP}:{self.server_port}")

        try:
            while True:
                connection_socket, client_address = self.server_socket.accept()
                client_IP, client_port = client_address
                self.output_queue.put(f"\nAccepted connection from {client_IP}:{client_port}")

                # receive client ID from the client
                client_ID = str(connection_socket.recv(1024).decode('utf-8'))

                # create new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_ID, connection_socket))
                client_thread.start()

        except KeyboardInterrupt:
            self.output_queue.put("Server stopping...")
        finally:
            self.stop_server()

    def handle_client(self, client_ID, connection_socket):
        self.clients[client_ID] = (connection_socket, client_ID)
        #print(self.clients)

        try:
            self.print_connected_clients()

            while True:
                data = connection_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Received data from client {client_ID}: {data}")

                if client_ID == "F35":
                    self.broadcast_message(client_ID, data)

                # check for command identifier
                elif data.startswith("/sendto "):
                    target_client_ID, message = data[8:].split(" ", 1)
                    self.send_message(client_ID, target_client_ID, message)
                else:
                    print(f"Unknown command from client {client_ID}")
                


        except ConnectionResetError:
            print(f"Connection with client {client_ID} closed.")
            del self.clients[client_ID]
            self.print_connected_clients()

    def send_message(self, sender_ID, target_client_ID, message):
        target_info = self.clients.get(target_client_ID, None)
        if target_info:
            target_socket, _ = target_info
            try:
                target_socket.send(f"Message from {sender_ID}: {message}".encode('utf-8'))
            except ConnectionError:
                print(f"Error sending message to {target_client_ID}")
        else:
            print(f"Target client {target_client_ID} not found.")

    def broadcast_message(self, sender_ID, message):
        for client_ID, (client_socket, _) in self.clients.items():
            if client_ID != sender_ID:
                try:
                    client_socket.send(f"Message from {sender_ID}: {message}".encode('utf-8'))
                except ConnectionError:
                    print(f"Error broadcasting to client {client_ID}")

    def print_connected_clients(self):
        connected_clients = list(self.clients.keys())
        print("\nConnected clients: ", connected_clients)
        
        # broadcast list of connected clients to each client
        for client_id, (client_socket, _) in self.clients.items():
            try: 
                client_socket.send(f"Connected clients: {', '.join(connected_clients)}".encode('utf-8'))
            except ConnectionError:
                print(f"Error sending connected clients list to {client_id}")

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
            self.output_queue.put("Server stopped")



def main():
    server = NetworkServer()
    #server.start_server()
    
    
    try:
        # Start server in a separate thread
        server_thread = threading.Thread(target=server.start_server)
        server_thread.start()

        # Wait for the server thread to finish
        server_thread.join()
    except KeyboardInterrupt:
        # Stop server when user interrupts with Ctrl+C
        server.stop_server()
    

if __name__ == "__main__":
    main()
    