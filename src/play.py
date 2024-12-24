import tetris

while True:
    gs = tetris.GameState()
    
    while True:
        print("Board:")
        print(str(gs))
        print("Current Score: " + str(gs.score()))
        print("Current Reward: " + str(round(gs.score_plus(), 1)))

        i:str = input("How many shifts? > ")
        shifts:int = int(i)
        gs.drop(shifts)

        # if game over
        if gs.over():
            print("Game over!")
            print("Score: " + str(gs.score()))
            input("Enter to go to next game.")
            gs = tetris.GameState()