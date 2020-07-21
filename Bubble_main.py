# Software for the Bubble robot
# This software allows the robot to move its head
# to random positions. For now, the software is not able to interact
# or see the world, but a camera with detection will be added to the software.

# yaw = turning head = GPIO17
# pitch = look up/down = GPIO22
# roll = tilt head = GPIO27

# General import statements
import pigpio
from time import sleep
import random
import config
import omitMaxValue
import moveServos
import determineNewPosition

yawMin = 1000
yawMax = 2000
pitchMin = 1200
pitchMax = 1900
rollMin = 1100
rollMax = 1900
programCounter = 1

# Define areas to look at
headPositions = [[0,1,1],[1,1,1],[2,1,1],[1,0,1],[1,2,1],[1,1,0],[1,1,2],[0,1,1],[0,1,1],[0,1,1]]
totalPositions = len(headPositions)

# Up/down/middle
lookUp =        [config.middle,pitchMax]
lookMiddle =    [config.middle-100,config.middle+100]
lookDown =      [pitchMin, config.middle]

# Left/right/center
lookLeft =      [config.middle,yawMax]
lookCenter =    [config.middle-100,config.middle+100]
lookRight =     [yawMin, config.middle]

# Tilt left/right/center
lookTiltLeft =  [config.middle, rollMax]
lookStraight =[config.middle-100,config.middle+100]
lookTiltRight = [rollMin, config.middle]


# Set the servos to their middle values
config.pi.set_servo_pulsewidth(config.yawServo, config.middle)
config.pi.set_servo_pulsewidth(config.pitchServo, config.middle)
config.pi.set_servo_pulsewidth(config.rollServo, config.middle)


# Program loop
while True:
    # # Get the random integers for rotating the head
    # config.totalSteps = random.randint(20,51)
    # config.yawSteps = random.randint(-1000,1000)
    # config.pitchSteps = random.randint(-800,800)
    # config.rollSteps = random.randint(-800,800)

    # Set the new position of the servos according to the general position of the head and the speed at which this needs to happen
    config.totalSteps = random.randint(20,51)
    newPitchPosition = newPosMaker(lookUp,lookMiddle,lookDown,headPositions[programCounter%totalPositions][0])
    newYawPosition = newPosMaker(lookLeft,lookCenter,lookRight,headPositions[programCounter%totalPositions][1])
    newRollPosition = newPosMaker(lookTiltLeft,lookStraight,lookTiltRight,headPositions[programCounter%totalPositions][2])

    # Calculate amount of steps necessary for new position
    config.yawSteps = newYawPosition - config.yawPosition
    config.pitchSteps = newPitchPosition - config.pitchPosition
    config.rollSteps = newRollPosition - config.rollPosition

    # Make sure the maximum potmeter valus are not exceeded
    config.yawSteps = omitMaxValue.MaxValue(config.yawPosition,config.yawSteps,yawMin,yawMax)
    config.pitchSteps = omitMaxValue.MaxValue(config.pitchPosition,config.pitchSteps,pitchMin,pitchMax)
    config.rollSteps = omitMaxValue.MaxValue(config.rollPosition,config.rollSteps,rollMin,rollMax)

    # Move the servos to the right place in the right time
    moveServos.moveTotalSteps()

    # Turn off the servos
    config.pi.set_servo_pulsewidth(config.yawServo, 0)
    config.pi.set_servo_pulsewidth(config.pitchServo, 0)
    config.pi.set_servo_pulsewidth(config.rollServo, 0)

    programCounter = programCounter + 1
