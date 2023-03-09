import cv2 as cv
import numpy as np
import mediapipe as mp

cap = cv.imread('elon_musk.jpg')

while True:
    cv.imshow('Main', cap)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
