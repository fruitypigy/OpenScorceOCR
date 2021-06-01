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

        # self.test_img = self.encode(cv2.imread('PreviewTest.png'))
    
    def drawSelected(self, graph: sg.Graph, areas: list[sa], colums_rows, max_images):
        
        graph.erase()
        drawn_images = 0
        for colum in range(0, colums_rows[0]):
            for row in range(0, colums_rows[1]):
                if drawn_images == max_images:
                    break
                top_left = (10+row*70, 10+colum*130)
                text_pos = (10+row*70, 125+colum*130)
                graph.draw_text(areas[drawn_images].getProcessed()[1], location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                graph.draw_image(data=areas[drawn_images].getProcessed()[0], location=(top_left)) 
                drawn_images += 1 
        
        return graph