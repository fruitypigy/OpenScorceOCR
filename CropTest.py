import cv2
import numpy as np

initial = cv2.imread('Tests\RawOne.jpg')

cropped = initial[12:360 , 43:228]

cv2.imshow('Test', cropped)
cv2.waitKey()
