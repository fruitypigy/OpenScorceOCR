import cv2
import PySimpleGUI as sg

class Feed:

    def __init__(self, feed_input=0):
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

    def getFrame(self):
        if self.is_video:
            frame = self.cap.read()[1], cv2.imencode('.png', self.cap.read()[1])[1].tobytes()
            return frame
        else:
            frame = self.img, cv2.imencode('.png', self.img)[1].tobytes(), cv2.imencode('.png', self.img)[1].tobytes()
            return frame
    
    def drawFrame(self, graph: sg.Graph):
        graph.draw_image(data=self.getFrame()[1], location=(0,0))
        return graph