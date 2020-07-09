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

yawPositie = 1500
pitchPositie = 1500
rollPositie = 1500


while True:
    draaitijd = random.randint(20,51)
    yawStappen = random.randint(-1000,1000)
    pitchStappen = random.randint(-800,800)
    rollStappen = random.randint(-800,800)

    if yawPositie + yawStappen > yawMax:
        yawStappen = yawMax-yawPositie
    if yawPositie + yawStappen < yawMin:
        yawStappen = yawMin-yawPositie

    if pitchPositie + pitchStappen > pitchMax:
        pitchStappen = pitchMax-pitchPositie
    if pitchPositie + pitchStappen < pitchMin:
        pitchStappen = pitchMin-pitchPositie

    if rollPositie + rollStappen > rollMax:
        rollStappen = rollMax-rollPositie
    if rollPositie + rollStappen < rollMin:
        rollStappen = rollMin-rollPositie

    yawOnderverdeeld = int(float(yawStappen)/draaitijd)
    pitchOnderverdeeld = int(float(pitchStappen)/draaitijd)
    rollOnderverdeeld = int(float(rollStappen)/draaitijd)

    #print('draaitijd', draaitijd)
    #print('yaw',yawPositie + yawStappen, yawStappen , yawMax, yawMin)
    #print('pitch',pitchPositie + pitchStappen, pitchPositie, pitchStappen, pitchOnderverdeeld, pitchMax, pitchMin)
    #print('roll',rollPositie + rollStappen, rollStappen, rollMax, rollMin)

    for x in range(0,draaitijd):
        yawPositie = yawPositie + yawOnderverdeeld
        pitchPositie = pitchPositie + pitchOnderverdeeld
        rollPositie = rollPositie + rollOnderverdeeld

        pi.set_servo_pulsewidth(yawServo, yawPositie)
        pi.set_servo_pulsewidth(pitchServo, pitchPositie)
        pi.set_servo_pulsewidth(rollServo, rollPositie)

        sleep(0.05)

    pi.set_servo_pulsewidth(yawServo, 0)
    pi.set_servo_pulsewidth(pitchServo, 0)
    pi.set_servo_pulsewidth(rollServo, 0)

    #sleep(1)
