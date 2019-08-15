import curses
import time
import asyncio


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
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()
    TIC_TIMEOUT = 0.1
    
    star = blink(canvas, row, column)
    coroutines = [blink(canvas, row, column + 2*j) for j in range(5)]
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

