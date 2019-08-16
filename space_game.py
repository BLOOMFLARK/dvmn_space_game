import curses
import time
import asyncio
import random
from curses_tools import draw_frame, read_controls, get_frame_size


async def blink(canvas, row, column, symbol='*'):
    latency = random.randint(0, 100)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        latency = random.randint(0, 1)
        for _ in range(20):
            await asyncio.sleep(0) 

        for _ in range(latency):
            await asyncio.sleep(0)	
           
        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(5):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


async def animate_spaceship(canvas, row, column):
    # with open("rocket_frame_1.txt") as file1:
	    # frame1 = file1.read()

    # with open("rocket_frame_2.txt") as file1:
        # frame2 = file2.read()

    frame1 = """  .
 .'.
 |o|
.'o'.
|.-.|
'   '
 ( )
  )
 ( )"""
    frame2 = """  .
 .'.
 |o|
.'o'.
|.-.|
'   '
  )
 ( )
  ("""
    frame_rows, frame_columns = get_frame_size(frame1)
    max_row, max_column = canvas.getmaxyx()
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        
        if row + rows_direction + frame_rows < max_row and -1 < row + rows_direction:
            row += rows_direction
        if column + columns_direction + frame_columns < max_column and 0 < column + columns_direction:
            column += columns_direction    

        
        draw_frame(canvas, row, column, frame1)
        canvas.refresh()  
        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame1, negative=True)
        draw_frame(canvas, row, column, frame2)
        canvas.refresh()  
        for _ in range(2):
            await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame2, negative=True)



def draw(canvas):
    stars = '+*.:'
    TIC_TIMEOUT = 0.1
    curses.curs_set(False)
    canvas.border()
    canvas.nodelay(True)

    max_y, max_x = canvas.getmaxyx()
    num_of_stars = random.randint(100, 200)
    
    coroutines = []
    for _ in range(num_of_stars):
        star = random.choice(stars)
        row = random.randint(1, max_y - 2)
        column = random.randint(1, max_x - 2)
        coroutines.append(blink(canvas, row, column, symbol=star))

    blast = fire(canvas, round(max_y / 2), round(max_x / 2))
    rocket = animate_spaceship(canvas, round(max_y / 2), round(max_x / 2)) 

    while True:
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()
        for coroutine in coroutines:
            coroutine.send(None)
            canvas.refresh()

        rocket.send(None)

        try:
            blast.send(None)
        except StopIteration:
            break   



async def fire(canvas, start_row, start_column, rows_speed=-0.05,  columns_speed=0):
    row, column = start_row, start_column, 

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def blinking_star():
    while (True):
    # adds string on (x,y) = (row, column)
        canvas.addstr(row, column, '*', curses.A_DIM)
        canvas.refresh()
        time.sleep(2)

        canvas.addstr(row, column, '*')
        canvas.refresh()
        time.sleep(0.3)

        canvas.addstr(row, column, '*', curses.A_BOLD)
        canvas.refresh()
        time.sleep(0.5)

        canvas.addstr(row, column, '*')
        canvas.refresh()
        time.sleep(0.3)    


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

