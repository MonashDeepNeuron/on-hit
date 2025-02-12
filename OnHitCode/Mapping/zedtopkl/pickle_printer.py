
import pickle

with open('pickle_data/annotation.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)
