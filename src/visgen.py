import visuals
import tetris
import intelligence
import representation
import random

model_save_path = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\checkpoint16.keras"
images_save_folder = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\game_images"

print("Loading model...")
tai = intelligence.TetrisAI(model_save_path)

onGame:int = 1
gs = tetris.GameState()
for i in range(0, 100):
    print("On move " + str(i) + "... ")

    # get move
    predictions:list[float] = tai.predict(representation.BoardState(gs))
    shift:int = predictions.index(max(predictions))

    # make move
    gs.drop(shift)

    # determine which square that was just filled in that we should highlight
    cds:list[int] = gs.column_depths()
    highlight:tuple[int, int] = (cds[shift], shift)

    # save image of game
    path = images_save_folder + "\\" + f"{i:06d}" + ".png"
    visuals.genimg(gs, path, highlight, onGame)
    
    # game over?
    if gs.over():
        print("Game over! Going to next game.")
        gs = tetris.GameState()
        if random.random() <= 0.95:
            gs.randomize()
        onGame = onGame + 1