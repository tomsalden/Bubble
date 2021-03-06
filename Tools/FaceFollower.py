import sys
sys.path.append('home/pi/local/lib/python3.7/site-packages/cv2/python-3.7')
sys.path.append("..")

import cv2, queue, threading, time, os
import numpy as np
import pigpio
import math
import omitMaxValue
import MoveServo

os.chdir("/home/pi/opencv-4.4.0/data/haarcascades")

face_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_frontalface_alt.xml')
profile_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_eye.xml')

pi = pigpio.pi()
yawServo = 27     #Servo op z'n hoofd
pitchServo = 21   #Servo voor schuinkijken
rollServo = 22    #Servo voor hoofddraaien

midden = 1500
yawMin = 1200
yawMax = 1800
pitchMin = 1200
pitchMax = 1800
rollMin = 1200
rollMax = 1800

yawPosition = midden
pitchPosition = midden
rollPosition = midden

pi.set_servo_pulsewidth(yawServo, yawPosition)
pi.set_servo_pulsewidth(pitchServo, pitchPosition)
pi.set_servo_pulsewidth(rollServo, rollPosition)

DistanceSubject = 90 #Estimated 157, tuned to this value


#Due to fov of camera and resolution:
#           /  |
#        /     | 80
#     / 27 deg |
# cam  --------|
#     \        |
#       \      | 80
#          \   |
#     |---------|
#         157.00
#
# So 80/tan(27deg) = 157.00

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(3,160) # set Width
    self.cap.set(4,120) # set Height
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

cap = VideoCapture(0)

while True:
    time.sleep(1)   # simulate time between events
    img = cap.read()
    #img = cv2.flip(frame, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #First check for faces
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    if len(faces):
      print("Face detected")
      for (x,y,w,h) in faces:
          cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
          roi_gray = gray[y:y+h, x:x+w]
          roi_color = img[y:y+h, x:x+w]
          detectedCenterX = x + 1/2*w
          detectedCenterY = y + 1/2*h

    else:
        eyes = eye_cascade.detectMultiScale(gray, 1.05, 5)
        if len(eyes):
            print("Eye detected")
            for (x,y,w,h) in eyes:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                detectedCenterX = x + 1/2*w
                detectedCenterY = y + 1/2*h

        else:
            profiles = profile_cascade.detectMultiScale(gray, 1.05, 5)
            if len(profiles):
                print("Profile detected")
                for (x,y,w,h,) in profiles:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
                    detectedCenterX = x + 1/2*w
                    detectedCenterY = y + 1/2*h
            else:
                detectedCenterX = 80
                detectedCenterY = 60


    cv2.imshow("img", img)


    #Move servos so the detectedCenter is in the middle of the frame
    #Yaw:
    #print(detectedCenterX)
    #print(detectedCenterY)

    if detectedCenterX < 80:
        angleX = math.degrees(math.atan((80 - detectedCenterX)/DistanceSubject))
    else:
        angleX = -math.degrees(math.atan((detectedCenterX - 80)/DistanceSubject))


    extraStepsYaw = math.floor(angleX/(180/1000))
    extraStepsYaw = omitMaxValue.MaxValue(yawPosition,extraStepsYaw,yawMin,yawMax)

    yawPosition = MoveServo.moveTotalSteps(extraStepsYaw,5,yawPosition,pi,yawServo,0.01)

    #Pitch:
    if detectedCenterY < 60:
        angleX = -math.degrees(math.atan((60 - detectedCenterY)/DistanceSubject))
    else:
        angleX = math.degrees(math.atan((detectedCenterY - 60)/DistanceSubject))

    extraStepsPitch = math.floor(angleX/(180/1000))
    extraStepsPitch = omitMaxValue.MaxValue(pitchPosition,extraStepsPitch,pitchMin,pitchMax)

    pitchPosition = MoveServo.moveTotalSteps(extraStepsPitch,5,pitchPosition,pi,pitchServo,0.01)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cv2.destroyAllWindows()
