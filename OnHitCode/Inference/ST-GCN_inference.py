from mmaction.apis import inference_recognizer, init_recognizer

config_path = "../mmaction2/configs/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d.py"
checkpoint_path = "https://download.openmmlab.com/mmaction/v1.0/skeleton/stgcnpp/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d/stgcnpp_8xb16-bone-u100-80e_ntu60-xsub-keypoint-3d_20221230-7f356072.pth"
img_path = None # waiting for pkl file from issue2

model = init_recognizer(config_path, checkpoint_path, device="cuda:0")  
result = inference_recognizer(model, img_path)