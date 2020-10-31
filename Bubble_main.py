# Software for the Bubble robot
# This software allows the robot to move its head
# to random positions. For now, the software is not able to interact
# or see the world, but a camera with detection will be added to the software.

# yaw = turning head = GPIO17
# pitch = look up/down = GPIO22
# roll = tilt head = GPIO27

# For general headpositions, the terminology is:
# [0,1,2], where
# First number = up/middle/down
# Second number = left/center/right
# Third number = tiltLeft/straight/tiltRight

# General import statements
import pigpio
import time
import random
import config
import omitMaxValue
import moveServos
import determineNewPosition
import printFunctions
import TerminalDisplay
import _thread
import math

programCounter = 1
ready = 0

# Define areas to look at
#headPositions = [[0,1,1],[1,1,1],[2,1,1],[1,0,1],[1,2,1],[1,1,0],[1,1,2],[0,1,1],[0,1,1],[0,1,1]]
headPositions = [[0,1,1]]
totalPositions = len(headPositions)

# Up/down/middle - Pitch
lookUp =        [config.middle,config.pitchMax]
lookMiddle =    [config.middle-100,config.middle+100]
lookDown =      [config.pitchMin, config.middle]

# Left/right/center - Yaw
lookLeft =      [config.middle,config.yawMax]
lookCenter =    [config.middle-100,config.middle+100]
lookRight =     [config.yawMin, config.middle]

# Tilt left/right/center - Roll
lookTiltLeft =  [config.middle, config.rollMax]
lookStraight =[config.middle-100,config.middle+100]
lookTiltRight = [config.rollMin, config.middle]


# Set the servos to their middle values
config.pi.set_servo_pulsewidth(config.yawServo, config.yawMiddle)
config.pi.set_servo_pulsewidth(config.pitchServo, config.pitchMiddle)
config.pi.set_servo_pulsewidth(config.rollServo, config.rollMiddle)


def headPositionDeterminer():
    config.currentHeadPosition = [0,0,0]
    if (config.pitchPosition > config.middle+100):
        config.currentHeadPosition[0] = 0
    elif (config.pitchPosition < config.middle-100):
        config.currentHeadPosition[0] = 2
    else:
        config.currentHeadPosition[0] = 1

    if (config.yawPosition > config.middle+100):
        config.currentHeadPosition[1] = 0
    elif (config.yawPosition < config.middle-100):
        config.currentHeadPosition[1] = 2
    else:
        config.currentHeadPosition[1] = 1

    if (config.rollPosition > config.middle+100):
        config.currentHeadPosition[2] = 0
    elif (config.rollPosition < config.middle-100):
        config.currentHeadPosition[2] = 2
    else:
        config.currentHeadPosition[2] = 1


