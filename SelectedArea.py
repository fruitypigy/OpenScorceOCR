import cv2
import ImageProcess as  ip
import PySimpleGUI as sg
from OpenCVMatch import getDigit

class SelectedArea:

    def __init__(self, rectangle, pos = (200, 200), dim = (5, 5)):
        self.dim = dim
        self.pos = pos
        self.rectangle = rectangle
        self.length = 30
        self.height = 50
        self.top_left = (0,1)
        self.bottom_right = (1,0)
        self.initiated = False

    def adjustRectangle(self, graph: sg.Graph, event=None, values=None, is_main=False):
        self.initiated = True
        if is_main:
            line_color = 'red'
            size = 4
        else:
            line_color = 'green'
            size = 1

        if event == 'graph':
            self.pos = values['graph']
        elif event == ',':
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif event == ';':
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif event == '/':
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif event == '.':
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif event == 'MouseWheel:Up' and self.length < 120: 
            self.length += 3
            self.height += 5
        elif event == 'MouseWheel:Down' and self.length > 3:
            self.length -= 3
            self.height -= 5
        
        self.top_left = (self.pos[0] - self.length, self.pos[1] + self.height)
        self.bottom_right = (self.pos[0] + self.length, self.pos[1] - self.height)

        graph.draw_rectangle(self.top_left, self.bottom_right, line_color=line_color, line_width=size)

        return graph

    def getCrop(self, img):
        
        #TODO return cropped area instead of coords
        self.coords = [self.bottom_right[1], self.top_left[1], 
                self.top_left[0], self.bottom_right[0]] 

        for x in range(len(self.coords)):
            if self.coords[x-1] < 0:
                self.coords[x-1] = 0

        img = img[self.coords[0]:self.coords[1], self.coords[2]:self.coords[3]]
        encoded = cv2.imencode('.png', img)[1].tobytes()
        return encoded
        # return self.coords
    def processArea(self):
        pass
    
    def getProcessed(self):
        pass