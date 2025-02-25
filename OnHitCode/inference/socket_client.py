import socket

class SocketClient:
    '''
    Use this on the remote computer to send messages to a socket
    Input:
        server_ip: str = ip address
        port:int = port number used to connect to
    '''
    def __init__(self, server_ip:str="130.194.132.217", port:int=5000):
        self.server_ip = server_ip
        self.server_port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(None)
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to {self.server_ip}:{self.server_port}")

    def send_message(self, message):
        '''
        Sends a single message over to the server, note the message has no specificed type
        There is a message at the end to mark the end 

        Input:
            message: all = whatever you want to send over to the server
        '''
        self.client_socket.sendall(message + b"<END>")
    
    def receive_message(self):
        '''
        Receives a message from the server.

        Returns:
            - str: The received message.
        '''
        if self.client_socket:
            try:
                response = self.client_socket.recv(1024).decode()
                print(f"📥 Received: {response}")
                return response
            except socket.error as e:
                print(f"❌ Receive error: {e}")
                return None

    def close_socket(self):
        '''
        Manually close the socket
        '''
        self.client_socket.close()
        print("Client socket closed.")

# Run the client to send one message
if __name__ == "__main__":
    client = SocketClient("130.194.132.217",5000)  # Replace with actual server IP
    print("socket2")
    try:
        client.send_message("Hello, Server!")
    finally:
        client.close_socket()
