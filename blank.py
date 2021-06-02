import ImageProcess as ip
import cv2

images = ('Segments\SegBM.jpg', 'Segments\SegBR.jpg', 'Segments\SegBL.jpg',
        'Segments\SegM.jpg', 'Segments\SegTM.jpg',
        'Segments\SegTR.jpg', 'Segments\SegTL.jpg')
for x in range(len(images)):
    img = cv2.imread(images[x])
    resized = ip.resize(img, (60, 100))
    cv2.imwrite(images[x], resized)