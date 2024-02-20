import tkinter as tk
from tkinter import Text
from server import NetworkServer
import sys
import queue
from threading import Thread
import threading

# Custom stdout class to redirect print statements
class CustomStdout:
    def __init__(self, output_queue):
        self.output_queue = output_queue

    def write(self, message):
        self.output_queue.put(message)

    def flush(self):
        pass

# ServerWindow class to display network traffic
class ServerWindow(tk.Tk):
    def __init__(self):
        super().__init__()

      
        self.title("Network Server")

        # Create a Text widget for displaying output
        self.output_text = Text(self, wrap="word")
        self.output_text.pack(expand=True, fill="both")

        # Create a queue for communication between threads
        self.output_queue = queue.Queue()

        # Redirect print statements to the queue
        sys.stdout = CustomStdout(self.output_queue)

        # Start the server in a separate thread
        self.server_thread = threading.Thread(target=self.start_server_in_thread)
        self.server_thread.start()
        #self.server_thread.join()

        # Start a periodic task to check the queue for messages
        self.after(100, self.check_output_queue)

  
    # starts the network server
    def start_server_in_thread(self):
        server = NetworkServer(self.output_queue)
        server.start_server()

    def check_output_queue(self):
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.output_text.insert("end", message)
                self.output_text.see("end")  # Scroll to the end
        except queue.Empty:
            pass
        finally:
            # Schedule the next check
            self.after(100, self.check_output_queue)


# Run the Tkinter event loop
if __name__ == "__main__":
    app = ServerWindow()
    app.mainloop()