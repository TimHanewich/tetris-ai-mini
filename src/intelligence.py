import keras
import numpy

class Experience:
    def __init__(self):
        self.state:list[int] = None
        self.action:int = None
        self.reward:float = None
        self.next_state:list[int] = None
        self.done:bool = False

class TetrisAI:

    def __init__(self, save_file_path:str = None):

        # if there is a save_file_path provided, load that
        if save_file_path != None:
            self.model = keras.models.load_model(save_file_path) # load from file path
        else:

            # built layers
            input_board = keras.layers.Input(shape=(16,), name="input_board")
            carry = keras.layers.Dense(64, "relu", name="layer1")(input_board)
            carry = keras.layers.Dense(64, "relu", name="layer2")(carry)
            carry = keras.layers.Dense(32, "relu", name="layer3")(carry)
            output = keras.layers.Dense(4, "linear", name="output")(carry)

            # construct the model
            self.model = keras.Model(inputs=input_board, outputs=output)
            self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.003), loss="mse")

    def save(self, path:str) -> None:
        """Saves the keras model to file"""
        self.model.save(path)

    def predict(self, board:list[int]) -> list[float]:
        """Performs a forward pass through the neural net to predict the Q-values (current/future rewards) of each potential next move (shift) given the current state, returning as an array of floating point numbers."""
        x = numpy.array([board])
        prediction = self.model.predict(x, verbose=False)
        vals:list[float] = prediction[0].tolist() # the "tolist()" function just converts it from a numpy.darray to a normal list of floats!
        return vals
    
    def train(self, board:list[int], qvalues:list[float]) -> None:
        x = numpy.array([board])
        y = numpy.array([qvalues])
        self.model.fit(x, y, epochs=1, verbose=False)