import intelligence
import tetris

save_path = r""
tai = intelligence.TetrisAI(save_path)

while True:
    gs = tetris.GameState()
    while True:

        print("Board:")
        print(str(gs))

        # get move
        predictions:list[float] = tai.predict(gs)
        shift:int = predictions.index(max(predictions))
        print("Move: " + str(shift))
        input("Enter to execute the move it selected")

        # make move
        gs.drop(shift)

        # if game over
        if gs.over():
            print("Game is over!")
            print("Final score: " + str(gs.score()))
            print("Going to next game...")
            gs = tetris.GameState()

