import numpy as np
import cv2
import PySimpleGUI as sg
import time

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
    heigth = int(values['height'])
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
        start = time.time()
        frames = cycles = 0
        while True:
        
            pts1 = np.float32(points)
            pts2 = np.float32([[0,0], [width, 0], [0,heigth], [width, heigth]])
            
            matrix = cv2.getPerspectiveTransform(pts1, pts2)

            transformed = cv2.warpPerspective(img, matrix, (width, heigth))
            # print('Hello World')

            transformed_encoded = cv2.imencode('.png', transformed)[1].tobytes()
            window['output'].update(data=transformed_encoded, size=(width, heigth))


            window.read(timeout=0.1)
            if frames >= 100:
                print(f'Processing at {100/(time.time()-start)} fps')
                frames = 0
                start = time.time()
                cycles += 1
            elif cycles >= 2:
                break        
            else:
                frames += 1
