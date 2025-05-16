import socket
import numpy as np

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
            
            data = b""
            while True:
                packet = self.client_socket.recv(8192)
                data = data + packet
                if b"<END>" in packet: 
                    break
            print(f"Received from client")
            cleaned_data ,_= data.split(b"<END>",1)
            message = inference_on_data(cleaned_data)
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
'''
Function to take the result from mmaction and then process it into a string
'''
def format_prediction(prediction):
    '''Converts MMAction2 prediction output to a readable string with top 5 predictions.

    Input: prediction(object with 3 attritbutes)
        these attributes are generally pytorch tensors

    Output: str = a string of a dictionary that has the results and the keys that correspond to specific results 
    
    
    '''
    pred_scores = prediction.pred_score.cpu().numpy()  # Convert tensor to NumPy array
    pred_label = int(prediction.pred_label.cpu().numpy())  # Extract the predicted class
    gt_label = int(prediction.gt_label.cpu().numpy())  # Extract the ground truth label
    num_classes = int(pred_scores.shape[0])  # Total number of classes

    # Get the top 5 predictions
    top5_indices = np.argsort(pred_scores)[-5:][::-1]  # Get top 5 indices in descending order
    top5_scores = pred_scores[top5_indices]  # Get corresponding probabilities

    # Format the output string
    result_str = (
        f"Prediction Results:\n"
        f"- Number of Classes: {num_classes}\n"
        f"- Predicted Label: {pred_label} (GT: {gt_label})\n"
        f"- Top 5 Predictions:\n"
    )

    result_dict = {}
    result_arr = [0 for _ in range(14)]

    for i in range(5):
        # result_str += f"  {i+1}. Class {top5_indices[i]} - {top5_scores[i]:.4f}\n"
        result_dict[top5_indices[i]] = top5_scores[i]
        result_arr[top5_indices[i] - 1] = top5_scores[i]

    return str(result_arr)
    #return str(result_dict)
    # return result_str


from mmaction.apis import inference_recognizer, init_recognizer
import pickle

config_path = "/home/labuser/OnHit/mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d.py"
checkpoint_path = "/home/labuser/OnHit/OnHitCode/models/test2/best_acc_top1_epoch70.pth"

def inference_on_data(input_data):
    '''
    This process the data, using inference 
    Input:
        input_data: (np array) = M (person)x T(frame) x V(Joint) x C(cords)
    
    Output:
        (str) formatted stgcn results  
    '''


    model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  

    skeleton_data = pickle.loads(input_data)
    result = inference_recognizer(model, skeleton_data)

    return format_prediction(result)
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
