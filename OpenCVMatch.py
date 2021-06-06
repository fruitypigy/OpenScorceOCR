import cv2
import numpy as np

SegBM = cv2.imread('Segments\SegBM.jpg')
SegBR = cv2.imread('Segments\SegBR.jpg')
SegBL = cv2.imread('Segments\SegBL.jpg')
SegM = cv2.imread('Segments\SegM.jpg')
SegTM = cv2.imread('Segments\SegTM.jpg')
SegTR = cv2.imread('Segments\SegTR.jpg')
SegTL = cv2.imread('Segments\SegTL.jpg')

segments = [SegBM,SegBR,SegBL,SegM,SegTM,SegTR,SegTL]
segmentnames = ['SegBM', 'SegBR', 'SegBL', 'SegM', 'SegTM', 'SegTR', 'SegTL']

zero = [True, True, True, False, True, True, True]
one = [False, True, False, False, False, True, False]
two = [True, False, True, True, True, True, False]
three = [True, True, False, True, True, True, False]
four = [False, True, False, True, False, True, True]
five = [True, True, False, True, True, False, True]
six = [True, True, True, True, True, False, True]
seven = [False, True, False, False, True, True, False]
eight = [True, True, True, True, True, True, True]
nine = [True, True, False, True, True, True, True]

numbers = [zero,one,two,three,four,five,six,seven,eight,nine]

def checkSeg(img, seg,  min_percentage=2.5, max_percentage=10):
	# print('Checking ' + segmentnames[seg])

	check = segments[seg]

	combined = (cv2.addWeighted(check, 0.4, img, 0.1, 0))

	combined_hsv = cv2.cvtColor(combined, cv2.COLOR_BGR2HSV)

	sensitivity = 0
	lower_bound = np.array([0 - sensitivity, 0 - sensitivity, 0 - sensitivity]) 
	upper_bound = np.array([1 + sensitivity, 1 + sensitivity, 1 + sensitivity]) 

	msk = cv2.inRange(combined_hsv, lower_bound, upper_bound)


	percentage = calcSeg(msk)
	# print("Percentage = " + str(percentage) + '\n')
	return (percentage > min_percentage and percentage < max_percentage)


def calcSeg(msk): 
	''' 
	returns the percentage of white in a binary image 
	''' 
	height, width = msk.shape[:2] 
	num_pixels = height * width 
	count_white = cv2.countNonZero(msk) 
	percent_white = (count_white/num_pixels) * 100 
	percent_white = round(percent_white,2) 
	return percent_white

def getDigit(img, min_percentage=2.5, max_percentage=10):
	
	digit = [checkSeg(img,0,min_percentage,max_percentage),checkSeg(img,1,min_percentage,max_percentage),checkSeg(img,2,min_percentage,max_percentage),checkSeg(img,3,min_percentage,max_percentage),checkSeg(img,4,min_percentage,max_percentage),checkSeg(img,5,min_percentage,max_percentage),checkSeg(img,6,min_percentage,max_percentage)]
	
	for x in range(10):
		if digit == numbers[x]:
			# print("Found " + str(x) + ' with min %: ' + str(min_percentage) + ' max % :' + str(max_percentage))
			return x
		x += 1
	# print("Failed to Find Digit" + ' with min %: ' + str(min_percentage) + ' max % :' + str(max_percentage))
	return -1