def BubbleMainLoop():
    # Program loop
    global programCounter
    global headPositions
    global ready

    movingToHead = False

    while(config.programRunning):
        # # Get the random integers for rotating the head
        # config.totalSteps = random.randint(20,51)
        # config.yawSteps = random.randint(-1000,1000)
        # config.pitchSteps = random.randint(-800,800)
        # config.rollSteps = random.randint(-800,800)

        if (config.programMode == 'Random'): # Default state of the robot, randomly moving its head
            # Set the new position of the servos according to the general position of the head and the speed at which this needs to happen
            # Include 'emotions' in the calculation
            config.breakSleep = False

            if (config.currentEmotion == 'Alert'):
                config.sleepTime = 0.04
                timeBetweenMoves = random.randint(5,15) #Less time between Bubble moving
                config.totalSteps = random.randint(5,10) #Less steps, so movement is faster
                headPositions = [[random.randint(0,1),random.randint(0,2),1]] #Don't look down, don't tilt head

            elif (config.currentEmotion == 'Sad'):
                config.sleepTime = 0.04
                timeBetweenMoves = random.randint(50,100) #Take a long time between moves
                config.totalSteps = random.randint(30,40)
                headPositions = [[2,random.randint(0,2),1]] #Only look down, don't tilt head

            elif (config.currentEmotion == 'Curious'):
                config.sleepTime = 0.04
                timeBetweenMoves = random.randint(5,30) #Take a long time between moves
                config.totalSteps = random.randint(10,20)
                schuin = [0,2]
                headPositions = [[0,random.randint(0,2),random.choice(schuin)]] #Only look up, always tilt head

            else:
                config.sleepTime = 0.04
                timeBetweenMoves = random.randint(5,100)
                config.totalSteps = random.randint(30,40)
                headPositions = [[random.randint(0,2),random.randint(0,2),random.randint(0,2)]]



            newPitchPosition = determineNewPosition.newPosMaker(lookUp,lookMiddle,lookDown,headPositions[programCounter%totalPositions][0])
            newYawPosition = determineNewPosition.newPosMaker(lookLeft,lookCenter,lookRight,headPositions[programCounter%totalPositions][1])
            newRollPosition = determineNewPosition.newPosMaker(lookTiltLeft,lookStraight,lookTiltRight,headPositions[programCounter%totalPositions][2])
            config.currentHeadPosition = headPositions[programCounter%totalPositions]

            # Calculate amount of steps necessary for new position
            config.yawSteps = newYawPosition - config.yawPosition
            config.pitchSteps = newPitchPosition - config.pitchPosition
            config.rollSteps = newRollPosition - config.rollPosition


            if (config.newHead == True):
                movingToHead = True
                if config.headCenter[0] < 80:
                    angleX = math.degrees(math.atan((80 - config.headCenter[0])/config.DistanceSubject))
                else:
                    angleX = -math.degrees(math.atan((config.headCenter[0] - 80)/config.DistanceSubject))
                config.yawSteps = math.floor(angleX/(180/1000))

                if config.headCenter[1] < 60:
                    angleX = -math.degrees(math.atan((60 - config.headCenter[1])/config.DistanceSubject))
                else:
                    angleX = math.degrees(math.atan((config.headCenter[1] - 60)/config.DistanceSubject))
                config.pitchSteps = -math.floor(angleX/(180/1000))

                config.rollSteps = config.rollMiddle - config.rollPosition

                #config.rollSteps = 10
                config.headCenter = [80,60]
                config.newHead = False
                timeBetweenMoves = random.randint(50,100)

            if (config.newColor == True):
                if config.headCenter[0] < 80:
                    angleX = math.degrees(math.atan((80 - config.headCenter[0])/config.DistanceSubjectColor))
                else:
                    angleX = -math.degrees(math.atan((config.headCenter[0] - 80)/config.DistanceSubjectColor))
                config.yawSteps = math.floor(angleX/(180/1000))

                if config.headCenter[1] < 60:
                    angleX = -math.degrees(math.atan((60 - config.headCenter[1])/config.DistanceSubjectColor))
                else:
                    angleX = math.degrees(math.atan((config.headCenter[1] - 60)/config.DistanceSubjectColor))
                config.pitchSteps = -math.floor(angleX/(180/1000))

                config.rollSteps = config.rollMiddle - config.rollPosition

                #config.rollSteps = 10
                config.headCenter = [80,60]
                config.newColor = False
                timeBetweenMoves = random.randint(50,100)
                config.totalSteps = 3


            # Make sure the maximum potmeter values are not exceeded and set new position
            config.yawSteps = omitMaxValue.MaxValue(config.yawPosition,config.yawSteps,config.yawMin,config.yawMax)
            config.pitchSteps = omitMaxValue.MaxValue(config.pitchPosition,config.pitchSteps,config.pitchMin,config.pitchMax)
            config.rollSteps = omitMaxValue.MaxValue(config.rollPosition,config.rollSteps,config.rollMin,config.rollMax)

            # Move the servos to the right place in the right time
            ready = 0
            moveServos.moveTotalSteps()
            ready = 1

            programCounter = programCounter + 1
            sleepCounter = 0



            while(sleepCounter < timeBetweenMoves and config.breakSleep == False):
                time.sleep(0.1)
                sleepCounter = sleepCounter + 1

            if (movingToHead == True):
                #config.newHead = False
                movingToHead = False

        elif (config.programMode == 'Keyboard'): #Keyboard Interaction with the robot
            steps = 200
            config.sleepTime = 0.005
            config.yawSteps = 0
            config.pitchSteps = 0
            config.rollSteps = 0
            config.totalSteps = 30

            if (config.keyPressed == 'A'): #Turn left
                config.yawSteps = omitMaxValue.MaxValue(config.yawPosition,-1*steps,config.yawMin,config.yawMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'D'): #Turn right
                config.yawSteps = omitMaxValue.MaxValue(config.yawPosition,steps,config.yawMin,config.yawMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'S'): #Turn down
                config.pitchSteps = omitMaxValue.MaxValue(config.pitchPosition,-1*steps,config.pitchMin,config.pitchMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'W'): #Turn up
                config.pitchSteps = omitMaxValue.MaxValue(config.pitchPosition,steps,config.pitchMin,config.pitchMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'Q'): #Rotate left
                config.rollSteps = omitMaxValue.MaxValue(config.rollPosition,-1*steps,config.rollMin,config.rollMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'E'): #Rotate right
                config.rollSteps = omitMaxValue.MaxValue(config.rollPosition,steps,config.rollMin,config.rollMax)
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'C'): #Center button
                config.yawSteps = config.yawMiddle - config.yawPosition
                config.pitchSteps = config.pitchMiddle - config.pitchPosition
                config.rollSteps = config.rollMiddle - config.rollPosition
                moveServos.moveTotalSteps()
                headPositionDeterminer()

            elif (config.keyPressed == 'O'): #Center button
                config.pi.set_servo_pulsewidth(config.yawServo, 0)
                config.pi.set_servo_pulsewidth(config.pitchServo, 0)
                config.pi.set_servo_pulsewidth(config.rollServo, 0)



def main():
    try:
        _thread.start_new_thread(BubbleMainLoop,())
        _thread.start_new_thread(TerminalDisplay.TerminalStarter,())

    except:
        print("Error: unable to start thread")
    while (1):
        pass
        time.sleep(0.1)
        if (config.programRunning == 0): # and ready == 1):
            break

    printFunctions.clearPrints()
    print("Program exiting")
    print("Returning Bubble to initial position")

    config.sleepTime = 0.04
    config.totalSteps = 10
    config.yawSteps = config.yawMiddle - config.yawPosition
    config.pitchSteps = config.pitchMiddle - config.pitchPosition
    config.rollSteps = config.rollMiddle - config.rollPosition

    moveServos.moveTotalSteps()

    config.pi.set_servo_pulsewidth(config.yawServo, config.yawMiddle)
    config.pi.set_servo_pulsewidth(config.pitchServo, config.pitchMiddle)
    config.pi.set_servo_pulsewidth(config.rollServo, config.rollMiddle)

    print("Disabling Servos")

    config.pi.set_servo_pulsewidth(config.yawServo, 0)
    config.pi.set_servo_pulsewidth(config.pitchServo, 0)
    config.pi.set_servo_pulsewidth(config.rollServo, 0)

    print("Done, program stopped!")

if __name__ == "__main__":
        main()
