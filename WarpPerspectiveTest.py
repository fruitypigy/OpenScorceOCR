import numpy as np
import cv2
import PySimpleGUI as sg
import time
from ImageProcess import warpPerspective

layout = [[sg.Graph((600,600), (0,600), (600,0), enable_events=True, background_color='black', key='graph'), sg.Image(background_color='grey', size=(480,480), key='output')], 
        [sg.Button('Reset'), sg.Button('Warp'), sg.Text('Width:'), sg.Input(100, key='width', size=(5, 4)), sg.Text('Height:'), sg.Input(100, key='height', size=(5,4))],
        [sg.Text(size=(100, 4), key='points_text')]]

window = sg.Window('WarpPerspectiveTest', layout)

img = cv2.imread('TestInputs\RealTwoCropped.png')

img_encoded = cv2.imencode('.png', img)[1].tobytes()

graph = window['graph'] # type: sg.Graph

window.read(timeout=1)
graph.draw_image(data=img_encoded, location=(0,0))

points = [] # type: list[list]

while True:
    event, values = window.read()
    graph.erase()
    graph.draw_image(data=img_encoded, location=(0,0))
    pos = list(values['graph'])
    width = int(values['width'])
    height = int(values['height'])
    print(event, values)
    print(pos)
    if event == None:
        break
    elif event == 'graph':
        graph.draw_circle(values['graph'] ,radius=2, fill_color='red')
        if len(points) < 4:
            points.append(pos)
            window['points_text'].update(points)
            print(points)
        else:
            points = []
            points.append(pos)
            window['points_text'].update(points)
    elif event == 'Reset':
        points = []
        window['points_text'].update(points)
    elif event == 'Warp' and len(points) == 4:
        encoded = warpPerspective(img, points, (width, height))
        window['output'].update(data=encoded[1])
        