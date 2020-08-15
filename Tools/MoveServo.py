# Make sure the servos move the right amount of steps in the right amount of time

from time import sleep

def moveTotalSteps(servoSteps,totalSteps,servoPosition,servoObject,servoPin,sleepTime):

    # Subdivide the steps to set the steps/time for the servos
    servoDivided = int(float(servoSteps)/totalSteps)

    if servoDivided > 0:
        servoExtraStep = 1
    else:
        servoExtraStep = -1

    servoRest = abs(servoSteps - (servoDivided * totalSteps))
    servoStartExtraStep = totalSteps - servoRest


    # Run the servo sequence
    for x in range(0,totalSteps):

        #Make sure to add the right amount of steps each time, including extra steps to get to the total steps every time
        if x < servoStartExtraStep:
            servoPosition = servoPosition + servoDivided
        else:
            servoPosition = servoPosition + servoDivided + servoExtraStep


        # Set the servos to the right step each time, but leave them off if they don't have steps
        if servoDivided and servoRest:
            servoObject.set_servo_pulsewidth(servoPin, servoPosition)

        sleep(sleepTime)

    return servoPosition
