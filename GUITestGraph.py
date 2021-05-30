import time
from itertools import cycle
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import TRANSPARENT_BUTTON, Window
import numpy as np
import cv2
import ImageProcess
import OpenCVMatch as match
import gc



file_event, file_values = sg.Window('Get filename example', [[sg.Text('Filename')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()] ]).read(close=True)
img = cv2.imread(file_values[0]) # type: np.ndarray
encoded = cv2.imencode('.png', img)[1].tobytes()

# cap = cv2.VideoCapture(0)
# img = cap.read()[1]
# encoded = cv2.imencode('.png', cap.read()[1])[1].tobytes()



height = img.shape[0]
width = img.shape[1]

valmx_slider = [sg.Text('Val Max'), sg.Slider((0, 255), 255, orientation='horizontal', key='-VAL_MX_Slider', enable_events=True),
                sg.Text('Val Min'), sg.Slider((0, 255), 0, orientation='horizontal', key='-VAL_MN_Slider', enable_events=True)]
satmx_slider = [sg.Text('Sat Max'), sg.Slider((0, 255), 255, orientation='horizontal', key='-SAT_MX_Slider', enable_events=True),
                sg.Text('Sat Min'), sg.Slider((0, 255), 0, orientation='horizontal', key='-SAT_MN_Slider', enable_events=True)]
huemx_slider = [sg.Text('Hue Max'), sg.Slider((0, 255), 255, orientation='horizontal', key='-HUE_MX_Slider', enable_events=True),
                sg.Text('Hue Min'), sg.Slider((0, 255), 0, orientation='horizontal', key='-HUE_MN_Slider', enable_events=True)]

input_graph_element = sg.Graph( canvas_size=(width, height), graph_bottom_left=(0, height), graph_top_right=(width, 0), enable_events=True, drag_submits=True, key="graph" )

guessed_element = [sg.Text('Failed to Find Value', background_color='white',  text_color='red', font='Courier 25', size=(20,1) ,key='FOUND')]

image_layout = [
        [input_graph_element, sg.Image(key='selected'), sg.Image(key='-PROCCESSED-')],
        [guessed_element],
        [valmx_slider],
        [satmx_slider],
        [huemx_slider]
]


image_window = sg.Window("GUI Graph Test", image_layout, finalize=True)

graph = image_window["graph"] # type: sg.Graph
feed = graph.draw_image(data=encoded, location=(0, 0))

dragging = False
startpoint = None
endpoint = None
rectangle = None
cropped = img
v_max_slider = s_max_slider = h_max_slider = 255
v_min_slider = s_min_slider = h_min_slider = 0
old_v_max_slider = old_s_max_slider = old_h_max_slider = 255
old_v_min_slider = old_s_min_slider = old_h_min_slider = 0
x1 = x2 = y1 = y2 = None
cycle_time_start = time.time()
cycles_per_second = 0
cycles = 0
start_proccess = False

print(cycle_time_start)

