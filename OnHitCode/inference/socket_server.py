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

        # Receive a single message
        data = self.client_socket.recv(8192).decode()
        print(f"Received from client: {data}")

        return data  # Return the received message

    def continuous_receive_return_message(self):
        """
        Continously listens to receive a message and send a message back to the client.

        Return: 
            None
        """
        while True:
            self.client_socket, client_address = self.server_socket.accept()
            print(f"Connected by {client_address}")

            # Receive a single message from the client
            data = self.client_socket.recv(8192).decode()
            print(f"Received from client: {data}")

            message = placeholder_data()
            self.client_socket.send(message.encode())

    def close_socket(self):
        '''
        Manually closes the socket
        '''
        if hasattr(self, "client_socket"):  # Check if client socket exists
            self.client_socket.close()
            print("Client socket closed.")
        self.server_socket.close()
        print("Server socket closed.")


####################################################################
#                                                                  #
#                                                                  #
#            TESTING DATA ONLY REMOVE ON PRODUCTION!!!!            #
#                                                                  #
#                                                                  #
#####################################################################
def placeholder_data():
    from mmaction.apis import inference_recognizer, init_recognizer
    import pickle

    config_path = "/home/labuser/OnHit/mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-motion-u100-80e_ntu60-xsub-keypoint-3d.py"
    checkpoint_path = "https://download.openmmlab.com/mmaction/v1.0/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d_20221230-7f356072.pth"

    with open("/home/labuser/OnHit/OnHitCode/Mapping/zedtopkl/pickle_data/annotation.pkl", "rb") as f:
        data = pickle.load(f)


    img_path =  data["annotations"][1] # waiting for pkl file from issue2


    model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  
    result = inference_recognizer(model, img_path)
    pred_score = result.pred_score
    return str(pred_score)
####################################################################
#                                                                  #
#                                                                  #
#            TESTING DATA ONLY REMOVE ON PRODUCTION!!!!            #
#                                                                  #
#                                                                  #
#####################################################################


# Run the server to receive one message
if __name__ == "__main__":
    server = SocketServer()
    try:
        # message = server.receive_single_message()
        # print(f"Final message received: {message}")
        server.continuous_receive_return_message()
    except KeyboardInterrupt:
        print("\nServer interrupted.")
    finally:
        server.close_socket()
