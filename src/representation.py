import tetris

def BoardState(gs:tetris.GameState) -> list[int]:
    """Represents the board as a state of flattened integers."""
    ToReturn:list[int] = []
    for row in gs.board:
        for col in row:
            ToReturn.append(int(col))
    return ToReturn