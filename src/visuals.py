import tetris
import PIL.Image

def genimg(gs:tetris.GameState, save_path:str) -> None:
    grid_img_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\assets\grid.png"
    img:PIL.Image.Image = PIL.Image.open(grid_img_path)

    # fill squares
    for ri in range(0, len(gs.board)):
        for ci in range(0, len(gs.board[ri])):
            if gs.board[ri][ci]:
                fillsquare(img, ri, ci)

    img.save(save_path)
    
def fillsquare(img:PIL.Image.Image, row:int, col:int) -> None:
    
    # settings (custom to the grid image)
    top_left_corner_xy:int = 98  # where the top left corner of the top left square starts
    square_height_width:int = 92 # the width/height of each square
    border_thickness:int = 4 # the border width of the table that separates each square.

    # determine top left corner (where to start)
    start_y:int = top_left_corner_xy + ((square_height_width + border_thickness) * row)
    start_x:int = top_left_corner_xy + ((square_height_width + border_thickness) * col)
    stop_y:int = start_y + square_height_width
    stop_x:int = start_x + square_height_width

    for x in range(start_x, stop_x):
        for y in range(start_y, stop_y):
            img.putpixel((x,y), (153,223,225))