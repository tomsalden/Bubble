import curses
import time
import config
import random
import img2ascii

import sys
import numpy as np

sys.path.append('home/pi/local/lib/python3.7/site-packages/cv2/python-3.7')
import cv2, queue, threading

# Create daemon for picamera, so no frames are missed when one is asked
class VideoCapture:
  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(3,160) # set Width
    self.cap.set(4,120) # set Height
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

class faceDetection:
    def __init__(self, cameraObject):
        self.cameraObect = cameraObject
        self.face_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_frontalface_alt.xml')
        self.profile_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_profileface.xml')
        self.eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_eye.xml')

        self.detected = 0
        self.faces = 0

        t = threading.Thread(target=self._detector)
        t.daemon = True
        t.start()

    def _detector(self):
        while True:
            img = self.cameraObect.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            self.faces = self.face_cascade.detectMultiScale(gray, 1.05, 5)
            if len(self.faces):
                self.detected = True
            else:
                self.eyes = self.eye_cascade.detectMultiScale(gray, 1.05, 5)
                if len(self.faces):
                    self.detected = True
                else:
                    profiles = self.profile_cascade.detectMultiScale(gray, 1.05, 5)
                    if len(self.faces):
                        self.detected = True
                    else:
                        self.detected = False

            time.sleep(1)

    def detect(self):
        return self.detected, self.faces



# Create the terminal boxes
def arrowPlotter(arrowBox,headPositions):
    truncatedHeadPosition = [0,0]
    truncatedHeadPosition[0] = headPositions[0]
    truncatedHeadPosition[1] = headPositions[1]
    arrowBox.addstr(1,1,"Current\n Position\n ")
    arrowBox.addstr("---------- ")
    arrowBox.clrtobot()


    if (truncatedHeadPosition == [0,2]): #Up-Left
        arrowBox.addstr(". . . .\n . .\n .   .\n .     .\n         .\n ")
    elif (truncatedHeadPosition == [0,1]): #Up-Center
        arrowBox.addstr("    .\n    ...\n   . . .\n  .  .  .\n     .\n ")
    elif (truncatedHeadPosition == [0,0]): #Up-Right
        arrowBox.addstr("  . . . .\n       . .\n     .   .\n   .     .\n .\n ")
    elif (truncatedHeadPosition == [1,2]): #Middle-Left
        arrowBox.addstr("    .\n   .\n . . . . .\n   .\n     .\n ")
    elif (truncatedHeadPosition == [1,1]): #Middle-Center
        arrowBox.addstr("    _\n  /  .  \ \n |  o o  |\n  \  _  /\n ")
    elif (truncatedHeadPosition == [1,0]): #Middle-Right
        arrowBox.addstr("    .\n       .\n . . . . .\n       .\n     .\n ")
    elif (truncatedHeadPosition == [2,2]): #Down-Left
        arrowBox.addstr("        .\n .     .\n .   .\n . .\n . . . .\n ")
    elif (truncatedHeadPosition == [2,1]): #Down-Center
        arrowBox.addstr("    .\n  .  .  .\n   . . .\n    ...\n     .\n ")
    elif (truncatedHeadPosition == [2,0]): #Down-Right
        arrowBox.addstr(".\n   .     .\n     .   .\n       . .\n   . . . .\n ")


    arrowBox.addstr(9,1,"\n ----------")

    if (headPositions[2] == 2):
        arrowBox.addstr(" Tilted\n   Left          ")
    elif (headPositions[2] == 1):
        arrowBox.addstr(" Tilted\n  Straight")
    elif (headPositions[2] == 0):
        arrowBox.addstr(" Tilted\n   Right         ")

    arrowBox.box()
    arrowBox.refresh()

