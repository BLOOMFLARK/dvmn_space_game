import curses
import time
import asyncio


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        # прерывает исполнение и дает управление родительсокму потоку (типа ретерна)
        # каждый раз при запуске корутины она будет продолжать работу с места последнего await
        # - чстой воды генератор, где await == yield, но возвращает не итерируемый объект а управление потоком
        await asyncio.sleep(0) # дай поработать другим

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)




def draw(canvas):
    row, column = (5, 20)
    curses.curs_set(False)
    canvas.border()
    
    star = blink(canvas, row, column)

    star.send(None)
    canvas.refresh()
    time.sleep(2)

    star.send(None)
    canvas.refresh()
    time.sleep(0.3)

    star.send(None)
    canvas.refresh()
    time.sleep(0.5)

    star.send(None)
    canvas.refresh()
    time.sleep(0.3)


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

