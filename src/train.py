import intelligence
import tetris
import sys
import representation
import math
import collections
import random
import tools

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\log.txt" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# training settings
gamma:float = 0.5
epsilon:float = 0.2

# training config
batch_size:int = 100 # the number of experiences that will be collected and trained on
save_model_every_experiences:int = 5000
################

# construct/load model
tai:intelligence.TetrisAI = None
if model_save_path != None and model_save_path != "":
    print("Loading model checkpoint at '" + model_save_path + "'...")
    tai = intelligence.TetrisAI(model_save_path)
    print("Model loaded!")
else:
    print("Constructing new model...")
    tai = intelligence.TetrisAI()  

# variables to track
experiences_trained:int = 0 # the number of experiences the model has been trained on
model_last_saved_at_experiences_trained:int = 0 # the last number of experiences that the model was trained on
on_checkpoint:int = 0

# training loop
while True:

    # collect X number of experiences
    gs:tetris.GameState = tetris.GameState()
    experiences:list[intelligence.Experience] = []
    for ei in range(0, batch_size):

        # print!
        sys.stdout.write("\r" + "Collecting experience " + str(ei+1) + " / " + str(batch_size) + "... ")
        sys.stdout.flush()

        # get board representation
        state_board:list[int] = representation.BoardState(gs)

        # select move to play
        move:int
        if random.random() < epsilon: # if by chance we should select a random move
            move = random.randint(0, 3) # choose move at random
        else:
            predictions:list[float] = tai.predict(state_board) # predict Q-Values
            move = predictions.index(max(predictions)) # select the move (index) with the highest Q-Value

        # play the move
        IllegalMovePlayed:bool = False
        MoveReward:float
        try:
            MoveReward = gs.drop(move)
        except tetris.InvalidDropException as ex: # the model (or at random) tried to play an illegal move
            IllegalMovePlayed = True
            MoveReward = -3.0 # small penalty for illegal moves
        except Exception as ex:
            print("Unhandled exception in move execution: " + str(ex))
            input("Press enter key to continue, if you want to.")
        
        # store this experience
        exp:intelligence.Experience = intelligence.Experience()
        exp.state = state_board
        exp.action = move
        exp.reward = MoveReward
        exp.next_state = representation.BoardState(gs) # the state we find ourselves in now.
        exp.done = gs.over() or IllegalMovePlayed # it is over if the game is completed OR an illegal move was played
        experiences.append(exp)

        # if game is over or they played an illegal move, reset the game!
        if gs.over() or IllegalMovePlayed:
            gs = tetris.GameState()
    print()

    # print avg rewards
    rewards:float = 0.0
    for exp in experiences:
        rewards = rewards + exp.reward
    status:str = "Average reward over those " + str(len(experiences)) + " experiences on model w/ " + str(experiences_trained) + " trained experiences: " + str(round(rewards / len(experiences), 2))
    tools.log(log_file_path, status)
    print(status)
    
    # train!
    for ei in range(0, len(experiences)):
        exp = experiences[ei]

        # print training number
        sys.stdout.write("\r" + "Training on experience " + str(ei+1) + " / " + str(len(experiences)) + "... ")
        sys.stdout.flush()

        # determine new target based on the game ending or not (maybe we should factor in future rewards, maybe we shouldnt)
        new_target:float
        if exp.done:
            new_target = exp.reward
        else:
            max_q_of_next_state:float = max(tai.predict(exp.next_state))
            new_target = exp.reward + (gamma * max_q_of_next_state) # blend immediate vs. future rewards

        # ask the model to predict again for this experiences state
        qvalues:list[float] = tai.predict(exp.state)

        # plug in the new target where it belongs
        qvalues[exp.action] = new_target

        # now train on the updated qvalues (with 1 changed)
        tai.train(exp.state, qvalues)
        experiences_trained = experiences_trained + 1
    print("Training complete!")

    # save model?
    if (experiences_trained - model_last_saved_at_experiences_trained) >= save_model_every_experiences:
        print("Time to save model!")
        path:str = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\checkpoint" + str(on_checkpoint) + ".keras"
        tai.save(path)
        print("Checkpoint # " + str(on_checkpoint) + " saved to " + path + "!")
        on_checkpoint = on_checkpoint + 1
        model_last_saved_at_experiences_trained = experiences_trained
        print("Model saved to " + path + "!")