from client import NetworkClient

class GroundStation(NetworkClient):
    def __init__(self, client_id, current_positon):
        super().__init__(client_id)
        self.current_postion = current_positon

    def get_current_postion(self):
        return self.current_postion

def main():
    ground_station = GroundStation("GS", (100, 200))

    try:
        ground_station.connect_to_server()
    
    except KeyboardInterrupt:
        print("Closing the client.")
        ground_station.close_connection()

if __name__ == "__main__":
    main()