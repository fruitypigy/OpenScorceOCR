import cv2 as cv
import argparse
import numpy as np
import Testing
import OpenCVMatch
import ImageProcess
import time

alpha_slider_max = 255
title_window = 'Test'


hm = 0
sm = 0
vm = 0

hx = 255
sx = 255
vx = 255

angle = 2

crop = 0.8

def hueMin(val):

    Testing.hm = val
    updateWindow()

def hueMax(val):
	Testing.hx = val
	updateWindow()

def satMin(val):

    Testing.sm = val
    updateWindow()

def satMax(val):
	Testing.sx = val
	updateWindow()

def valMin(val):
	Testing.vm = val
	updateWindow()
	
def valMax(val):
	Testing.vx = val
	updateWindow()

def valRotate(val):
	Testing.angle = val
	updateWindow()

def valCrop(val):
	Testing.crop = val*0.01
	updateWindow()

def updateWindow():
    msk = maskRotate(src1)
    cv.imshow('Image', msk)

def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

def maskRotate(img):
	realProcessed = ImageProcess.process(img, hm,hx,sm,sx,vm,vx,Testing.crop*100, angle=angle)
	print('Real Processed shows: ' + str(OpenCVMatch.getDigit(realProcessed)))

	print('V Max: ' + str(vx) + ' Scale:' + str(crop))
	combined_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	# print(hm)

	lower_bound = np.array([hm, sm, vm]) 
	upper_bound = np.array([hx, sx, vx]) 

	#create mask 
	msk = cv.inRange(combined_hsv, lower_bound, upper_bound)
    
	# grab the dimensions of the image and calculate the center of the
	# image
	(h, w) = msk.shape[:2]
	(cX, cY) = (w // 2, h // 2)
	# rotate our image by 45 degrees around the center of the image
	M = cv.getRotationMatrix2D((cX, cY), angle, 1.0)
	rotated = cv.warpAffine(msk, M, (w, h))
	# cv.imshow("Rotated by 45 Degrees", rotated)

	# processed = ImageProcess.process(msk)
	# OpenCVMatch.getDigit(msk)

	cropped = crop_img(rotated, crop)

	dim = (279, 469)
	resized = cv.resize(cropped, dim)
	return resized

def digitRec(val):
	masked = maskRotate(src1)
	# print("Test")

	masked = cv.merge((masked, masked, masked))
	# cv.imwrite('TESTTEST.jpg', masked)
	# masked = cv.imread('TESTTEST.jpg')
	# processed = ImageProcess.process(masked,hm, hx, sm, sx, vm, vx)
	# print(vx)
	OpenCVMatch.getDigit(masked)
	# cv.imwrite('PROCCESSEDDDDD.jpg', processed)
	# OpenCVMatch.getDigit(src1)

src1 = cv.imread('Tests\Real.jpg')

cv.namedWindow(title_window)

cv.createTrackbar('Hue Min', title_window , 0, alpha_slider_max, hueMin)
cv.createTrackbar('Hue Max', title_window , 255, alpha_slider_max, hueMax)
cv.createTrackbar('Sat Min', title_window , 0, alpha_slider_max, satMin)
cv.createTrackbar('Sat Max', title_window , 255, alpha_slider_max, satMax)
cv.createTrackbar('Val Min', title_window , 0, alpha_slider_max, valMin)
cv.createTrackbar('Val Max', title_window , 255, alpha_slider_max, valMax)
cv.createTrackbar('Rotation', title_window , 0, 360, valRotate)
cv.createTrackbar('Crop', title_window , 0, 100, valCrop)
cv.createTrackbar('Test', title_window , 0, 1, digitRec)

# Show some stuff
hueMin(0)


# Wait until user press some key
cv.waitKey()