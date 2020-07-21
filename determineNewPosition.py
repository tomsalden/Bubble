# A function to determine the new position of the servos
def newPosMaker(opt1,opt2,opt3,x):
    switcher = {
        0:opt1,
        1:opt2,
        2:opt3
    }
    return switcher.get(x,opt2)
