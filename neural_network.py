import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class hex_neural_network:
    def __init__(self, train_x, train_y, grid_size):
        self.train_x = train_x
        self.train_y = train_y
        self.grid_size = grid_size
        self.model = keras.Sequential(
            [
                layers.Dense(2, activation="relu", input_shape=(self.grid_size,), name="layer1"),
                layers.Dense(3, activation="relu", name="layer2"),
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