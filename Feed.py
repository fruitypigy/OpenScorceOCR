from typing import Sized
import cv2
import PySimpleGUI as sg
from ImageProcess import resize, process, rotate, hsvProcess

class Feed:

    def __init__(self, feed_input):
        self.feed_input = feed_input
        self.backround = None

        if type(feed_input) == int:
            self.is_video = True
            self.cap = cv2.VideoCapture(feed_input)

        elif type(feed_input) == str:
            self.is_video = False
            self.img = cv2.imread(feed_input)

        else:
            exit(1)

        if self.is_video:
            read = self.cap.read()[1]
        else:
            read = self.img

        height = read.shape[0]
        width = read.shape[1]
        print((height, width))
        self.config(0, height, 0, width)

    def config(self, x1, x2, y1, y2, scale=1, v_vals=(), h_vals=(), s_vals=(), rot=0):
        self.crop = lambda img : img[x1:x2, y1:y2]
        self.sclae = scale
        self.rot = rot
        self.v_vals = v_vals
        self.h_vals = h_vals
        self.s_vals = s_vals


    def getFrame(self, raw=False):
        if self.is_video:
            read = self.cap.read()[1]
        else:
            read = self.img

        # for x in range(len(self.coords)):
        #     if self.coords[x-1] < 0:
        #         self.coords[x-1] = 0

        read = self.crop(read)
        read = rotate(read, self.rot)
        read = hsvProcess(read, v_max=30)
        # cropped = read[self.coords[0]:self.coords[1], self.coords[2]:self.coords[3]]

        # dims = int(read.shape[1]*self.scale), int(read.shape[0]*self.scale)
        # resized = resize(read, dims)
        frame = read, cv2.imencode('.png', read)[1].tobytes()
        return frame
    
    def drawFrame(self, graph: sg.Graph):
        graph.draw_image(data=self.getFrame()[1], location=(0,0))
        return graph