# Make sure the servos move the right amount of steps in the right amount of time

import config
from time import sleep

def moveTotalSteps():

    # Subdivide the steps to set the steps/time for the servos
    yawDivided = int(float(config.yawSteps)/config.totalSteps)
    pitchDivided = int(float(config.pitchSteps)/config.totalSteps)
    rollDivided = int(float(config.rollSteps)/config.totalSteps)

    if yawDivided > 0:
        yawExtraStep = 1
    else:
        yawExtraStep = -1

    if pitchDivided > 0:
        pitchExtraStep = 1
    else:
        pitchExtraStep = -1

    if rollDivided > 0:
        rollExtraStep = 1
    else:
        rollExtraStep = -1

    yawRest = abs(config.yawSteps - (yawDivided * config.totalSteps))
    pitchRest = abs(config.pitchSteps - (pitchDivided * config.totalSteps))
    rollRest = abs(config.rollSteps - (rollDivided * config.totalSteps))

    yawStartExtraStep = config.totalSteps - yawRest
    pitchStartExtraStep = config.totalSteps - pitchRest
    rollStartExtraStep = config.totalSteps - rollRest

    # Run the servo sequence
    for x in range(0,config.totalSteps):

        #Make sure to add the right amount of steps each time, including extra steps to get to the total steps every time
        if x < yawStartExtraStep:
            config.yawPosition = config.yawPosition + yawDivided
        else:
            config.yawPosition = config.yawPosition + yawDivided + yawExtraStep

        if x < pitchStartExtraStep:
            config.pitchPosition = config.pitchPosition + pitchDivided
        else:
            config.pitchPosition = config.pitchPosition + pitchDivided + pitchExtraStep

        if x < rollStartExtraStep:
            config.rollPosition = config.rollPosition + rollDivided
        else:
            config.rollPosition = config.rollPosition + rollDivided + rollExtraStep

        # Set the servos to the right step each time, but leave them off if they don't have steps
        if yawDivided and yawRest:
            config.pi.set_servo_pulsewidth(config.yawServo, config.yawPosition)

        if pitchDivided and pitchRest:
            config.pi.set_servo_pulsewidth(config.pitchServo, config.pitchPosition)

        if rollDivided and rollRest:
            config.pi.set_servo_pulsewidth(config.rollServo, config.rollPosition)

        sleep(config.sleepTime)
