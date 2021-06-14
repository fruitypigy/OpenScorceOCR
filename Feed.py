import cv2
import PySimpleGUI as sg
from ImageProcess import resize, process, rotate, hsvProcess, warpPerspective


class Feed:

    def __init__(self, feed_input, desired_height=600, desired_width=600):
        self.resize_for_crop = False
        self.crop_scale = 1
        self.rot = 0
        self.h_vals = (0, 255)
        self.s_vals = (0, 255)
        self.v_vals = (0, 255)
        self.skip_warp = True
        self.configInput(feed_input)
        self.configCrop(0, self.read().shape[0], 0, self.read().shape[1])
        self.configScale(desired_height, desired_width)
        self.configRotHSV()

    def config_crop(self, x1, x2, y1, y2):
        print(f'Feed Crop X1: {x1}, X2: {x2}, Y1: {y1}, Y2: {y2}')
        self.crop = lambda img: img[x1:x2, y1:y2]

    def configRotHSV(self, rot=0, h_vals=(0, 255), s_vals=(0, 255), v_vals=(0, 255)):
        self.rot = rot
        self.h_vals = h_vals
        self.s_vals = s_vals
        self.v_vals = v_vals

    def config_scale(self, desired_height=600, desired_width=600):
        self.height = self.read().shape[0]
        self.width = self.read().shape[1]

        self.scale = 1

        print(f'Input Resolution: {self.width, self.height}')
        print(f'Desired Width: {desired_width}, Desired Height: {desired_height}')

        while self.height * self.scale > desired_height or self.width * self.scale > desired_width:
            print(f'Resizing: {int(self.width * self.scale), int(self.height * self.scale)}')
            self.scale -= 0.01

        # TODO add scale up toggle
        # TODO Fix scale up
        if self.scale == 1:
            while self.height * self.scale < desired_height and self.width * self.scale < desired_width:
                print(f'Resizing: {int(self.width * self.scale), int(self.height * self.scale)}')
                self.scale += 0.01

        self.height = int(self.height * self.scale)
        self.width = int(self.width * self.scale)

        print(f'Resized to {self.width, self.height}')

    def configWarp(self, coords, dims):
        self.warp_coords = ((int(coords[0][0] / self.scale), int(coords[0][1] / self.scale)),
                            (int(coords[1][0] / self.scale), int(coords[1][1] / self.scale)),
                            (int(coords[2][0] / self.scale), int(coords[2][1] / self.scale)),
                            (int(coords[3][0] / self.scale), int(coords[3][1] / self.scale)))
        print(f'Orignial Size: {self.read().shape[1], self.read().shape[0]}\n'
              f'Adjusted Coords: {self.warp_coords}\n'
              f'Current Size: {self.width, self.height}\n'
              f'Current Warp Coords: {coords}\n'
              f'Current Scale: {self.scale}')
        self.scale = 1
        self.warp_dims = dims
        self.skip_warp = False

    def configInput(self, feed_input):
        self.feed_input = feed_input
        print(f'Feed Input: {self.feed_input}')
        if type(feed_input) == int or feed_input.endswith('.mp4'):
            self.is_video = True
            self.cap = cv2.VideoCapture(feed_input)
        else:
            self.is_video = False
            self.img = cv2.imread(feed_input)

    def getFrame(self, raw=False):
        read = self.read()

        self.height = read.shape[0]
        self.width = read.shape[1]

        dims = self.width, self.height
        read = rotate(read, self.rot)
        read = resize(read, (dims[0] * self.scale, dims[1] * self.scale))

        if not self.skip_warp:
            read = warpPerspective(read, self.warp_coords, self.warp_dims)[0]

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
        graph.draw_image(data=self.get_frame(raw)[1], location=(0, 0))
