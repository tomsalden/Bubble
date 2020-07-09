# Software for the Bubble robot
# This software allows the robot to move its head
# to random positions. For now, the software is not able to interact
# or see the world, but a camera with detection will be added to the software.

# General import statements
import pigpio
from time import sleep
import random
from omitMaxValue import *

# Initialisations
pi = pigpio.pi()
yawServo = 17     #Servo op z'n hoofd
pitchServo = 22   #Servo voor schuinkijken
rollServo = 27    #Servo voor hoofddraaien

# Initial values for the variables
middle = 1500
yawMin = 1000
yawMax = 2000
pitchMin = 1200
pitchMax = 1900
rollMin = 1100
rollMax = 1900

# Set the servos to their middle values
pi.set_servo_pulsewidth(yawServo, middle)
pi.set_servo_pulsewidth(pitchServo, middle)
pi.set_servo_pulsewidth(rollServo, middle)

yawPositie = middle
pitchPositie = middle
rollPositie = middle


# Program loop
while True:
    # Get the random integers for rotating the head
    draaitijd = random.randint(20,51)
    yawStappen = random.randint(-1000,1000)
    pitchStappen = random.randint(-800,800)
    rollStappen = random.randint(-800,800)


    # Make sure the maximum potmeter valus are not exceeded
    yawStappen = omitMaxValue(yawPositie,yawStappen,yawMin,yawMax)
    pitchStappen = omitMaxValue(pitchPositie,pitchStappen,pitchMin,pitchMax)
    rollStappen = omitMaxValue(rollPositie,rollStappen,rollMin,rollMax)


    # Subdivide the steps to set the steps/time for the servos
    yawOnderverdeeld = int(float(yawStappen)/draaitijd)
    pitchOnderverdeeld = int(float(pitchStappen)/draaitijd)
    rollOnderverdeeld = int(float(rollStappen)/draaitijd)

    # Run the servo sequence
    for x in range(0,draaitijd):
        yawPositie = yawPositie + yawOnderverdeeld
        pitchPositie = pitchPositie + pitchOnderverdeeld
        rollPositie = rollPositie + rollOnderverdeeld

        pi.set_servo_pulsewidth(yawServo, yawPositie)
        pi.set_servo_pulsewidth(pitchServo, pitchPositie)
        pi.set_servo_pulsewidth(rollServo, rollPositie)

        sleep(0.05)

    # Turn off the servos
    pi.set_servo_pulsewidth(yawServo, 0)
    pi.set_servo_pulsewidth(pitchServo, 0)
    pi.set_servo_pulsewidth(rollServo, 0)

    #sleep(1)
    #test erbij
