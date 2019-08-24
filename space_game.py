import curses
import time
import asyncio
import random
from curses_tools import draw_frame, read_controls, get_frame_size


STARS = '+*.:'
TIC_TIMEOUT = 0.1
NUM_OF_STARS = random.randint(100, 200)


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


def check_ship_inside_border(current_coordinate, step, frame_size, border) -> bool:
    """ Checks if frame does not exceed border limit in 1 Dimension! """
    return current_coordinate + step + frame_size < border and 0 < current_coordinate + step:


async def animate_spaceship(canvas, row, column):
    with open("/Users/mac/git_projects/dvmn_space_game/frames/rocket_frame_1.txt") as file1:
        frame1 = file1.read()

    with open("/Users/mac/git_projects/dvmn_space_game/frames/rocket_frame_2.txt") as file2:
        frame2 = file2.read()

    frame_rows, frame_columns = get_frame_size(frame1)

    max_row, max_column = canvas.getmaxyx()

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        if check_ship_inside_border(current_coordinate=row, step=rows_direction, frame_size=frame_rows, border=max_row):
            row += rows_direction
        if check_ship_inside_border(current_coordinate=column, step=columns_direction, frame_size=frame_columns, border=max_column):
            column += columns_direction    
        draw_frame(canvas, row, column, frame1)
        canvas.refresh()  

        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame1, negative=True)
        draw_frame(canvas, row, column, frame2)
        canvas.refresh()  

        await asyncio.sleep(0)

        draw_frame(canvas, row, column, frame2, negative=True)


async def blink(canvas, row, column, offset_tics, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)

        for _ in range(offset_tics):
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


def draw(canvas):
    curses.curs_set(False)

    canvas.border()
    canvas.nodelay(True)

    max_y, max_x = canvas.getmaxyx()
    center_y, center_x = round(max_y / 2), round(max_x / 2)
    
    coroutines = []
    for _ in range(NUM_OF_STARS):
        offset_tics = random.randint(0, 100)
        star = random.choice(STARS)
        row = random.randint(1, max_y - 2)
        column = random.randint(1, max_x - 2)
        coroutines.append(blink(canvas, row, column, symbol=star, offset_tics=offset_tics))

    rocket = animate_spaceship(canvas, center_y, center_x)
    coroutines.append(rocket)

    while True:
        time.sleep(TIC_TIMEOUT)
        canvas.refresh()
        for coroutine in coroutines:
            coroutine.send(None)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

