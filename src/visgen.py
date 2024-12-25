import visuals
import tetris
import intelligence
import representation
import random
import os

### SETTINGS ###
model_save_path = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\checkpoint16.keras"
images_save_folder = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\game_images"
################

if os.path.exists(images_save_folder) == False:
    os.mkdir(images_save_folder)

print("Loading model...")
tai = intelligence.TetrisAI(model_save_path)

# variables for tracking
onFrame:int = 0
onGame:int = 1

def next_save_path() -> str:
    global onFrame
    path = images_save_folder + "\\" + f"{onFrame:06d}" + ".png"
    onFrame = onFrame + 1
    return path

# generate!
gs:tetris.GameState = tetris.GameState()
for i in range(0, 60):

    print("On move " + str(i) + "... ")

    # create next game if needed
    if gs == None or gs.over():
        print("We need to generate a new game!")
        gs = tetris.GameState()
        if random.random() <= 0.95:
            gs.randomize()
        onGame = onGame + 1

        # generate a few frames of this starting space so that way the observer can see the ending spot.
        for _ in range(0, 8):
            visuals.genimg(gs, next_save_path(), None, onGame)

    # get move
    predictions:list[float] = tai.predict(representation.BoardState(gs))
    shift:int = predictions.index(max(predictions))

    # make move
    gs.drop(shift)

    # determine which square that was just filled in that we should highlight
    cds:list[int] = gs.column_depths()
    highlight:tuple[int, int] = (cds[shift], shift)

    # save image of game
    visuals.genimg(gs, next_save_path(), highlight, onGame)

    # if that last move the model played ended the game (now 16 squares are filled), generate a few more frames
    if gs.over():
        for _ in range(0, 5):
            visuals.genimg(gs, next_save_path(), highlight, onGame)