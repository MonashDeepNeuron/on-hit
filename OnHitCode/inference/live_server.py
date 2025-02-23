from mmaction.apis import inference_recognizer, init_recognizer
import pickle
from socket_server import *
import numpy as np



config_path = "/home/labuser/OnHit/mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d.py"
checkpoint_path = "/home/labuser/OnHit/OnHitCode/models/test2/epoch_20.pth"

model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  

ws_server = SocketServer()


'''
Function to take the result from mmaction and then process it into a string
'''
def format_prediction(prediction):
    """Converts MMAction2 prediction output to a readable string with top 5 predictions."""
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

    for i in range(5):
        result_str += f"  {i+1}. Class {top5_indices[i]} - {top5_scores[i]:.4f}\n"

    return result_str

'''
Loop to send and recieve message
1. Recieve message
2. predict 
3. send back 
'''
while True:
    input_data = ws_server.receive_single_message()
    skeleton_data = pickle.loads(input_data)


    result = inference_recognizer(model, skeleton_data)

    formatted_result = format_prediction(result)

    ws_server.send_message(formatted_result)
