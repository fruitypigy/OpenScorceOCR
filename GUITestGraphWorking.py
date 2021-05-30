import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import TRANSPARENT_BUTTON
import numpy as np
import cv2
import ImageProcess
import OpenCVMatch as match



file_event, file_values = sg.Window('Get filename example', [[sg.Text('Filename')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()] ]).read(close=True)

img = cv2.imread(file_values[0]) # type: np.ndarray
encoded = cv2.imencode('.png', img)[1].tobytes() 

height = img.shape[0]
width = img.shape[1]

val_slider = sg.Slider((0, 255), 255, orientation='horizontal', key='-VALSlider-', enable_events=True)



layout = [
    [
        sg.Text('Val Max'), val_slider,
        sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, height),
            graph_top_right=(width, 0),
            enable_events=True,
            drag_submits=True,
            key="graph"
        ), sg.Image(key='selected'), sg.Image(key='-PROCCESSED-')],
        [sg.Text('Start Position: (---,---)\nEnd Position:   (---,---)', key='-CURSOR_POS-', font='Courier 10'),
        sg.Button('Find Value')
    ]
]


window = sg.Window("GUI Graph Test", layout, finalize=True)

graph = window["graph"] # type: sg.Graph
image = graph.draw_image(data=encoded, location=(0, 0))

dragging = False
startpoint = None
endpoint = None
rectangle = None
cropped = None
v_max_slider = 255
x1 = x2 = y1 = y2 = None

while True:

    img = cv2.imread(file_values[0]) # type: np.ndarray
    encoded = cv2.imencode('.png', img)[1].tobytes() 
    image = graph.draw_image(data=encoded, location=(0, 0))
    graph.delete_figure(image)

    event, values = window.Read()

    if event == '-VALSlider-':
        
        v_max_slider = int(values['-VALSlider-'])
        cropped = img[y1:y2 , x1:x2]
        cropped_encoded = cv2.imencode('.png', cropped)[1].tobytes()
        # window['selected'].update(data=cropped_encoded)

        cropped_dim = (x2-x1, y2-y1)
        proccessed = ImageProcess.process(cropped, v_max=v_max_slider, dim=cropped_dim)
        processed_encoded = cv2.imencode('.png', proccessed)[1].tobytes()
        window['-PROCCESSED-'].update(data=processed_encoded)

    
    print('Val: ' + str(v_max_slider))

    if event == 'graph':

        cursor_pos = values['graph']
        cursor_text = ('Start Position: ' + str(startpoint) +
                        '\nEnd Position:   ' + str(cursor_pos))



        if not dragging:
            graph.delete_figure(rectangle)
            dragging = True
            startpoint = cursor_pos
            endpoint = cursor_pos
            rectangle = graph.draw_rectangle(startpoint, endpoint, line_color="white", line_width=4, fill_color='blue')
        else:
            endpoint = cursor_pos
            graph.delete_figure(rectangle)
            rectangle = graph.draw_rectangle(startpoint, endpoint, line_color="white", line_width=4, fill_color='blue')
            
            if (startpoint[0] != endpoint[0]) and (startpoint[1] != endpoint[1]):
                print(bool(startpoint == endpoint))
                x1, x2, y1, y2 = startpoint[0], endpoint[0], startpoint[1], endpoint[1]

                if x2 < 0:
                    x2 = 0
                    print("X Less")
                if y2 < 0:
                    print("Y Less")
                    y2 = 0

                if x2 < x1:
                    x1, x2 = x2, x1
                
                if y2 < y1:
                    y1, y2 = y2, y1

                cropped = img[y1:y2 , x1:x2]
                cropped_encoded = cv2.imencode('.png', cropped)[1].tobytes()
                # window['selected'].update(data=cropped_encoded)

                cropped_dim = (x2-x1, y2-y1)
                proccessed = ImageProcess.process(cropped, v_max=v_max_slider, dim=cropped_dim)
                processed_encoded = cv2.imencode('.png', proccessed)[1].tobytes()
                window['-PROCCESSED-'].update(data=processed_encoded)

        # print('Cursor Position: cursor_pos)
        # print('Start Point: ', startpoint)
        # print('End Point: ', endpoint)

        window['-CURSOR_POS-'].update(cursor_text)

    elif event.endswith('+UP'):

        dragging = False
        startpoint = None
        endpoint = None
    elif event == 'Find Value':

        if cropped.any():
            
            guess = match.getDigit(ImageProcess.process(cropped, v_max=v_max_slider))
            if guess > -1:
                sg.popup(('Found ' + str(guess))) 

    if event is None:
        break