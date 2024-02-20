from client import NetworkClient
import threading

class F35(NetworkClient):
    def __init__(self, client_id, current_position, current_speed):
        super().__init__(client_id)
        self.current_position = current_position
        self.current_speed = current_speed

        self.reporting_thread = threading.Thread(target=self.report_postion_and_speed)
        

    def get_current_position(self):
        return self.current_position
    
    def get_current_speed(self):
        return self.current_speed
    
    def report_postion_and_speed(self):
        try:
            while True:
                report_message = f"Current postion: {self.current_position}, Current speed: {self.current_speed}"

                self.client_socket.send(report_message.encode('utf-8'))

                #print("Sent current postion and speed")

                #time.sleep(10)

        except (ConnectionError, OSError):
            print("Error sending current postion and speed. Connection may be closed")

    def start_reporting_thread(self):
        self.reporting_thread.start()


def main():
    F35_client = F35("F35", (100, 500), "300 knots")
    #ground_station = GroundStation("GS", (100, 200))
    
    try:
        F35_client.connect_to_server()
        #ground_station.connect_to_server()
        #F35_client.start_reporting_thread()

    except KeyboardInterrupt:
        print("Closing the client.")
        F35_client.close_connection()
        #ground_station.close_connection()
    #client2.connect_to_server()

if __name__ == "__main__":
    main()