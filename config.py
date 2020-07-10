# config.py>
import pigpio
# Define global variables

# Initialisations
pi = pigpio.pi()
yawServo = 17     #Servo op z'n hoofd
pitchServo = 22   #Servo voor schuinkijken
rollServo = 27    #Servo voor hoofddraaien

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
