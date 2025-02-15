from mmaction.apis import inference_recognizer, init_recognizer
import pickle




config_path = "/home/labuser/OnHit/mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-motion-u100-80e_ntu60-xsub-keypoint-3d.py"
checkpoint_path = "https://download.openmmlab.com/mmaction/v1.0/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d_20221230-7f356072.pth"

with open("/home/labuser/OnHit/OnHitCode/Mapping/zedtopkl/pickle_data/annotation.pkl", "rb") as f:
    data = pickle.load(f)


img_path =  data["annotations"][0] # waiting for pkl file from issue2


model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  
result = inference_recognizer(model, img_path)