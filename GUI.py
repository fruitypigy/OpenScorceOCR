import PySimpleGUI as sg
import cv2
from SelectedArea import SelectedArea as sa 
from Feed import Feed

img = cv2.imread('square.png')

backround = None

area_number = 20
area_list = [] # type: list[sa]
area_combo_list = []

area_selected = 0
list_selected = 'Area 0'


listAdjust = lambda selected, event, values : area_list[selected].adjustRectangle(event, values)
draw = lambda top_left, bottom_right, color, size : graph.draw_rectangle(top_left, bottom_right, line_color=color, line_width=size)
crop = lambda img, crop_coords : encode(img[crop_coords[0]:crop_coords[1], crop_coords[2]:crop_coords[3]])

for combo_count in range(0, area_number):
    area_combo_list.append(str('Area ' + str(combo_count))) 

graph_element = sg.Graph((400, 400), (0, 400), (400, 0), pad=(10,10), 
                    enable_events=True, key='graph', drag_submits=True)
selector_elemtent = sg.Combo(values=area_combo_list, size=(10, 5), default_value = 'Area 0', readonly=True, enable_events=True, key='area_selector')

layout = [[selector_elemtent],[graph_element, sg.Image(key='cropped')]]

window = sg.Window('Resizeable Rectangle Test', layout, return_keyboard_events=True, finalize=True)

graph = window['graph'] # type: sg.Graph

for area_count in range(0, area_number):
    area_list.append(sa(graph.DrawRectangle((-1,-1), (-1,-1))))
    area_list[area_count].adjustRectangle()    

def drawAll(event, values):

    for count in range(0, area_number):
        if count == area_selected:
            top_left, bottom_right = listAdjust(count, event, values)
            color = 'red'
            size = 4
        elif area_list[count].initiated:
            top_left, bottom_right = listAdjust(count, None, None)
            color = 'green'
            size = 1
        else:
            break

        graph.delete_figure(area_list[count].rectangle)
        area_list[count].rectangle = draw(top_left, bottom_right, color, size)


def encode(image):
    return cv2.imencode('.png', image)[1].tobytes()

feed = Feed('Tests\scoreboard.png')

graph, backround = feed.drawFrame(graph)


while True:
    
    event, values = window.read(timeout=0.1)


    # graph.delete_figure(backround)
    graph, backround = feed.drawFrame(graph)
    
    drawAll(event, values)

    if event == None:
        break
    elif event == 'area_selector':
        list_selected = values['area_selector'] # type: str
        
        for selected_count in range(area_number, -1, -1):
            if list_selected.endswith(str(selected_count)):
                area_selected = selected_count
                break
        

    crop_coords = area_list[area_selected].getCrop()
    
    cropped_encoded = crop(img, crop_coords)


    window['cropped'].update(data=cropped_encoded)