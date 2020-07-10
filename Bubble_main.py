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
config.pi.set_servo_pulsewidth(config.yawServo, middle)
config.pi.set_servo_pulsewidth(config.pitchServo, middle)
config.pi.set_servo_pulsewidth(config.rollServo, middle)


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


    # Subdivide the steps to set the steps/time for the servos
    yawDivided = int(float(config.yawSteps)/config.totalSteps)
    pitchDivided = int(float(config.pitchSteps)/config.totalSteps)
    rollDivided = int(float(config.rollSteps)/config.totalSteps)

    # Run the servo sequence
    for x in range(0,config.totalSteps):
        config.yawPosition = config.yawPosition + yawDivided
        config.pitchPosition = config.pitchPosition + pitchDivided
        config.rollPosition = config.rollPosition + rollDivided

        config.pi.set_servo_pulsewidth(config.yawServo, config.yawPosition)
        config.pi.set_servo_pulsewidth(config.pitchServo, config.pitchPosition)
        config.pi.set_servo_pulsewidth(config.rollServo, config.rollPosition)

        sleep(0.04)

    # Turn off the servos
    pi.set_servo_pulsewidth(config.yawServo, 0)
    pi.set_servo_pulsewidth(config.pitchServo, 0)
    pi.set_servo_pulsewidth(config.rollServo, 0)

    #sleep(1)
    #test erbij
