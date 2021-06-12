import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import TEXT_LOCATION_BOTTOM_LEFT
from SelectedArea import SelectedArea as sa
from AreaDict import AreaDict

class SelectedViewer:

    def __init__(self, area_dim=(60, 100), spacing=5):
        # TODO Make selected viewer adjustable
        self.area_dim = area_dim
        self.spacing = spacing


    def draw_selected(self, graph: sg.Graph, area_dict: AreaDict, columns_rows=(3, 6)):
        # TODO Make clicking on segment open window to make per-segment adjustments
        # TODO Only erase and draw images when they are updated instead of clearing the whole graph every frame
        # TODO Use values from init
        graph.erase()
        drawn_images = 0
        for column in range(0, columns_rows[0]):
            for row in range(0, columns_rows[1]):
                if drawn_images == len(area_dict()):
                    break
                top_left = (10 + row * 70, 10 + column * 130)
                text_pos = (10 + row * 70, 125 + column * 130)
                digit, update = list(area_dict().values())[drawn_images].getDigit()
                if update:
                    graph.draw_text(f'{digit} [X]', location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                else:
                    graph.draw_text(f'{digit} [ ]', location=text_pos, text_location=TEXT_LOCATION_BOTTOM_LEFT)
                graph.draw_image(data=list(area_dict().values())[drawn_images].getProcessed(), location=top_left)
                drawn_images += 1
