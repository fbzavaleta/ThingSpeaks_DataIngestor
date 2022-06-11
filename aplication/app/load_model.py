import pickle
from sklearn.linear_model import LinearRegression

class LoadLoad():
    def __init__(self, filename):      
        with open(filename , 'rb') as f:
            loaded_model = pickle.load(f)            
        self.model = loaded_model
    
