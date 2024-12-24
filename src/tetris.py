import statistics

class InvalidDropException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class GameState:

    def __init__(self):
        self.board:list[list[bool]] = [[False,False,False,False],[False,False,False,False],[False,False,False,False],[False,False,False,False]] # 4 rows of 4 columns, 4x4
    
    def __str__(self):
        ToReturn:str = ""
        ToReturn = " ┌────┐" + "\n"
        onRow:int = 0
        for row in self.board:

            # add the row number in
            ToReturn = ToReturn + str(onRow) + "│"
            

            # print every square
            for column in row:
                if column:
                    ToReturn = ToReturn + "█"
                else:
                    ToReturn = ToReturn + " "
            ToReturn = ToReturn + "│\n"
            onRow = onRow + 1
        ToReturn = ToReturn + " └────┘"
        ToReturn = ToReturn + "\n" + "  0123"
        return ToReturn

    def column_depths(self) -> list[int]:
        """Calculates how 'deep' the available space on each column goes, from the top down."""

        # record the depth of every column
        column_depths:list[int] = [0,0,0,0]
        column_collisions:list[bool] = [False, False, False, False] # records whether we have "reached the floor" of this column, a.k.a. reached a square that is occupied.

        # find the depth of each column 
        # In this sense, "depth" is the number of squares that are clear, to be clear
        for ri in range(0, len(self.board)): # for every row   
            for ci in range(0, len(self.board[0])): # for every column (use first row to know how many columns there are)
                if column_collisions[ci] == False and self.board[ri][ci] == False: # if column X has not been recorded yet and the column in this row is not occupied, increment the depth
                    column_depths[ci] = column_depths[ci] + 1
                else: # we hit a floor!
                    column_collisions[ci] = True

        return column_depths
    
    def over(self) -> bool:
        """Determines the game is over (if all cols in top row are occupied)."""
        return self.board[0] == [1,1,1,1]
    
    def drop(self, column:int) -> float:
        """Drops a single block into the column, returns the reward of doing so."""
        if column < 0 or column > 3:
            raise InvalidDropException("Invalid move! Column to drop in must be 0, 1, 2, or 3.")
        
        reward_before:float = self.score_plus()
        cds:list[int] = self.column_depths()
        if cds[column] == 0:
            raise InvalidDropException("Unable to drop on column " + str(column) + ", it is already full!")
        self.board[cds[column]-1][column] = True
        reward_after:float = self.score_plus()
        return reward_after - reward_before

    def score(self) -> int:
        ToReturn:int = 0
        for row in self.board:
            for col in row:
                if col:
                    ToReturn = ToReturn + 1
        return ToReturn
    
    def score_plus(self) -> float:
        
        # start at score
        ToReturn:float = float(self.score())

        # penalize for standard deviation
        stdev:float = statistics.pstdev(self.column_depths())
        ToReturn = ToReturn - (stdev * 2)

        return ToReturn