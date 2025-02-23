from mmaction.apis import inference_recognizer, init_recognizer
import pickle




config_path = "/home/labuser/OnHit/mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d.py"
checkpoint_path = "/home/labuser/OnHit/OnHitCode/models/test2/epoch_20.pth"

with open("/home/labuser/OnHit/OnHitCode/Mapping/zedtopkl/test_pkl_files/nathan_dataset.pkl", "rb") as f:
    data = pickle.load(f)


img_path =  data["annotations"][21] # waiting for pkl file from issue2


model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  
result = inference_recognizer(model, img_path)
print(result)