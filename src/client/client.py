from socket import *
import threading

class NetworkClient():
    def __init__(self, client_id):
        self.client_id = client_id
        self.server_IP = '127.0.0.1'
        self.server_port = 12345
        self.server_address = (self.server_IP, self.server_port)
        self.client_socket = None

    def connect_to_server(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.server_address)

        # Send client ID to server during initial connection
        self.client_socket.send(str(self.client_id).encode('utf-8'))

        # Start seperate threads for sending and receiving messages
        send_thread = threading.Thread(target=self.send_message)
        receive_thread = threading.Thread(target=self.receive_message)

        send_thread.start()
        receive_thread.start()

    
    def send_message(self):
        try:
            while True:
                message = input("\nEnter your message: ")
                self.client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print(f"Closing send thread from {self.client_id}")

    def receive_message(self):
        try:
            while True:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"\n{data}")
        except KeyboardInterrupt:
            print(f"Closing send thread from {self.client_id}")

    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()

    

'''
def main():
    client1 = NetworkClient("F35")
    #client2 = NetworkClient()
    
    try:
        client1.connect_to_server()

    except KeyboardInterrupt:
        print("Closing the client.")
        client1.close_connection()
    #client2.connect_to_server()

if __name__ == "__main__":
    main()
'''
