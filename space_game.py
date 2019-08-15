import curses
import time


def draw(canvas):
    row, column = (5, 20)
    canvas.border()
    # no blinking cursor
    curses.curs_set(False)
    
    # adds string on (x,y) = (row, column)
    canvas.addstr(row, column, 'Hello World')

    # make the string appear on the screen
    canvas.refresh()

    time.sleep(3)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)

