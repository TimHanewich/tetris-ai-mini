import visuals
import tetris
import intelligence
import representation
import random

model_save_path = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\checkpoint16.keras"
print("Loading model...")
tai = intelligence.TetrisAI(model_save_path)

gs = tetris.GameState()
for i in range(0, 500):
    print("On move " + str(i) + "... ")

    # save image of game
    path = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\game_images" + "\\" + f"{i:06d}" + ".png"
    visuals.genimg(gs, path)
    
    # get move
    predictions:list[float] = tai.predict(representation.BoardState(gs))
    shift:int = predictions.index(max(predictions))

    # make move
    gs.drop(shift)
    
    # game over?
    if gs.over():
        print("Game over! Going to next game.")
        gs = tetris.GameState()
        if random.random() <= 0.95:
            gs.randomize()