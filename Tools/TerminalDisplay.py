import curses
import time
headPositions = [0,1,2]

def arrowPlotter(arrowBox,headPositions):
    truncatedHeadPosition = [0,0]
    truncatedHeadPosition[0] = headPositions[0]
    truncatedHeadPosition[1] = headPositions[1]

    if (truncatedHeadPosition == [0,0]): #Up-Left
        arrowBox.addstr(1,1,". . . .\n . .\n .   .\n .     .\n         .")
    elif (truncatedHeadPosition == [0,1]): #Up-Center
        arrowBox.addstr(1,1,"    .\n    ...\n   . . .\n  .  .  .\n     .")
    elif (truncatedHeadPosition == [0,2]): #Up-Right
        arrowBox.addstr(1,1,"  . . . .\n       . .\n     .   .\n   .     .\n .")
    elif (truncatedHeadPosition == [1,0]): #Middle-Left
        arrowBox.addstr(1,1,"    .\n   .\n . . . . .\n   .\n     .")
    elif (truncatedHeadPosition == [1,1]): #Middle-Center
        arrowBox.addstr(1,1,"    _\n  /  .  \ \n |  o o  |\n  \  _  /")
    elif (truncatedHeadPosition == [1,2]): #Middle-Right
        arrowBox.addstr(1,1,"    .\n       .\n . . . . .\n       .\n     .")
    elif (truncatedHeadPosition == [2,0]): #Down-Left
        arrowBox.addstr(1,1,"        .\n .     .\n .   .\n . .\n . . . .")
    elif (truncatedHeadPosition == [2,1]): #Down-Center
        arrowBox.addstr(1,1,"    .\n  .  .  .\n   . . .\n    ...\n     .")
    elif (truncatedHeadPosition == [2,2]): #Down-Right
        arrowBox.addstr(1,1,".\n   .     .\n     .   .\n       . .\n   . . . .")

    arrowBox.addstr(6,1,"----------")

    if (headPositions[2] == 0):
        arrowBox.addstr(7,1," Tilted\n   Left")
    elif (headPositions[2] == 1):
        arrowBox.addstr(7,1," Tilted\n  Straight")
    elif (headPositions[2] == 2):
        arrowBox.addstr(7,1," Tilted\n   Right")



def main():
    testvar = 1

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    stdscr.timeout(150)

    stdscr.addstr(15,1,str(testvar))
    arrowBox = curses.newwin(10, 11, 1, 1)

    arrowPlotter(arrowBox,headPositions)

    arrowBox.box()

    stdscr.refresh()
    arrowBox.refresh()
    stdscr.refresh()

    running = True
    while (running ):
        #Arrow in Box1 (topleft)
        #if (headPositions == []
        testvar = testvar + 1
        stdscr.addstr(15,1,str(testvar))
        stdscr.refresh()


        key = stdscr.getch()
        if ( key == 27 ):
            running = False
            break

    curses.endwin()

if __name__ == "__main__":
        main()
