import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa

def link_setup(area_list: list[str]):
    link_setup_layout = [
        [sg.Listbox(area_list, size=(15, 12), default_values=([area_list[0]]), key='list'),
         sg.Column([
             [sg.Button('Add Area'), sg.Button('Add Custom')],
             [sg.Button('Back'), sg.Button('Clear')],
             [sg.Text('Custom: '), sg.Input(':', size=(16, 1), key='custom')]
         ], vertical_alignment='t')
         ],
        [sg.Text('Link Name'), sg.Input(size=(32, 1), key='link_name')],
        [sg.Text('Preview: '), sg.Input(size=(32, 1), readonly=True, key='preview')],
        [sg.Save(disabled=True), sg.Cancel()]
    ]

    link_setup_window = sg.Window('Create Link', link_setup_layout)

    linked_list = []  # type: list[str]

    while True:
        event, values = link_setup_window.read()
        area_selector_value = values['list']
        print(area_selector_value)
        if event is None or event == 'Cancel':
            linked_list.clear()
            break
        elif event == 'Save':
            break
        elif event == 'Add Area':
            linked_list.append(area_selector_value[0])
        elif event == 'Add Custom':
            linked_list.append(values['custom'])
        elif event == 'Back' and linked_list:
            print(values['list'])
            linked_list.pop()
        elif event == 'Clear':
            linked_list.clear()

        link_setup_window['Save'].update(disabled=not bool(linked_list))
        link_setup_window['preview'].update(linked_list)

    return linked_list, values['link_name']


if __name__ == '__main__':
    areas = ['Area 1', 'Area 2', 'Area 3', 'Area 4']
    print(link_setup(areas))
