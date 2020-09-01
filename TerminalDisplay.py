import curses
import time
import config

def arrowPlotter(arrowBox,headPositions):
    truncatedHeadPosition = [0,0]
    truncatedHeadPosition[0] = headPositions[0]
    truncatedHeadPosition[1] = headPositions[1]

    if (truncatedHeadPosition == [0,2]): #Up-Left
        arrowBox.addstr(1,1,". . . .\n . .\n .   .\n .     .\n         .")
    elif (truncatedHeadPosition == [0,1]): #Up-Center
        arrowBox.addstr(1,1,"    .\n    ...\n   . . .\n  .  .  .\n     .")
    elif (truncatedHeadPosition == [0,0]): #Up-Right
        arrowBox.addstr(1,1,"  . . . .\n       . .\n     .   .\n   .     .\n .")
    elif (truncatedHeadPosition == [1,2]): #Middle-Left
        arrowBox.addstr(1,1,"    .\n   .\n . . . . .\n   .\n     .")
    elif (truncatedHeadPosition == [1,1]): #Middle-Center
        arrowBox.addstr(1,1,"    _\n  /  .  \ \n |  o o  |\n  \  _  /")
    elif (truncatedHeadPosition == [1,0]): #Middle-Right
        arrowBox.addstr(1,1,"    .\n       .\n . . . . .\n       .\n     .")
    elif (truncatedHeadPosition == [2,2]): #Down-Left
        arrowBox.addstr(1,1,"        .\n .     .\n .   .\n . .\n . . . .")
    elif (truncatedHeadPosition == [2,1]): #Down-Center
        arrowBox.addstr(1,1,"    .\n  .  .  .\n   . . .\n    ...\n     .")
    elif (truncatedHeadPosition == [2,0]): #Down-Right
        arrowBox.addstr(1,1,".\n   .     .\n     .   .\n       . .\n   . . . .")

    arrowBox.addstr(6,1,"----------")

    if (headPositions[2] == 2):
        arrowBox.addstr(7,1," Tilted\n   Left          ")
    elif (headPositions[2] == 1):
        arrowBox.addstr(7,1," Tilted\n  Straight")
    elif (headPositions[2] == 0):
        arrowBox.addstr(7,1," Tilted\n   Right         ")



def TerminalStarter():

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    stdscr.timeout(150)
    curses.curs_set(0)
    screenHeight, screenWidth = stdscr.getmaxyx()

    #Title Box
    titleBox = curses.newwin(10, screenWidth, 1, 1)

    titleBox.addstr(1,1,"  ____        _     _     _         _____            _             _    _____           _\n  |  _ \      | |   | |   | |       / ____|          | |           | |  / ____|         | |\n  | |_) |_   _| |__ | |__ | | ___  | |     ___  _ __ | |_ _ __ ___ | | | |     ___ _ __ | |_ ___ _ __\n  |  _ <| | | | '_ \| '_ \| |/ _ \ | |    / _ \| '_ \| __| '__/ _ \| | | |    / _ \ '_ \| __/ _ \ '__|\n  | |_) | |_| | |_) | |_) | |  __/ | |___| (_) | | | | |_| | | (_) | | | |___|  __/ | | | ||  __/ |\n  |____/ \__,_|_.__/|_.__/|_|\___|  \_____\___/|_| |_|\__|_|  \___/|_|  \_____\___|_| |_|\__\___|_|")
    titleBox.box()

    #Arrow Box (top left)
    arrowHeaderBox = curses.newwin(4,11,11,1)
    arrowHeaderBox.addstr(1,1,"Current\n Position")
    arrowBox = curses.newwin(10, 11, 15, 1)
    arrowPlotter(arrowBox,config.currentHeadPosition)
    arrowBox.box()
    arrowHeaderBox.box()

    stdscr.refresh()
    arrowBox.refresh()
    arrowHeaderBox.refresh()
    titleBox.refresh()
    stdscr.refresh()

    running = True
    previousHeadPosition = config.currentHeadPosition
    while (running ):
        #Arrow in Box1 (topleft)
        #if (headPositions == []
        if(previousHeadPosition != config.currentHeadPosition):
            arrowBox.clear()
            arrowPlotter(arrowBox,config.currentHeadPosition)
            arrowBox.box()
            arrowBox.refresh()
            #stdscr.refresh()
            previousHeadPosition = config.currentHeadPosition


        key = stdscr.getch()
        if ( key == 27 ):
            running = False
            break

    curses.endwin()
