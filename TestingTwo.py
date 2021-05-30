import cv2
import ImageProcess
import OpenCVMatch

img = cv2.imread('Tests\Two2.jpg')

cv2.imwrite('OUTPUT.jpg', img)

processed = ImageProcess.process(img, h_max=255, s_max=255, v_max=163, scale=87, angle=3)

print(OpenCVMatch.getDigit(processed))