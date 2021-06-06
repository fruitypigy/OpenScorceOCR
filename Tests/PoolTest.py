from OpenCVMatch import getDigit
from GUI import process
from multiprocessing import Pool
from os import name
from PySimpleGUI.PySimpleGUI import I
import cv2
import ImageProcess as ip
import time


class imageWriter:
    def __init__(self, img_path, number) -> None:
        self.img = cv2.imread(img_path)
        self.number = number
    def writeProcessed(self):
        name = str(self.number) + '.png'
        processed = ip.process(self.img, v_max=50)
        print(getDigit(processed))
        # cv2.imwrite(name, processed)
        print('Finished')

def writeImage(iw: imageWriter):
    iw.writeProcessed()

if __name__ == '__main__':



    writerList = []
    for x in range(0,100):
        writerList.append(imageWriter('Tests\RawEightTwo.jpg', x))

    while True:
        # start = time.time()
        # with Pool(16) as p:
        #     p.map(writeImage, writerList)
        #     # print(p.map(writeImage, writerList))
        # pooltime = time.time()- start
        # nopooltime = None


        start = time.time()
        for count in range(len(writerList)):
            writeImage(writerList[count])
            print('No Pool')
        pooltime = None
        nopooltime = time.time() - start

        print('Pool time: ' + str(pooltime) + '\nNo Pool Time: ' + str(nopooltime))
        # time.sleep(0.5)