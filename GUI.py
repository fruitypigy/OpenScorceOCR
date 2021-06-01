from SelectedViewer import SelectedViewer as sv
import PySimpleGUI as sg
import cv2
from SelectedArea import SelectedArea as sa 
from Feed import Feed


feed = Feed('Tests\scoreboard.png')

backround = None

area_number = 5
area_list = [] # type: list[sa]
area_combo_list = []

area_selected = 0
list_selected = 'Area 0'

viewer = sv()

draw = lambda top_left, bottom_right, color, size : graph.draw_rectangle(top_left, bottom_right, line_color=color, line_width=size)

for combo_count in range(0, area_number):
    area_combo_list.append(str('Area ' + str(combo_count))) 

graph_element = sg.Graph((400, 400), (0, 400), (400, 0), pad=(10,10), 
                    enable_events=True, key='graph', drag_submits=True)
viewer_graph_element = sg.Graph((400, 400), (0, 400), (400, 0), pad=(10,10), 
                    enable_events=True, key='viewer', drag_submits=True)

selector_elemtent = sg.Combo(values=area_combo_list, size=(10, 5), default_value = 'Area 0', readonly=True, enable_events=True, key='area_selector')

layout = [[selector_elemtent],[graph_element, sg.Image(key='cropped'), viewer_graph_element]]

window = sg.Window('Main', layout, return_keyboard_events=True, finalize=True)

graph = window['graph'] # type: sg.Graph
viewer_graph = window['viewer'] # type: sg.Graph

for area_count in range(0, area_number):
    area_list.append(sa(graph.draw_rectangle((-1,-1), (-1,-1))))
    graph = area_list[area_count].adjustRectangle(graph)    

def drawAll(event, values):

    for count in range(0, area_number):
        if count == area_selected:
            area_list[count].adjustRectangle(graph, event, values, True)
        elif area_list[count].initiated:
            area_list[count].adjustRectangle(graph)

for x in range(len(area_list)):
    area_list[x].processArea(feed.getFrame()[0])


viewer_graph = viewer.drawSelected(viewer_graph, area_list, (3,3), area_number)

cycles = 0

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
    
    if event == 'graph':
        area_list[area_selected].processArea(feed.getFrame()[0], skip_digit=True)
        cycles = 10
    elif cycles >= 10:    
        for area_count in range(len(area_list)):
            area_list[area_count].processArea(feed.getFrame()[0])
            cycles = 0
    else:
        cycles += 1
    
    viewer_graph = viewer.drawSelected(viewer_graph, area_list, (3,3), area_number)
    window['cropped'].update(data=area_list[area_selected].getCrop(feed.getFrame()[0])[0])
    graph.erase()
    graph = feed.drawFrame(graph)
    drawAll(event, values)
