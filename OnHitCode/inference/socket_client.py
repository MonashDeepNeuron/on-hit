import socket

class SocketClient:
    '''
    Use this on the remote computer to send messages to a socket
    '''
    def __init__(self, server_ip="127.0.0.1", port=5000):
        self.server_ip = server_ip
        self.server_port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to {self.server_ip}:{self.server_port}")

    def send_message(self, message):
        '''
        Sends a single message over to the server, note the message has no specificed type

        Input:
            message: all = whatever you want to send over to the server
        '''
        self.client_socket.sendall(message)
        response = self.client_socket.recv(1024).decode()
        return response

    def close_socket(self):
        '''
        Manually close the socket
        '''
        self.client_socket.close()
        print("Client socket closed.")

# Run the client to send one message
if __name__ == "__main__":
    client = SocketClient("130.194.132.217")  # Replace with actual server IP
    try:
        client.send_message("Hello, Server!")
    finally:
        client.close_socket()
