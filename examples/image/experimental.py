#!/usr/bin/env python
import device_patches      
import cv2
import os
import time
import sys, getopt
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner
runner = None
model = "86.eim"
dir_path = os.path.dirname(os.path.realpath(__file__))
modelfile = os.path.join(dir_path, model)
cam = cv2.VideoCapture(cv2.CAP_V4L2)

while True:
    check, frame = cam.read()

    cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()





