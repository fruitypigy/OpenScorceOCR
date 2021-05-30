import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import numpy as np
import cv2

img = cv2.imread('Tests\RawTest.jpg')
encoded = cv2.imencode('.png', img)[1].tobytes()
height, width, channels = img.shape

graph_element = sg.Graph(
            canvas_size=(width, height),
            graph_bottom_left=(0, 0),
            graph_top_right=(width, height),
            key="graph"
        )



print(height, width, channels)

# define the window layout
layout = [[sg.Text('Cursor Test', size=(10, 1), justification='center', font='Helvetica 20')],
            [sg.Image(filename='', key='image'), graph_element],
            [sg.Text('Cursor Position: ', key='-CURSOR-')]]

# create the window and show it without the plot
window = sg.Window('Demo Application - OpenCV Integration',
                    layout)

window.Finalize()

graph = window.Element("graph")
graph.DrawImage(data=encoded, location=(0, height))

while True:
    event, values = window.read(timeout=20)
    if event == WIN_CLOSED:
        break
    window['image'].update(data=encoded)