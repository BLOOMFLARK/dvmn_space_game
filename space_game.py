import curses
import time
import asyncio
import random


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
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
    stars = '+*.:'
    TIC_TIMEOUT = 0.1
    curses.curs_set(False)
    canvas.border()

    max_y, max_x = canvas.getmaxyx()
    num_of_stars = random.randint(100, 200)
    
    coroutines = []
    for _ in range(num_of_stars):
        star = random.choice(stars)
        row = random.randint(0, max_y - 2)
        column = random.randint(0, max_x - 2)
        coroutines.append(blink(canvas, row, column, symbol=star))

    canvas.refresh()

    while True:
    	time.sleep(TIC_TIMEOUT)
    	canvas.refresh()
    	for coroutine in coroutines:
            coroutine.send(None)
            canvas.refresh()	



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

