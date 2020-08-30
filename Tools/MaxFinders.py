import pigpio
from time import sleep
import random

# connect to the
pi = pigpio.pi()
yawServo = 14     #Servo op z'n hoofd
pitchServo = 15   #Servo voor schuinkijken
rollServo = 18    #Servo voor hoofddraaien

midden = 1500
yawMin = 1500   #
yawMax = 1500   #
pitchMin = 1500 # 1300
pitchMax = 1500 # 1750
rollMin = 1300  # 1300
rollMax = 1850  # 1850

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
