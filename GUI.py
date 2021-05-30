import PySimpleGUI as sg
import cv2
from SelectedArea import SelectedArea as sa 

img = cv2.imread('square.png')

backround = None

area_number = 20
area_list = [] # type: list[sa]
area_combo_list = []

area_selected = 0
list_selected = 'Area 0'


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

    for draw_count in range(0, area_number):
        # print(area_selected)
        if draw_count == area_selected:
            top_left, bottom_right = area_list[draw_count].adjustRectangle(event, values)
            color = 'red'
        elif area_list[draw_count].initiated:
            top_left, bottom_right = area_list[draw_count].adjustRectangle()
            color = 'black'
        else:
            break

        graph.delete_figure(area_list[draw_count].rectangle)
        area_list[draw_count].rectangle = (graph.draw_rectangle(top_left, bottom_right, line_color=color))


def encode(image):
    return cv2.imencode('.png', image)[1].tobytes()

backround = graph.draw_image(data=encode(img), location=(0,0))

while True:
    
    event, values = window.read(timeout=0.1)

    # graph.delete_figure(backround)
    # backround = graph.draw_image(data=encode(img), location=(0,0))
    
    drawAll(event, values)
    print(values)

    if event == None:
        break
    elif event == 'area_selector':
        list_selected = values['area_selector'] # type: str
        print('Combo Sees: ' + str(list_selected))
        
        for selected_count in range(area_number, -1, -1):
            if list_selected.endswith(str(selected_count)):
                area_selected = selected_count
                break
        

    crop_coords = area_list[area_selected].getCrop()

    cropped = img[crop_coords[0]:crop_coords[1], 
                    crop_coords[2]:crop_coords[3]]

    cropped_encoded = encode(cropped)
    window['cropped'].update(data=cropped_encoded)