from client import NetworkClient

class NavalVessel(NetworkClient):
    def __init__(self, client_id, current_position):
        super().__init__(client_id)
        self.current_position = current_position

    def get_current_position(self):
        return self.current_position
    
def main():
    naval_vessel = NavalVessel("NV", (100, 200))

    try:
        naval_vessel.connect_to_server()
    
    except KeyboardInterrupt:
        print("Closing the client.")
        naval_vessel.close_connection()

if __name__ == "__main__":
    main()