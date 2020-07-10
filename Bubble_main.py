# Software for the Bubble robot
# This software allows the robot to move its head
# to random positions. For now, the software is not able to interact
# or see the world, but a camera with detection will be added to the software.

# General import statements
import pigpio
from time import sleep
import random
import config
import omitMaxValue
import moveServos

yawMin = 1000
yawMax = 2000
pitchMin = 1200
pitchMax = 1900
rollMin = 1100
rollMax = 1900

# Set the servos to their middle values
config.pi.set_servo_pulsewidth(config.yawServo, config.middle)
config.pi.set_servo_pulsewidth(config.pitchServo, config.middle)
config.pi.set_servo_pulsewidth(config.rollServo, config.middle)


# Program loop
while True:
    # Get the random integers for rotating the head
    config.totalSteps = random.randint(20,51)
    config.yawSteps = random.randint(-1000,1000)
    config.pitchSteps = random.randint(-800,800)
    config.rollSteps = random.randint(-800,800)


    # Make sure the maximum potmeter valus are not exceeded
    config.yawSteps = omitMaxValue.MaxValue(config.yawPosition,config.yawSteps,yawMin,yawMax)
    config.pitchSteps = omitMaxValue.MaxValue(config.pitchPosition,config.pitchSteps,pitchMin,pitchMax)
    config.rollSteps = omitMaxValue.MaxValue(config.rollPosition,config.rollSteps,rollMin,rollMax)

    moveServos.moveTotalSteps()

    # Turn off the servos
    config.pi.set_servo_pulsewidth(config.yawServo, 0)
    config.pi.set_servo_pulsewidth(config.pitchServo, 0)
    config.pi.set_servo_pulsewidth(config.rollServo, 0)

    #sleep(1)
    #test erbij
