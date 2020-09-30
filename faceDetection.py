import sys
sys.path.append('/usr/local/lib/python3.7/site-packages/cv2/python-3.7')
sys.path.append("..")

import cv2, queue, threading, time, os
import numpy as np
import pigpio
import math

os.chdir("/home/pi/opencv-4.4.0/data/haarcascades")

face_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_frontalface_alt.xml')
profile_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.4.0/data/haarcascades/haarcascade_eye.xml')


def faceDetection(gray):
    detected = 0
    faces = face_cascade.detectMultiScale(gray, 1.05, 5)
    if len(faces):
        detected = 1
    else:
        eyes = eye_cascade.detectMultiScale(gray, 1.05, 5)
        if len(faces):
            detected = 1
        else:
            profiles = profile_cascade.detectMultiScale(gray, 1.05, 5)
            if len(faces):
                detected = 1

    return faces, detected
