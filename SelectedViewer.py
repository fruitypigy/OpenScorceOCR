from PySimpleGUI.PySimpleGUI import TEXT_LOCATION_BOTTOM_LEFT, TEXT_LOCATION_CENTER
import cv2
import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa
from ImageProcess import resize

class SelectedViewer:
    
    def __init__(self, list_size=1, area_dim=(60, 100), spacing=5):
        self.area_dim = area_dim
        self.spacing = spacing
        # self.list_size = list_size
        self.crop = lambda img, crop_coords : img[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3]]
        self.encode = lambda img : cv2.imencode('.png', img)[1].tobytes()
        self.test_img = self.encode(cv2.imread('PreviewTest.png'))
    def drawSelected(self, graph: sg.Graph, colums_rows, max_images):

        draw_images = 0
        for colum in range(0, colums_rows[0]):
            for row in range(0, colums_rows[1]):
                if draw_images == max_images:
                    break
                top_left = (10+row*70, 10+colum*130)
                text_pos = (10+row*70, 125+colum*130)
                graph.draw_text('Found Num', location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                graph.draw_image(data=self.test_img, location=(top_left)) 
                draw_images += 1 
        
        return graph