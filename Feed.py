import cv2
import PySimpleGUI as sg
from ImageProcess import resize, process, rotate, hsvProcess

class Feed:

    def __init__(self, feed_input, desired_height=600, desired_width=600):
        self.resize_for_crop = False
        self.crop_scale = 1
        self.rot = 0
        self.h_vals = (0, 255)
        self.s_vals = (0, 255)
        self.v_vals = (0, 255)
        self.configInput(feed_input)
        self.configCrop(0, self.read().shape[0], 0, self.read().shape[1])
        self.configScale(desired_height, desired_width)
        self.configRotHSV()


    def configCrop(self, x1, x2, y1, y2, v_vals=(), h_vals=(), s_vals=(), rot=0):
        print(f'Feed Crop X1: {x1}, X2: {x2}, Y1: {y1}, Y2: {y2}')
        self.crop = lambda img : img[x1:x2, y1:y2]
        
    def configRotHSV(self, rot=0, h_vals=(0, 255), s_vals=(0, 255), v_vals=(0, 255)):
        self.rot = rot
        self.h_vals = h_vals
        self.s_vals = s_vals
        self.v_vals = v_vals

    def configScale(self, desired_height = 600, desired_width = 600):
        self.height = self.read().shape[0]
        self.width = self.read().shape[1]

        self.scale = 1
        
        print(f'Input Resolution: {self.width, self.height}')
        print(f'Desired Width: {desired_width}, Desired Height: {desired_height}')

        while self.height*self.scale > desired_height or self.width*self.scale > desired_width:
            print(f'Resizing: {int(self.width * self.scale), int(self.height * self.scale)}')
            self.scale -= 0.01
        
        # TODO add scale up toggle
        # TODO Fix scale up
        if self.scale == 1:
            while self.height*self.scale < desired_height and self.width*self.scale < desired_width:
                print(f'Resizing: {int(self.width * self.scale), int(self.height * self.scale)}')
                self.scale += 0.01
       
        self.height = int(self.height * self.scale)
        self.width = int(self.width * self.scale)
        
        print(f'Resized to {self.width, self.height}')

    def configInput(self, feed_input):
        self.feed_input = feed_input
        print(f'Feed Input: {self.feed_input}')
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

        self.height = read.shape[0]
        self.width = read.shape[1]

        dims = self.width, self.height
        read = rotate(read, self.rot)
        read = resize(read, (dims[0]*self.scale, dims[1]*self.scale))
        read = self.crop(read)
      
        if self.resize_for_crop:
            while read.shape[0]*self.crop_scale < 600 and read.shape[1]*self.crop_scale < 800:
                
                self.crop_scale += 0.125
                # print(f'Resizing: {read.shape[0]*self.crop_scale, read.shape[1]*self.crop_scale}')
                
            if self.crop_scale != 1:
                self.crop_scale -= 0.125
                self.crop_height = int(read.shape[0] * self.crop_scale)
                self.crop_width = int(read.shape[1] * self.crop_scale)
                read = resize(read, (self.crop_width, self.crop_height))

        if not raw:
            read = hsvProcess(read, h_min=self.h_vals[0], h_max=self.h_vals[1],
                                    s_min=self.s_vals[0], s_max=self.s_vals[1],
                                    v_min=self.v_vals[0], v_max=self.v_vals[1])

        frame = read, cv2.imencode('.png', read)[1].tobytes()
        return frame

    def read(self):
        if self.is_video:
            read = self.cap.read()[1]
        else:
            read = self.img
        return read
    
    def drawFrame(self, graph: sg.Graph, raw=False):
        graph.erase()
        graph.draw_image(data=self.getFrame(raw)[1], location=(0,0))
        return graph