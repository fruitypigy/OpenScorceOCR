import cv2
import numpy as np

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
	(h, w) = img.shape[:2]
	(cX, cY) = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
	return cv2.warpAffine(img, M, (w, h))


def resize(img, dim=(60, 100)):
    dim = dim
    resized = cv2.resize(img, (int(dim[0]), int(dim[1])))

    return resized

def hsvProcess(img, h_min=0, h_max=255, s_min=0, s_max=255, v_min=0, v_max=255):
    mask_vals = [h_min, h_max, s_min, s_max, v_min, v_max]
    masked = mask(img, mask_vals)
    return cv2.merge((masked, masked, masked))
    
def process(img, h_min=0, h_max=255, s_min=0, s_max=255, v_min=0, v_max=255, scale=100, dim=(60,100), angle=0):
    # print('Processing with v_max: ' + str(v_max) + ' scale: ' + str(scale))
    mask_vals = [h_min, h_max, s_min, s_max, v_min, v_max]
    
    masked = mask(img, mask_vals)
    rotated = rotate(masked, angle)
    cropped = crop(rotated, scale*0.01)
    resized = resize(cropped, dim)

    merged = cv2.merge((resized, resized, resized))

    return merged

def warpPerspective(img, coords, dims=(600,300)):
    if type(coords) != list:
        coords = list(coords)

    width, height = dims

    pts1 = np.float32(coords)
    pts2 = np.float32([[0,0], [width, 0], [0,height], [width, height]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    transformed = cv2.warpPerspective(img, matrix, (width, height))

    transformed_encoded = cv2.imencode('.png', transformed)[1].tobytes()

    return transformed, transformed_encoded