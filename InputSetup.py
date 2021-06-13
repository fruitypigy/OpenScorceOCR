from tkinter.constants import DISABLED
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import HorizontalSeparator
from Feed import Feed


def inputSetup():
    sg.Spin(('None', '2'))

    # TODO Fix crash on close with out selecting image
    browse_element = sg.Column([[sg.Text('Image Input')],
                                [sg.FileBrowse(target='input', file_types=(('jpg', '.jpg'), ('png', '.png'), ('mp4', 'mp4')))]])

    camera_select_element = sg.Column(([[sg.Text('Camera Input')],
                                        [sg.Spin((0, 1, 2, 3), 'None', size=(6, 1), key='cam_select',
                                                 enable_events=True)]]))

    preview_element = sg.Image(background_color='grey', size=(400, 400), key='preview')

    selected_element = sg.Input(key='input', size=(20, 1), readonly=True, enable_events=True)

    window = sg.Window('Setup', [[preview_element], [browse_element, camera_select_element], [HorizontalSeparator()],
                                 [selected_element, sg.OK(disabled=True, key='OK'), sg.Quit()]])

    feed = None

    while True:
        event, values = window.read(50)

        if event == None or event == 'Quit':
            exit()
        elif event == 'input' and values['input']:
            window['OK'].update(disabled=False)
            feed = Feed(values['input'])
        elif event == 'cam_select':
            if values['cam_select'] != 'None':
                window['OK'].update(disabled=False)
                window['input'].update(values['cam_select'])
                feed = Feed(values['cam_select'])
        elif event == 'OK':
            window.close()
            feed = Feed(feed.feed_input)
            return feed
        elif feed:
            window['preview'].update(data=feed.get_frame(True)[1])


if __name__ == '__main__':
    inputSetup()
