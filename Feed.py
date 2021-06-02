import cv2
import PySimpleGUI as sg
from ImageProcess import resize

class Feed:

    def __init__(self, feed_input=0, scale=1):
        self.feed_input = feed_input
        self.backround = None
        self.scale = scale

        if type(feed_input) == int:
            self.is_video = True
            self.cap = cv2.VideoCapture(feed_input)

        elif type(feed_input) == str:
            self.is_video = False
            self.img = cv2.imread(feed_input)

        else:
            exit(1)

    def getFrame(self):
        if self.is_video:
            read = self.cap.read()[1]
        else:
            read = self.img
        dims = int(read.shape[1]*self.scale), int(read.shape[0]*self.scale)
        resized = resize(read, dims)
        frame = resized, cv2.imencode('.png', resized)[1].tobytes()
        return frame
    
    def drawFrame(self, graph: sg.Graph):
        graph.draw_image(data=self.getFrame()[1], location=(0,0))
        return graph