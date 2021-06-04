from tkinter.constants import DISABLED
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import HorizontalSeparator
import cv2
from Feed import Feed

def inputSetup():
    sg.Spin(('None', '2'))
    browse_element = sg.Column([[sg.Text('Image Input')], 
                                [sg.FileBrowse(target='input', file_types=(('JPG', '.jpg'), ('PNG', '.png')))]])

    camera_select_element = sg.Column(([sg.Text('Camera Input')], 
                            [sg.Spin((0, 1, 2, 3), 'None', size=(6, 1), key='cam_select', enable_events=True)]))

    preview_element = sg.Image('square.png', key='preview')

    selected_element = sg.Input(key='input', size=(20, 1), readonly=True, enable_events=True)

    window = sg.Window('Test', [[preview_element], [browse_element, camera_select_element], [HorizontalSeparator()], [selected_element, sg.OK(disabled=True, key='OK'), sg.Quit()]])

    feed = None

    while True:
        event, values = window.read(timeout=1)
        
        if event == None or event == 'Quit':
            exit()
        elif event == 'input':
            window['OK'].update(disabled=False)
            feed = Feed(values['input'])
        elif event == 'cam_select':
            if values['cam_select'] != 'None':
                window['OK'].update(disabled=False)
                window['input'].update(values['cam_select'])
                feed = Feed(values['cam_select'])
        elif event == 'OK':
            return feed
        elif feed:
            window['preview'].update(data=feed.getFrame(True)[1])
        
inputSetup()
print('Fin')