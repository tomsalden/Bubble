# config.py>
import pigpio
# Define global variables

# Initialisations
pi = pigpio.pi()
yawServo = 14     #Servo op z'n hoofd
pitchServo = 15   #Servo voor schuinkijken
rollServo = 18    #Servo voor hoofddraaien

currentHeadPosition = [1,1,1]
programRunning = True
programMode = 'Random'
keyPressed = 'none'

currentEmotion = 'Normal'
nextEmotion = 'Normal'
Emotions = ['Normal','Other']
timetoNextEmotion = 10

# Initial values for the variables
middle = 1500

yawPosition = middle
pitchPosition = middle
rollPosition = middle

totalSteps = 20
yawSteps = 100
pitchSteps = 100
rollSteps = 100

sleepTime = 0.04

yawMin = 500
yawMax = 2500
pitchMin = 1300
pitchMax = 1750
rollMin = 1350
rollMax = 1850

cameraEnabled = False
imageShow = False
cap = 0

detection = False
