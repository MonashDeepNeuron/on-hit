import socket

class SocketServer:
    def __init__(self, host:str="0.0.0.0", port:int=5000):
        '''
        Init for the server class, this allows us to create a server socket that recieves messages
        Input: 
            host: str = 0,0,0,0 means it accepts from all ips
            port: int = port number use to connect
        
        '''
        self.server_ip = host
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)
        self.server_socket.settimeout(None)
        print(f"Server listening on {self.server_ip}:{self.server_port}...")

    def receive_single_message(self):
        '''
        Calling this function opens up the socket to receive message and then 
        returns it (note: does not automatically close the socket)

        Return:
            data: depends on what you are sending over, most likely will be a json like

        '''
        """Waits for a single message from the client and returns it."""
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Connected by {client_address}")


        buffer = b""
        while True:
        # Receive a single message
            data = self.client_socket.recv(1024)
            buffer += data 
            if b"<END>" in buffer:
                print("Buffer reached")
                break

        #Gotta remove the buffer
        cleaned_data, _ = buffer.split(b"<END>",1)
        return cleaned_data  # Return the received message

    def close_socket(self):
        '''
        Manually closes the socket
        '''
        if hasattr(self, "client_socket"):  # Check if client socket exists
            self.client_socket.close()
            print("Client socket closed.")
        self.server_socket.close()
        print("Server socket closed.")
    
    def send_message(self, message: str):
        """
        Sends a message to the client.
        Inputs:
            message (str): The response message to send.
        """
        if hasattr(self, "client_socket"):  # Check if the client socket exists
            message += b"<END>"
            self.client_socket.sendall(message.encode())
            print(f"Sent to client: {message}")

# Run the server to receive one message
if __name__ == "__main__":
    server = SocketServer()
    try:
        message = server.receive_single_message()
        print(f"Final message received: {message}")
    except KeyboardInterrupt:
        print("\nServer interrupted.")
    finally:
        server.close_socket()
