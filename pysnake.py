import curses
import time
import random
import string
import sys

def clean_snake(win, snake):
    for i in snake:
        win.addch(i[0], i[1], ' ')

def create_snake(win, snake):
    for i in snake:
        win.addch(i[0], i[1], '#')
        
def create_apple(win):
    height, width = win.getmaxyx()
    y = -1
    x = -1
    while not (2 < y < height - 1 and 2 < x < width - 1):
                y = int(random.random() * height)
                x = int(random.random() * width)               
    
    win.addch(y, x, '@', curses.color_pair(1))
    win.refresh()
    
    return y, x
    
def main(stdscr_d):
    curses.init_pair(1, curses.COLOR_RED, 0)
    stdscr = stdscr_d.subwin(30, 40, 0, 0)
    info = stdscr_d.subwin(25, 50, 0, 42)
    stdscr.keypad(1)
    
    score = 0
    snake = [(10, 10)]
    stdscr.addch(snake[0][0], snake[0][1] , '#')
    
    curses.curs_set(0)
    stdscr.timeout(0)
    stdscr.border(0, 0, 0, 0, '+', '+', '+', '+')
    info.border(0, 0, 0, 0, '+', '+', '+', '+')
    height, width = stdscr.getmaxyx()
    info.addstr(2, 2, 'Score: %d' % (score))
    info.addstr(3, 2, 'Snake Lenght: %d' % (len(snake)))
    
    info.refresh()
    stdscr.refresh()
    
    ay, ax = create_apple(stdscr)
    key = curses.KEY_RIGHT
    
    
    while True:
        time.sleep(0.1)
        c = stdscr.getch()
        
        if c != -1:
            key = c
        
        if stdscr.inch(ay, ax) != 320:
            ay, ax = create_apple(stdscr)
            score += 9
            info.addstr(2, 2, 'Score: %d' % (score))
            info.addstr(3, 2, 'Snake Lenght: %d' % (len(snake)))
            info.refresh()
        
        clean_snake(stdscr, snake)
        
        if key == ord('q'):
            break
            
        elif key == curses.KEY_DOWN:
            y = snake[0][0] + 1
            x = snake[0][1]
            
        elif key == curses.KEY_UP:
            y = snake[0][0] - 1
            x = snake[0][1]            
            
        elif key == curses.KEY_LEFT:
            y = snake[0][0]
            x = snake[0][1] - 1
            
        elif key == curses.KEY_RIGHT:
            y = snake[0][0]
            x = snake[0][1] + 1
        
        if (0 >= x or x >= width -1 or 
            0 >= y  or y >= height -1 or
            (y, x) in snake):
            stdscr.timeout(-1)
            info.addstr(12, 18, 'Game Over!!!')
            info.addstr(13, 17, 'Press q to quit')
            info.refresh()
            c = stdscr.getch()
            while c != ord('q'):
                c = stdscr.getch()
            break
        
        snake.insert(0, (y, x))
        if len(snake) > 1 and stdscr.inch(y, x) != 320:
            snake.pop()            
            
        create_snake(stdscr, snake)
        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)