def servoBoxPlotter(servoBox):
    h,w, = servoBox.getmaxyx()
    display = '#'
    yawRange = (w / float(config.yawMax - config.yawMin)) * (config.yawPosition - config.yawMin)
    yawPos = int(yawRange)

    pitchRange = (w / float(config.pitchMax - config.pitchMin)) * (config.pitchPosition - config.pitchMin)
    pitchPos = int(pitchRange)

    rollRange = (w / float(config.rollMax - config.rollMin)) * (config.rollPosition - config.rollMin)
    rollPos = int(rollRange)

    servoBox.addstr(1,1,"Servo range:\n ")
    servoBox.clrtobot()
    servoBox.hline("-",w)
    servoBox.addstr(4,1,"Yaw: " + str(config.yawPosition) + "\n ")
    servoBox.hline("-",w)
    servoBox.addstr("{}".format(display*yawPos))

    servoBox.addstr(7,1,"Pitch: " + str(config.pitchPosition) + "\n ")
    servoBox.hline("-",w)
    servoBox.addstr("{}".format(display*pitchPos))

    servoBox.addstr(10,1,"Roll: " + str(config.rollPosition) + "\n ")
    servoBox.hline("-",w)
    servoBox.addstr("{}".format(display*rollPos))

    servoBox.box()
    servoBox.refresh()

def currentModePlotter(modeWindow,mode):
    modeWindow.addstr(1,1,"Current\n Mode\n ")
    modeWindow.addstr("---------- ")
    modeWindow.clrtobot()
    if (mode == 'Random'):
        modeWindow.addstr("  ____\n  /\\' .\\\n /: \___\ \n \\' / . /\n  \/___/")
        modeWindow.addstr(11,1,"Random\n Mode")

    if (mode == 'Keyboard'):
        modeWindow.addstr("   __\n   (  )\n    ||\n  _|\"\"|_\n |______|")
        modeWindow.addstr(11,1,"Keyboard\n Mode")

    modeWindow.addstr(10,1,"---------- ")

    modeWindow.box()
    modeWindow.refresh()