while True:
    
    gc.collect()
    if  cycles >= 10:
        cycles_per_second = int(cycles / (time.time() - cycle_time_start))
        cycle_time_start = time.time()
        cycles = 0

    # img = cap.read()[1]
    # encoded = cv2.imencode('.png', cap.read()[1])[1].tobytes()
    start_proccess = True
    
    graph.delete_figure(feed)
    feed = graph.draw_image(data=encoded, location=(0, 0))
    graph.draw_text((str(cycles_per_second) + ' Cycles/Second'), (70,30), color='white')

    if (startpoint != None and endpoint != None) and (startpoint != endpoint):

        rectangle = graph.draw_rectangle(startpoint, endpoint, line_color="white", line_width=4)
    
    event, values = image_window.Read(timeout=0.1)

    if event in ('-VAL_MX_Slider', '-VAL_MN_Slider', '-SAT_MX_Slider','-SAT_MN_Slider', '-HUE_MX_Slider', '-HUE_MN_Slider'):
        
        v_max_slider = int(values['-VAL_MX_Slider'])
        v_min_slider = int(values['-VAL_MN_Slider'])
        s_max_slider = int(values['-SAT_MX_Slider'])
        s_min_slider = int(values['-SAT_MN_Slider'])
        h_max_slider = int(values['-HUE_MX_Slider'])
        h_min_slider = int(values['-HUE_MN_Slider'])
        
        if True:
        # print(old_v_max_slider, old_v_min_slider, v_max_slider, v_min_slider)
        # if ((old_v_max_slider, old_v_min_slider, old_s_max_slider, old_s_min_slider, old_h_max_slider, old_h_min_slider) 
            # != (v_max_slider, v_min_slider, s_max_slider, s_min_slider, h_max_slider, h_min_slider)):
            
            old_v_max_slider, old_v_min_slider, old_s_max_slider, old_s_min_slider, old_h_max_slider, old_h_min_slider = v_max_slider, v_min_slider, s_max_slider, s_min_slider, h_max_slider, h_min_slider
             
            cropped = img[y1:y2 , x1:x2]
            cropped_encoded = cv2.imencode('.png', cropped)[1].tobytes()
            # window['selected'].update(data=cropped_encoded)
            
            cropped_dim = (x2-x1, y2-y1)
            proccessed = ImageProcess.process(cropped, v_max=v_max_slider, v_min=v_min_slider,
                                        s_max=s_max_slider, s_min=s_min_slider, 
                                        h_max=h_max_slider, h_min=h_min_slider, dim=cropped_dim)
            processed_encoded = cv2.imencode('.png', proccessed)[1].tobytes()
            image_window['-PROCCESSED-'].update(data=processed_encoded)


    if (start_proccess and (startpoint != None and endpoint != None) and (startpoint[0] != endpoint[0]) and (startpoint[1] != endpoint[1])):
        

        # print(bool(startpoint == endpoint))
        x1, x2, y1, y2 = startpoint[0], endpoint[0], startpoint[1], endpoint[1]

        if x2 < 0:
            x2 = 0
            # print("X Less")
        if y2 < 0:
            # print("Y Less")
            y2 = 0

        if x2 < x1:
            x1, x2 = x2, x1
        
        if y2 < y1:
            y1, y2 = y2, y1

        cropped = img[y1:y2 , x1:x2]
        cropped_encoded = cv2.imencode('.png', cropped)[1].tobytes()
        # window['selected'].update(data=cropped_encoded)

        cropped_dim = (x2-x1, y2-y1)
        proccessed = ImageProcess.process(cropped, v_max=v_max_slider, v_min=v_min_slider, 
                                    s_max=s_max_slider, s_min=s_min_slider,
                                    h_max=h_max_slider, h_min=h_min_slider, dim=cropped_dim)

        processed_encoded = cv2.imencode('.png', proccessed)[1].tobytes()
        image_window['-PROCCESSED-'].update(data=processed_encoded)
    
    if event == 'graph':

        cursor_pos = values['graph']

        if not dragging:
            graph.delete_figure(rectangle)
            dragging = True
            startpoint = cursor_pos
            endpoint = cursor_pos
        else:
            endpoint = cursor_pos
            graph.delete_figure(rectangle)
            

        # print('Cursor Position: cursor_pos)
        # print('Start Point: ', startpoint)
        # print('End Point: ', endpoint)

    elif event.endswith('+UP'):

        dragging = False
        # startpoint = (0,0)
        # endpoint = (1,1)

    # elif event == 'Find Value':

    #     if cropped.any():
                #         guess = match.getDigit(ImageProcess.process(cropped, v_max=v_max_slider))
    #         if guess > -1:
    #             sg.popup(('Found ' + str(guess))) 
    
    if cropped.any() and start_proccess:
        
        start_proccess = False
        guess = match.getDigit(ImageProcess.process(cropped, v_max=v_max_slider))
        if guess > -1:
            # sg.popup(('Found ' + str(guess)))
            image_window['FOUND'].update(('Guessed Value: ' + str(guess)))
        else:
            image_window['FOUND'].update(('Failed to Find Value' + str(guess)))

    if event is None:
        break
    
    cycles += 1