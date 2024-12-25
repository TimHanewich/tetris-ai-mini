import intelligence
import tetris
import representation

save_path = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\checkpoints\checkpoint16.keras"
tai = intelligence.TetrisAI(save_path)

while True:
    gs = tetris.GameState()
    while True:

        print("Board:")
        print(str(gs))

        # get move
        predictions:list[float] = tai.predict(representation.BoardState(gs))
        shift:int = predictions.index(max(predictions))
        print("Move: " + str(shift))
        input("Enter to execute the move it selected")

        # make move
        gs.drop(shift)

        # if game over
        if gs.over():
            print(str(gs))
            print("Game is over!")
            print("Final score: " + str(gs.score()))
            print("Going to next game...")
            gs = tetris.GameState()