def currentEmotionPlotter(emotionWindow,mode,nextMode,timetoNext):
    h,w, = emotionWindow.getmaxyx()
    emotionWindow.addstr(1,1,"Current\n emotion\n ")
    emotionWindow.clrtobot()
    emotionWindow.hline("-",w)
    emotionWindow.addstr(4,w//2 - len(mode)//2,mode)
    emotionWindow.addstr(6,1,"Time to\n next: ")
    emotionWindow.addstr(str(timetoNext))

    emotionWindow.addstr(9,1,"---------- ")
    emotionWindow.addstr("Next\n emotion:\n ")
    emotionWindow.addstr(12,w//2 - len(nextMode)//2,nextMode)


    emotionWindow.box()
    emotionWindow.refresh()

def menuPrinter(menuWindow,menuItems,menuHeader,selectedRow):
    h,w, = menuWindow.getmaxyx()
    menuWindow.addstr(1,w//2 - len(menuHeader)//2,menuHeader)
    #menuWindow.addstr(2,1,"--------")
    menuWindow.clrtobot()
    menuWindow.addstr("\n ")
    menuWindow.hline("-",w)

    for idx, row in enumerate(menuItems):
        x = w//2 - len(row)//2
        y = h//2 - len(menuItems)//2 + idx
        if idx == selectedRow:
            menuWindow.attron(curses.color_pair(1))
            menuWindow.addstr(y,x,row)
            menuWindow.attroff(curses.color_pair(1))
        else:
            menuWindow.addstr(y,x,row)

    menuWindow.box()
    menuWindow.refresh()

def imgPlotter(imgbox,ascii):
    imgbox.clrtobot()
    imgbox.addstr(1,1,"Webcam view:\n\n")
    for i in ascii:
        imgbox.addstr(i)
        imgbox.addstr("\n")

    imgbox.box()
    imgbox.refresh()

def activateImage(imgPlotterBox):
    if (config.cameraEnabled == False):

        config.cameraEnabled = True
    config.imageShow = not config.imageShow
    imgPlotterBox.addstr(1,1,"\n")
    imgPlotterBox.clrtobot()
    imgPlotterBox.addstr(6,42//2-1,"No\n")
    imgPlotterBox.addstr(7,42//2-3,"Image\n")
    imgPlotterBox.addstr(9,42//2-23//2,"Activate camera in menu")
    imgPlotterBox.box()
    imgPlotterBox.refresh()

def TerminalWrapped():
    localProgramMode = 'Random'
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(1)
    stdscr.timeout(300)
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    screenHeight, screenWidth = stdscr.getmaxyx()

    #Picam settings:
    cameraEnabled = False
    imageShow = False
    width = 40
    height = 30
    dim = (width, height)
    scale = 0.43
    cols = 40
    cap = VideoCapture(0)


    stdscr.refresh()



    #Title Box
    titleBox = curses.newwin(10, screenWidth-1, 1, 1)
    titleBox.addstr(1,1,"  ____        _     _     _         _____            _             _    _____           _\n  |  _ \      | |   | |   | |       / ____|          | |           | |  / ____|         | |\n  | |_) |_   _| |__ | |__ | | ___  | |     ___  _ __ | |_ _ __ ___ | | | |     ___ _ __ | |_ ___ _ __\n  |  _ <| | | | '_ \| '_ \| |/ _ \ | |    / _ \| '_ \| __| '__/ _ \| | | |    / _ \ '_ \| __/ _ \ '__|\n  | |_) | |_| | |_) | |_) | |  __/ | |___| (_) | | | | |_| | | (_) | | | |___|  __/ | | | ||  __/ |\n  |____/ \__,_|_.__/|_.__/|_|\___|  \_____\___/|_| |_|\__|_|  \___/|_|  \_____\___|_| |_|\__\___|_|")
    titleBox.box()
    titleBox.refresh()

    #Arrow Box (top left)
    arrowBox = curses.newwin(14, 11, 11, 1)
    arrowPlotter(arrowBox,config.currentHeadPosition)

    #ServospanBox
    servoBox = curses.newwin(14, 33, 25, 1)
    servoBoxPlotter(servoBox)

    #CurrentMode box
    currentMode = curses.newwin(14,11,11,12)
    currentModePlotter(currentMode,localProgramMode)

    #CurrentEmotion Box
    currentEmotion = curses.newwin(14,11,11,23)
    currentEmotionPlotter(currentEmotion,config.currentEmotion, config.nextEmotion, config.timetoNextEmotion)

    #Menu Box
    menuBox = curses.newwin(10,screenWidth-1,screenHeight-10,1)
    menu = ['Random Mode', 'Keyboard Mode', 'Camera on/off', 'Face detection on/off', 'Exit']
    menuBox.box()
    menuPosition = 0
    menuPrinter(menuBox,menu,'MenuTitle',menuPosition)

    #Image Plotter
    imgPlotterBox = curses.newwin(16,42,11,38)
    imgPlotterBox.addstr(6,42//2-1,"No\n")
    imgPlotterBox.addstr(7,42//2-3,"Image\n")
    imgPlotterBox.addstr(9,42//2-23//2,"Activate camera in menu")
    imgPlotterBox.box()
    imgPlotterBox.refresh()



    previousEmotionTime = config.timetoNextEmotion
    previousHeadPosition = config.currentHeadPosition
    localTime = time.time()

    localYaw = config.yawPosition
    localPitch = config.pitchPosition
    localRoll = config.rollPosition

    while (config.programRunning):

        #Replot arrowBox when position has changed
        if(previousHeadPosition != config.currentHeadPosition):
            arrowPlotter(arrowBox,config.currentHeadPosition)
            previousHeadPosition = config.currentHeadPosition

        #Replot servoBox when position has changed
        if(localYaw != config.yawPosition or localPitch != config.pitchPosition or localRoll != config.rollPosition):
            servoBoxPlotter(servoBox)
            localYaw = config.yawPosition
            localPitch = config.pitchPosition
            localRoll = config.rollPosition

        #Replot currentEmotion every second and camera if it is enabled
        if(time.time() - localTime >= 1):

            if (config.imageShow == True):
                img = cap.read()
                gray = gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                rescaledGray = cv2.resize(gray,dim)

                ascii = img2ascii.covertImageToAscii(rescaledGray, cols, scale, False)

                imgPlotter(imgPlotterBox, ascii)

            if (config.detection == True):
                detected,face = DetectorOfFaces.detect()
                if detected:
                    for (x,y,w,h) in face:
                        x1 = x//4
                        x2 = (x+w)//4
                        y1 = y//10 + 3
                        y2 = (y+h)//10 + 3

                        imgPlotterBox.addstr(1,30,str(x1) + " " + str(x2) + " " + str(y1) + " " + str(y2))

                        imgPlotterBox.box()
                        imgPlotterBox.refresh()

                        imgPlotterBox.attron(curses.color_pair(1))

                        imgPlotterBox.addstr(y1,x1,"8")
                        imgPlotterBox.addstr(y1,x2,"8")
                        imgPlotterBox.addstr(y2,x1,"8")
                        imgPlotterBox.addstr(y2,x2,"8")
                        imgPlotterBox.attroff(curses.color_pair(1))

                imgPlotterBox.addstr(1,20,str(detected))


                imgPlotterBox.box()
                imgPlotterBox.refresh()



            if (config.programMode == 'Random'):
                config.timetoNextEmotion = config.timetoNextEmotion -1
                if (config.timetoNextEmotion == -1):
                    config.timetoNextEmotion = random.randint(10,30)
                    config.currentEmotion = config.nextEmotion
                    config.nextEmotion = random.choice(config.Emotions)
                currentEmotionPlotter(currentEmotion,config.currentEmotion, config.nextEmotion, config.timetoNextEmotion)
            localTime = time.time()

        key = stdscr.getch()

        if ( key == 27 ): # ESC key
            config.keyPressed = 'ESC'
            config.programRunning = False
            break
        elif (key == curses.KEY_UP and menuPosition > 0):
            config.keyPressed = 'UP'
            menuPosition -= 1
        elif (key == curses.KEY_DOWN and menuPosition < len(menu) -1):
            config.keyPressed = 'DOWN'
            menuPosition += 1
        elif (key == curses.KEY_ENTER or key in[10,13]):
            config.keyPressed = 'ENTER'

            if (menu[menuPosition] == 'Exit'): #Exit the program
                config.programRunning = False
                break
            elif (menu[menuPosition] == 'Keyboard Mode'):
                config.programMode = 'Keyboard'
                localProgramMode = 'Keyboard'
            elif (menu[menuPosition] == 'Random Mode'):
                config.programMode = 'Random'
                localProgramMode = 'Random'
            elif (menu[menuPosition] == 'Camera on/off'):
                activateImage(imgPlotterBox)
            elif (menu[menuPosition] == 'Face detection on/off'):
                config.detection = True
                DetectorOfFaces = faceDetection(cap)


            currentModePlotter(currentMode,localProgramMode)

        elif (key == 97 and localProgramMode == 'Keyboard'): #A key pressed, move left with Keyboard
            config.keyPressed = 'A'
        elif (key == 100 and localProgramMode == 'Keyboard'): #D key pressed, move left with Keyboard
            config.keyPressed = 'D'
        elif (key == 119 and localProgramMode == 'Keyboard'): #W key pressed, move up with Keyboard
            config.keyPressed = 'W'
        elif (key == 115 and localProgramMode == 'Keyboard'): #W key pressed, move down with Keyboard
            config.keyPressed = 'S'
        elif (key == 113 and localProgramMode == 'Keyboard'): #Q key pressed, rotate left with Keyboard
            config.keyPressed = 'Q'
        elif (key == 101 and localProgramMode == 'Keyboard'): #E key pressed, rotate right with Keyboard
            config.keyPressed = 'E'
        elif (key == 99 and localProgramMode == 'Keyboard'): #C key pressed, Center robot with Keyboard
            config.keyPressed = 'C'
        elif (key == 111 and localProgramMode == 'Keyboard'): #O key pressed, disengage servos
            config.keyPressed = 'O'
        elif (key == 105): #I key pressed, toggle webcam VideoCapture
            activateImage(imgPlotterBox)
        else:
            config.keyPressed = 'None'

        menuPrinter(menuBox,menu,'MenuTitle',menuPosition)


    curses.endwin()

def TerminalStarter():
    curses.wrapper(TerminalWrapped())
