import PySimpleGUI as sg
import cv2
import numpy as np
import ImageProcess
import OpenCVMatch
import time

"""
Demo program that displays a webcam using OpenCV
"""


def main():

    hmin = 0
    hmax = 255
    cropval = 100


    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Text('Test', key='-Text-'), ]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout)

    layout2 = [ [sg.Txt('Enter values')],
                [sg.Txt('Hue Max')],
                [sg.In(255, size=(8,1), key='-HUEMAX-')],
                [sg.Txt('Hue Min')],
                [sg.In(0, size=(8,1), key='-HUEMIN-')],
                [sg.Txt('Crop')],
                [sg.In(100, size=(8,1), key='-CROP-')  ],
                [sg.Txt('Output')],
                [sg.Txt(size=(8,1), key='-OUTPUT-')  ],
                [sg.Button('Update')],
                [sg.Image(filename='', key='proccessed')]]

    otherwindow = sg.Window('Inputs', 
                        layout2)

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = True

    frames = 0

    start = time.time()

    while True:
        

        event1, values1 = window.read(timeout=20)
        event2, values2 = otherwindow.read(timeout=20)

        if event2 == 'Update':
            hmin = int(values2['-HUEMIN-'])
            hmax = int(values2['-HUEMAX-'])
            cropval = int(values2['-CROP-'])
        
        ret, frame = cap.read()
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    

        window['image'].update(data=imgbytes)

        processed = ImageProcess.process(frame, h_min=hmin, h_max=hmax, s_max=255, v_max=163, scale=cropval, angle=0)
        processedimgbytes = cv2.imencode('.png', processed)[1].tobytes()  # ditto
        otherwindow['proccessed'].update(data=processedimgbytes)
    
        guessed = OpenCVMatch.getDigit(processed)
        otherwindow['-OUTPUT-'].update('Guessed: ' + str(guessed))

        frames += 1
        if time.time() - start >= 1:
            fps = frames / start
            window['-Text-'].update(frames)
            start = time.time()
            frames = 0


main()