import curses
import curses.ascii
import random
import sys

def clean_snake(win, snake):
    for i in snake:
        win.addch(i[0], i[1], ' ')
    win.refresh()
        
def update_snake(win, snake):
    win.addch(snake[0][0], snake[0][1], '#')
    win.addch(snake[-1][0], snake[-1][1], ' ')
    win.refresh()

def create_snake(win, snake):
    for i in snake:
        win.addch(i[0], i[1], '#')
    win.refresh()
        
def create_apple(win):
    height, width = win.getmaxyx()
    y = -1
    x = -1
                
    while win.inch(y, x) != ord(' '):
        y = int(random.random() * height)
        x = int(random.random() * width)
        
    win.addch(y, x, '@', curses.color_pair(1))
    win.refresh()

    return y, x

def main(stdscr_d):
    curses.init_pair(1, curses.COLOR_RED, 0)
    curses.init_pair(2, curses.COLOR_GREEN, 0)
    stdscr = stdscr_d.subwin(30, 40, 0, 0)
    info = stdscr_d.subwin(25, 50, 0, 42)
    stdscr.keypad(1)

    difficult = 1
    score = 0
    
    snake = [(10, 10), (10,9), (10,8)]
    create_snake(stdscr, snake)
    
    curses.curs_set(0)
    stdscr.timeout(0)
    stdscr.border(0, 0, 0, 0, '+', '+', '+', '+')
    info.border(0, 0, 0, 0, '+', '+', '+', '+')
    height, width = stdscr.getmaxyx()
    info.addstr(2, 2, 'Score: %d' % (score))
    info.addstr(3, 2, 'Snake Lenght: %d' % (len(snake)))
    info.addstr(4, 2, 'Difficult: %d' % (difficult))
    
    info.refresh()
    stdscr.refresh()
    
    #Ham... ham... apple
    create_apple(stdscr)

    key = curses.KEY_RIGHT
    last_key = key

    while True:        
        stdscr.timeout(int(100 - (7 * difficult)))
        key = stdscr.getch()
        stdscr.timeout(0)

        if key == ord('p'):
            stdscr.timeout(-1)
            info.addstr(12, 18, '==Pause==')
            info.refresh()
            valid_key = stdscr.getch()            
            stdscr.timeout(0)
            key = valid_key if valid_key in (curses.KEY_DOWN,
                                             curses.KEY_UP,
                                             curses.KEY_LEFT,
                                             curses.KEY_RIGHT, ord('q')) else last_key
            info.addstr(12, 18, '         ')
            info.refresh()
            last_key = key                                 
            

        elif key in (ord('+'), ord('-')):
            if key == ord('+') and difficult < 9:
               difficult += 1

            elif key == ord('-') and difficult > 1:
              difficult -= 1

            info.addstr(4, 2, 'Difficult: %d' % (difficult))
            info.refresh()
            key = last_key
            
        elif key == ord('q'):
            sys.exit(0)
            
        elif curses.ascii.isascii(key):
            key = last_key

        else:
           last_key = key


        
        if key == curses.KEY_DOWN:
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

        #Always include a new piece in the snake
        snake.insert(0, (y, x))
        
        #get the char in the position
        current_char = stdscr.inch(y, x)
        
        #Remove the last piece if not ate the apple
        if current_char == 32:
            update_snake(stdscr, snake)
            snake.pop()
        
        #Eating the apple... it's delicious
        elif current_char == 320:
            create_apple(stdscr)
            stdscr.addch(y, x, '@', curses.color_pair(2))            
            score += (3 * difficult)
            info.addstr(2, 2, 'Score: %d' % (score))
            info.addstr(3, 2, 'Snake Lenght: %d' % (len(snake)))
            info.refresh()
            
        else:
            #Everything that's not a empty space or a red apple ends the game
            update_snake(stdscr, snake)
            snake.pop()
            stdscr.timeout(400)
            info.addstr(12, 18, 'Game Over!!!')
            info.addstr(13, 17, 'Press q to quit')
            info.addstr(14, 17, 'Press n to restart')
            info.refresh()
            update_snake(stdscr, snake)
            stdscr.refresh()
            c = None
            while c not in (ord('q'), ord('n')):
                #Blink effect, nice but this code is ugly
                clean_snake(stdscr, snake)
                c = stdscr.getch()
                create_snake(stdscr, snake)
                c = c if c in (ord('q'), ord('n')) else stdscr.getch()
                
            if c == ord('q'):
                sys.exit(0)
            
            else:
                stdscr_d.clear()
                main(stdscr_d)


if __name__ == '__main__':
    try:
        curses.wrapper(main)

    except KeyboardInterrupt:
        sys.exit(0)
