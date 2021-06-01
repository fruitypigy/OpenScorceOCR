import PySimpleGUI as sg
import cv2
from SelectedArea import SelectedArea as sa 
from Feed import Feed

img = cv2.imread('square.png')
feed = Feed('square.png')

backround = None

area_number = 20
area_list = [] # type: list[sa]
area_combo_list = []

area_selected = 0
list_selected = 'Area 0'


draw = lambda top_left, bottom_right, color, size : graph.draw_rectangle(top_left, bottom_right, line_color=color, line_width=size)

for combo_count in range(0, area_number):
    area_combo_list.append(str('Area ' + str(combo_count))) 

graph_element = sg.Graph((400, 400), (0, 400), (400, 0), pad=(10,10), 
                    enable_events=True, key='graph', drag_submits=True)
selector_elemtent = sg.Combo(values=area_combo_list, size=(10, 5), default_value = 'Area 0', readonly=True, enable_events=True, key='area_selector')

layout = [[selector_elemtent],[graph_element, sg.Image(key='cropped')]]

window = sg.Window('Resizeable Rectangle Test', layout, return_keyboard_events=True, finalize=True)

graph = window['graph'] # type: sg.Graph

for area_count in range(0, area_number):
    area_list.append(sa(graph.draw_rectangle((-1,-1), (-1,-1))))
    graph = area_list[area_count].adjustRectangle(graph)    

def drawAll(event, values):

    for count in range(0, area_number):
        if count == area_selected:
            area_list[count].adjustRectangle(graph, event, values, True)
        elif area_list[count].initiated:
            area_list[count].adjustRectangle(graph)


while True:
    
    event, values = window.read(timeout=0.1)

    if event == None:
        break
    elif event == 'area_selector':
        list_selected = values['area_selector'] # type: str
        
        for selected_count in range(area_number, -1, -1):
            if list_selected.endswith(str(selected_count)):
                area_selected = selected_count
                break
        

    window['cropped'].update(data=area_list[area_selected].getCrop(img))
    graph.erase()
    graph = feed.drawFrame(graph)
    drawAll(event, values)
