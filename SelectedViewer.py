import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import TEXT_LOCATION_BOTTOM_LEFT
from SelectedArea import SelectedArea as sa

class SelectedViewer:
    
    def __init__(self, area_dim=(60, 100), spacing=5):
        self.area_dim = area_dim
        self.spacing = spacing
    
    def drawSelected(self, graph: sg.Graph, areas: list[sa], colums_rows, max_images):
        # TODO Make clicking on segment open window to make per-segment adjustments
        graph.erase()
        drawn_images = 0
        for colum in range(0, colums_rows[0]):
            for row in range(0, colums_rows[1]):
                if drawn_images == max_images:
                    break
                top_left = (10+row*70, 10+colum*130)
                text_pos = (10+row*70, 125+colum*130)
                digit, update = areas[drawn_images].getDigit()
                if update:
                    graph.draw_text(f'{digit} [X]', location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                else:
                    graph.draw_text(f'{digit}', location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                graph.draw_image(data=areas[drawn_images].getProcessed(), location=(top_left)) 
                drawn_images += 1 
        
        return graph