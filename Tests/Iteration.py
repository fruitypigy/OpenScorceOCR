import itertools
import OpenCVMatch
import cv2
import numpy as np
import ImageProcess
import time
from PIL import Image
import json

print("INIT")

img = cv2.imread('Tests\RawSmallNine.jpg')

min_percentage = 2.5
max_percentage = 10

img_array = []
found_array = []



def iterate(img):
    start = time.time()
    cycles = 0
    for h in range(0, 1, 3):
        for x in range(0, 61, 4):
            for y in range(0,26, 3):
                for z in range(0,5):
                    scale_val = 100-y
                    v_val = 100-x
                    angle_val = z
                    # min_percentage = 3.5 - h * 0.1

                    # scale_val = 80
                    # v_val = 51
                    # angle_val = 0

                    print('v_val:' + str(v_val) 
                        + ' min%: ' + str(min_percentage) 
                        + ' angle: ' + str(angle_val) 
                        + ' scale: ' + str(scale_val))

                    processed = ImageProcess.process(img, h_max=255, s_max=255, v_max=v_val, scale=scale_val, angle=angle_val)
                    # if count == 2:
                    #     height, width, layers = processed.shape
                    #     size = (width,height)
                    #     img_array.append(processed)
                    #     count = 0
                    # else:                
                    #     count += 1
                    found = (OpenCVMatch.check_seg(processed, 1, min_percentage, max_percentage)
                             or OpenCVMatch.check_seg(processed, 5, min_percentage, max_percentage))
                    if found:
                        possible_digit = OpenCVMatch.get_digit(processed, min_percentage, max_percentage)
                        print(possible_digit)
                        if possible_digit != -1:
                            print('Found ' + str(possible_digit))
                            return cycles, processed, found, start, [v_val, scale_val, angle_val]
                    print('Cycle ' + str(cycles))
                    cycles += 1
    return cycles, processed, found, start

cycles, processed, found, start, settings = iterate(img)


passed = time.time() - start
cycles_per_second = cycles/passed
print('Finished on cycle: ' + str(cycles)
        + ' using values\nv_val: ' + str(settings[0]) 
        + '\nscale_val: ' + str(settings[1]) 
        + '\nangle_val ' + str(settings[2]))
        
print(str(cycles_per_second) + ' cycles per second') 

                # if not (found in found_array):
                #     found_array.append(found)

cv2.imshow("Final", processed)
cv2.imshow("Initial", ImageProcess.resize(img))

# out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()

cv2.waitKey()


# cv2.imshow('Image', img)
# cv2.waitKey()

# print(count)

# stuff = [1, 2, 3]
# for L in range(0, len(stuff)+1):
#     for subset in itertools.combinations(stuff, L):
#         print(subset)

# 0,0,0
# 1,0,0
# 2,0,0
# 3,0,0
# 4,0,0
# 5,0,0
# 0,1,0
# 1,1,0
# 2,1,0
# 3,1,0
# 4,1,0
# 5,1,0

# a - 0-5, b 0-20, c 0-85