import pigpio
from time import sleep
import random

# connect to the
pi = pigpio.pi()
yawServo = 14     #Servo op z'n hoofd
pitchServo = 15   #Servo voor schuinkijken
rollServo = 18    #Servo voor hoofddraaien

midden = 1500
yawMin = 1000   #
yawMax = 2000   #
pitchMin = 1300 # 1300
pitchMax = 1750 # 1750
rollMin = 1350  # 1300
rollMax = 1850  # 1850

yawCurrent = 1500
pitchCurrent = 1500
rollCurrent = 1500

yawIncrement = 1
pitchIncrement = 1
rollIncrement = 1

pi.set_servo_pulsewidth(yawServo, midden)
pi.set_servo_pulsewidth(pitchServo, midden)
pi.set_servo_pulsewidth(rollServo, midden)

sleep(1);

while True:

  yawCurrent = yawCurrent + yawIncrement
  pitchCurrent = pitchCurrent + pitchIncrement
  rollCurrent = rollCurrent + rollIncrement
  
  pi.set_servo_pulsewidth(yawServo, yawCurrent)
  pi.set_servo_pulsewidth(pitchServo, pitchCurrent)
  pi.set_servo_pulsewidth(rollServo, rollCurrent)
  
  if (yawCurrent == yawMax):
    yawIncrement = -1
  if (pitchCurrent == pitchMax):
    pitchIncrement = -1
  if (rollCurrent == rollMax):
    rollIncrement = -1

  if (yawCurrent == yawMin):
    yawIncrement = 1
  if (pitchCurrent == pitchMin):
    pitchIncrement = 1
  if (rollCurrent == rollMin):
    rollIncrement = 1

  sleep(0.01)
  

