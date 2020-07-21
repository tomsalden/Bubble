# A function to determine the new position of the servos
# Arguments: opt1 = first position
#            opt2 = middle positions
#            opt3 = last positions
#            x = chosen position
import random

def newPosMaker(opt1,opt2,opt3,x):
    switcher = {
        0:opt1,
        1:opt2,
        2:opt3
    }
    newPositionArea = switcher.get(x,opt2)
    newPosition = random.randint(newPositionArea[0],newPositionArea[1])

    return newPosition
