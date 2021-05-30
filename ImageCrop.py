import cv2
import numpy as np

def crop(img, x1, x2, y1, y2):
    cropped = img[y1:y2, x1:x2]
    return cropped

