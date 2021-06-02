import cv2
import OpenCVMatch
import numpy as np
import ImageProcess

def crop(img, scale):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

def mask(img, mask_vals):
    combined_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([mask_vals[0], mask_vals[2], mask_vals[4]])
    upper_bound = np.array([mask_vals[1], mask_vals[3], mask_vals[5]]) 

	#create mask
    return cv2.inRange(combined_hsv, lower_bound, upper_bound)

def rotate(img, angle):
    # grab the dimensions of the image and calculate the center of the
	# image
	(h, w) = img.shape[:2]
	(cX, cY) = (w // 2, h // 2)
	# rotate our image by 45 degrees around the center of the image
	M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
	return cv2.warpAffine(img, M, (w, h))


def resize(img, dim=(279,469)):
    dim = dim
    resized = cv2.resize(img, dim)

    return resized

def process(img, h_min=0, h_max=255, s_min=0, s_max=255, v_min=0, v_max=255, scale=100, dim=(279,469), angle=0):

    # print('Processing with v_max: ' + str(v_max) + ' scale: ' + str(scale))
    mask_vals = [h_min, h_max, s_min, s_max, v_min, v_max]
    
    masked = mask(img, mask_vals)
    rotated = rotate(masked, angle)
    cropped = crop(rotated, scale*0.01)
    resized = resize(cropped, dim)
    # blurred = cv2.bilateralFilter(resized, 20, 150, 150)
    
    merged = cv2.merge((resized, resized, resized))

    # merged = cv2.merge((blurred, blurred, blurred))
    # cv2.imshow('Blurred', blurred)
    # cv2.imshow('Resized', resized)
    # cv2.waitKey()

    return merged