import pigpio
from time import sleep
import random

# connect to the
pi = pigpio.pi()
yawServo = 17     #Servo op z'n hoofd
pitchServo = 22   #Servo voor schuinkijken
rollServo = 27    #Servo voor hoofddraaien

midden = 1500
yawMin = 1000
yawMax = 2000
pitchMin = 1200
pitchMax = 1900
rollMin = 1100
rollMax = 1900

pi.set_servo_pulsewidth(yawServo, midden)
pi.set_servo_pulsewidth(pitchServo, midden)
pi.set_servo_pulsewidth(rollServo, midden)

sleep(1);

while True:

    pi.set_servo_pulsewidth(yawServo, yawMin)
    pi.set_servo_pulsewidth(pitchServo, pitchMin)
    pi.set_servo_pulsewidth(rollServo, rollMin)

    sleep(1)

    pi.set_servo_pulsewidth(yawServo, yawMax)
    pi.set_servo_pulsewidth(pitchServo, pitchMax)
    pi.set_servo_pulsewidth(rollServo, rollMax)

    sleep(1)
