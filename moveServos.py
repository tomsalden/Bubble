# Make sure the servos move the right amount of steps in the right amount of time

import config
from time import sleep

def moveTotalSteps():

    # Subdivide the steps to set the steps/time for the servos
    yawDivided = int(float(config.yawSteps)/config.totalSteps)
    pitchDivided = int(float(config.pitchSteps)/config.totalSteps)
    rollDivided = int(float(config.rollSteps)/config.totalSteps)

    yawRest = config.yawSteps - (yawDivided * config.totalSteps)
    pitchRest = config.pitchSteps - (pitchDivided * config.totalSteps)
    rollRest = config.rollSteps - (rollDivided * config.totalSteps)

    yawStartExtraStep = config.totalSteps - yawRest
    pitchStartExtraStep = config.totalSteps - pitchRest
    rollStartExtraStep = config.totalSteps - rollRest

    # Run the servo sequence
    for x in range(0,config.totalSteps):

        #Make sure to add the right amount of steps each time, including extra steps to get to the total steps every time
        if x < yawStartExtraStep:
            config.yawPosition = config.yawPosition + yawDivided
        else:
            config.yawPosition = config.yawPosition + yawDivided + 1

        if x < pitchStartExtraStep:
            config.pitchPosition = config.pitchPosition + pitchDivided
        else:
            config.pitchPosition = config.pitchPosition + pitchDivided + 1

        if x < rollStartExtraStep:
            config.rollPosition = config.rollPosition + rollDivided
        else:
            config.rollPosition = config.rollPosition + rollDivided + 1

        # Set the servos to the right step each time, but leave them off if they don't have steps
        if yawDivided and yawRest:
            config.pi.set_servo_pulsewidth(config.yawServo, config.yawPosition)

        if pitchDivided and pitchRest:
            config.pi.set_servo_pulsewidth(config.pitchServo, config.pitchPosition)

        if rollDivided and rollRest:
            config.pi.set_servo_pulsewidth(config.rollServo, config.rollPosition)

        sleep(config.sleepTime)

    print(config.yawSteps,config.yawPosition, yawRest)
