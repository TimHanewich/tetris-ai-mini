import tetris

while True:
    gs = tetris.GameState()
    
    while True:
        print("Board:")
        print(str(gs))

        i:str = input("How many shifts? > ")
        shifts:int = int(i)
        reward = gs.drop(shifts)
        print("REWARD: " + str(reward))

        # if game over
        if gs.over():
            print("Game over!")
            print("Score: " + str(gs.score()))
            input("Enter to go to next game.")
            gs = tetris.GameState()