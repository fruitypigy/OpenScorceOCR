from typing import Sized
import cv2
import PySimpleGUI as sg
from numpy import select
from ImageProcess import resize, process, rotate, hsvProcess

class Feed:

    def __init__(self, feed_input):

        self.configInput(feed_input)
        self.configScale()

        self.config(0, self.height, 0, self.width)

    def config(self, x1, x2, y1, y2, v_vals=(), h_vals=(), s_vals=(), rot=0):
        self.crop = lambda img : img[x1:x2, y1:y2]
        self.rot = rot
        self.v_vals = v_vals
        self.h_vals = h_vals
        self.s_vals = s_vals
        
    def configScale(self):
        self.height = self.read().shape[0]
        self.width = self.read().shape[1]
        
        self.scale = 1
        self.skip_resize = True
        # resized = False

        print(f'Input Resolution: {self.height, self.width}')
        while self.height*self.scale > 600 or self.width*self.scale > 800:
            print(f'Resizing: {int(self.height*self.scale), int(self.width*self.scale)}')
            self.skip_resize = False
            resized = True
            self.scale -= 0.1

        # TODO add scale up toggle
        # while not resized and (self.height*self.scale < 600 or self.width*self.scale < 800):
        #     print(f'Resizing: {int(self.height*self.scale), int(self.width*self.scale)}')
        #     self.skip_resize = False
        #     self.scale += 0.1

        self.height = int(self.height * self.scale)
        self.width = int(self.width * self.scale)

    def configInput(self, feed_input):
        self.feed_input = feed_input
        if type(feed_input) == int:
            self.is_video = True
            self.cap = cv2.VideoCapture(feed_input)

        elif type(feed_input) == str:
            self.is_video = False
            self.img = cv2.imread(feed_input)

        else:
            exit(1)

    def getFrame(self, raw=False):
        read = self.read()

        if not self.skip_resize:
            dims = int(self.width), int(self.height)
            read = resize(read, dims)

        read = self.crop(read)
        read = rotate(read, self.rot)
        if not raw:
            read = hsvProcess(read, v_max=30)

        frame = read, cv2.imencode('.png', read)[1].tobytes()
        return frame

    def read(self):
        if self.is_video:
            read = self.cap.read()[1]
        else:
            read = self.img
        return read
    
    def drawFrame(self, graph: sg.Graph):
        graph.erase()
        graph.draw_image(data=self.getFrame()[1], location=(0,0))
        return graph