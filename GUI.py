from SelectedViewer import SelectedViewer as sv
import PySimpleGUI as sg
import cv2  
from SelectedArea import SelectedArea as sa 
from Feed import Feed
import time
from InputSetup import inputSetup
from FilterSetup import filterSetup

def main():
    feed = inputSetup()
    feed = filterSetup(feed)
    feed.resize_for_crop = True
    feed.getFrame()

    # print(feed.crop_width, feed.crop_height)

    # print(feed.h_vals, feed.s_vals, feed.v_vals)

    # feed = Feed('Tests\RealTwo.jpg')
    # feed = Feed(0)

    # feed.s_vals = (0, 40)

    # feed.config(200, 400, 200, 400)

    backround = None

    area_number = 8
    area_list = [] # type: list[sa]
    area_combo_list = []

    area_selected = 0
    list_selected = 'Area 0'

    viewer = sv()

    draw = lambda top_left, bottom_right, color, size : graph.draw_rectangle(top_left, bottom_right, line_color=color, line_width=size)

    for combo_count in range(0, area_number):
        area_combo_list.append(str('Area ' + str(combo_count))) 

    graph_element = sg.Graph((feed.crop_width, feed.crop_height), (0, feed.crop_height), (feed.crop_width, 0), pad=(10,10), 
                        enable_events=True, key='graph', drag_submits=True, background_color='black')
    viewer_graph_element = sg.Graph((480, 390), (0, 390), (480, 0), pad=(10,10), 
                        enable_events=True, key='viewer', drag_submits=True, background_color='grey')
    selector_element = sg.Listbox(values=area_combo_list, size=(10, 12), 
                        default_values = 'Area 0', enable_events=True, key='area_selector')
    text_element = sg.Text('1, 2, 3, 4, 5, 6, 7, 8, 9, 10', (60, 2), 
                        key='digits', text_color='White', background_color='grey')

    selector_col = [[selector_element], [sg.Image(key='cropped')]]

    layout = [[sg.Column(selector_col, vertical_alignment='top'), graph_element, viewer_graph_element], [text_element, sg.Button('Quit')]]

    # feed = setup(feed)

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

    def getDigits(areas: list[sa]):
        digits = [] # type: list[int]
        for count in range(len(areas)):
            digits.append(areas[count].getDigit())
        return digits

    for x in range(len(area_list)):
        area_list[x].processArea(feed.getFrame()[0])


    viewer_graph = viewer.drawSelected(viewer_graph, area_list, (6,3), area_number)

    cycles = 0


    while True:
        
        event, values = window.read(timeout=0.1)

        if event == None or event == 'Quit':
            break
        elif event == 'area_selector':
            list_selected = values['area_selector'][0] # type: str
            
            for selected_count in range(area_number, -1, -1):
                if list_selected.endswith(str(selected_count)):
                    area_selected = selected_count
                    break
        
        if event == 'graph':
            encoded, guessed = area_list[area_selected].processArea(feed.getFrame()[0], skip_digit=True)
            window['cropped'].update(data=encoded)
            cycles = 1
        elif cycles <= area_count+1:    
            area_list[cycles-1].processArea(feed.getFrame()[0])
            cycles += 1
        else:
            cycles = 1
        viewer_graph = viewer.drawSelected(viewer_graph, area_list, (3,3), area_number)
        window['cropped'].update(data=area_list[area_selected].getPreview())
        window['digits'].update((getDigits(area_list)))
        graph = feed.drawFrame(graph, True)
        drawAll(event, values)

if __name__ == '__main__':
    main()