import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
import numpy as np
from sklearn import preprocessing as pre

class hex_neural_network:
    def __init__(self, grid_size):
        self.train_x = None
        self.train_y = None
        self.grid_size = grid_size
        self.model = keras.Sequential(
            [
                layers.Dense(9, activation="tanh", input_shape=(self.grid_size,), name="layer1"),
                layers.Dense(6, activation="tanh", name="layer2"),
                layers.Dense(grid_size, name="layer3"),
            ]
        )
        self.model.compile(
            optimizer='adam',
            loss='mean_squared_error'
        )

    def train(self):
        self.model.fit(self.train_x, self.train_y, validation_split=0.2, epochs=30)

    def predict(self):
        pass

    
    def preprocessing(self):
        normalize = preprocessing.Normalization()
        normalize.adapt(self.train_x)
        self.train_y = pre.normalize(self.train_y, norm="l1")
        print(self.train_y[0])

    
    def load_dataset_from_csv(self):
        filename_x = 'hex_dataset_x.csv'
        filename_y = 'hex_dataset_y.csv'
        raw_data_x = open(filename_x, 'rt')
        raw_data_y = open(filename_y, 'rt')
        self.train_x = np.loadtxt(raw_data_x, delimiter=",")
        self.train_y = np.loadtxt(raw_data_y, delimiter=",")
        print(self.train_x.shape)



if __name__ == "__main__":
    network = hex_neural_network(16)
    network.load_dataset_from_csv()
    network.preprocessing()
    network.train()
