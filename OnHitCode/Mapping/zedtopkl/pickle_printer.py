
import pickle

with open('./test_pkl_files/annotation.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)
