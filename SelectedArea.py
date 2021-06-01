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
        self.processed = None
        self.guessed = -1

    def adjustRectangle(self, graph: sg.Graph, event=None, values=None, is_main=False):
        self.initiated = True
        if is_main:
            line_color = 'red'
            size = 4
        else:
            line_color = 'green'
            size = 2

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

    def getCrop(self, frame):

        self.coords = [self.bottom_right[1], self.top_left[1], 
                self.top_left[0], self.bottom_right[0]] 

        for x in range(len(self.coords)):
            if self.coords[x-1] < 0:
                self.coords[x-1] = 0

        frame = frame[self.coords[0]:self.coords[1], self.coords[2]:self.coords[3]]
        encoded = cv2.imencode('.png', frame)[1].tobytes()
        return encoded, frame
        
    def processArea(self, frame, skip_digit=False):
        cropped = self.getCrop(frame)[1]
        self.processed = ip.process(cropped, v_max=40)
        if not skip_digit:
            self.guessed = getDigit(self.processed)
        self.processed = ip.resize(self.processed, (60,100))
        self.processed_encoded = cv2.imencode('.png', self.processed)[1].tobytes()
        return self.processed_encoded, self.guessed
        
    def getProcessed(self):
        return self.processed_encoded, self.guessed