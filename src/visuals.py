import tetris
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

def genimg(gs:tetris.GameState, save_path:str, hightlight_square:tuple[int,int] = None, game_number:int = None) -> None:
    grid_img_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai-mini\assets\grid.png"
    img:PIL.Image.Image = PIL.Image.open(grid_img_path)

    # fill squares
    for ri in range(0, len(gs.board)):
        for ci in range(0, len(gs.board[ri])):
            if gs.board[ri][ci]:
                if hightlight_square != None and hightlight_square[0] == ri and hightlight_square[1] == ci:
                    fillsquare(img, ri, ci, (255,0,0))
                else: # fill with normal color
                    fillsquare(img, ri, ci)

    # draw the score
    draw:PIL.ImageDraw.Draw = PIL.ImageDraw.Draw(img)
    draw.text((0,543), "SCORE: " + str(gs.score()), (127, 127, 127), font=PIL.ImageFont.truetype("arial.ttf", 36))

    # print game number?
    if game_number != None:
        draw.text((0, 505), "GAME: " + str(game_number), (127,127,127), font=PIL.ImageFont.truetype("arial.ttf", 36))

    img.save(save_path)
    
def fillsquare(img:PIL.Image.Image, row:int, col:int, color:tuple[int, int, int] = (153,223,225)) -> None:
    
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
            img.putpixel((x,y), color)