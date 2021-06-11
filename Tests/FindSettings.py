import cv2
import numpy as np
import ImageProcess
import OpenCVMatch

def guessV(img, acceptable_range):
    for x in range(256):
        val = 256-x

        msk = ImageProcess.mask(img, [0,255, 0,255, 0,(val)])
        ''' 
        returns the percentage of white in a binary image 
        ''' 
        height, width = msk.shape[:2] 
        num_pixels = height * width 
        count_white = cv2.countNonZero(msk) 
        percent_white = (count_white/num_pixels) * 100 
        percent_white = round(percent_white,2)  
        print('White: ' + str(percent_white) + '% Value:' + str(val))
        
        if percent_white <= acceptable_range:
            print("Possible value: " + str(val))
            return val
        x += 1

img = cv2.imread('Tests\RawSmallNine.jpg')
v_max = guessV(img, 40)

processed = ImageProcess.process(img, 0,255,0,255,0,v_max, scale=86, angle=2)

print(OpenCVMatch.get_digit(processed, 2))