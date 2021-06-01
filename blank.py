import cv2
import PySimpleGUI as sg
from SelectedViewer import SelectedViewer as sv
from SelectedArea import SelectedArea as sa

graph_element = sg.Graph((750, 750), (0, 750), (750, 0), 
                key='graph', enable_events=True, background_color='white')

layout = [[graph_element]]

window = sg.Window('Selected Viewer Test', layout, finalize=True)

frame = cv2.imread('PreviewTest.png')

viewer = sv()

graph = window['graph'] # type: sg.Graph

while True:
    event, values = window.read()

    graph = viewer.drawSelected(graph, (6,6), 32)

    if event == None:
        exit()

