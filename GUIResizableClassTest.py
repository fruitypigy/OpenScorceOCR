import SelectedArea
import PySimpleGUI as sg

graph_element = sg.Graph((400, 400), (0, 400), (400, 0), enable_events=True, key='graph',drag_submits=True)

layout = [[graph_element]]

window = sg.Window('Resizeable Rectangle Test', layout, return_keyboard_events=True, finalize=True)

graph = window['graph'] # type: sg.Graph

area = SelectedArea.adjustRectangle()

while True:
    event, values = window.read()
    if event == 'graph':
        pass # area.update(event, values)