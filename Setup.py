import PySimpleGUI as sg
import cv2
import Feed

def setup(feed: Feed):
    setup_col = [[sg.Graph((400,400), (0,400), (400,0))]]
    setup_layout = [[sg.Column(setup_col)], [sg.Button('Confirm'), sg.Button('Quit')]]

    setup_window = sg.Window('Setup', setup_layout)

    while True:
        event, values = setup_window.read()
        
        if event == None or event == 'Quit':
            exit()
        elif event == 'Confirm':
            return feed