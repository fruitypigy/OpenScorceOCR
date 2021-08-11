from statistics import mean
import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa
from SelectedViewer import SelectedViewer as sv
from InputSetup import inputSetup
from FilterSetup import filterSetup
from AreaDict import AreaDict
from LinkSetup import link_setup
import time

def main():
    # sg.theme('DarkTeal6')
    # sg.theme('SystemDefault1')
    # sg.theme('DarkTanBlue')
    sg.theme('Dark2')

    feed, filepath = inputSetup()
    # TODO Remove all references to area_number
    # TODO Combine all   lists into area_dict
    feed, area_number = filterSetup(feed)
    # feed.resize_for_crop = True
    feed.get_frame()

    default_unrecognized = 0

    area_dict = AreaDict(area_number)
    for key in area_dict().keys():
        area_dict()[key].process_area(feed.get_frame()[0])

    viewer = sv()

    graph_right_click = [[''], ['Add Digit', 'Add Linked', 'Remove Last', 'Edit Values']]

    print(feed.width, feed.height)

    graph_element = sg.Graph((feed.width, feed.height), (0, feed.height), (feed.width, 0),
                             pad=(10, 10), enable_events=True, key='graph', drag_submits=True, background_color='black',
                             right_click_menu=graph_right_click)

    performance_element = sg.Text(size=(30, 5), key='performance_monitor')

    viewer_graph_element = sg.Graph((480, 390), (0, 390), (480, 0), pad=(10, 10),
                                    enable_events=True, key='viewer', drag_submits=True, background_color='grey')
    selector_element = sg.Listbox(list(area_dict().keys()), size=(15, 12), default_values=['Digit1'],
                                  enable_events=True, key='area_selector')
    text_element = sg.Text('1, 2, 3, 4, 5, 6, 7, 8, 9, 10', (60, 2),
                           key='digits', text_color='White', background_color='grey')

    selector_col = [
        [selector_element],
        [sg.Input(size=(15, 8), key='area_name', enable_events=True)],
        [sg.Image(key='cropped')]
    ]

    main_layout = [
        [
            sg.Column(selector_col, vertical_alignment='top'),
            sg.Column([[performance_element], [graph_element]]),
            sg.Column([
                [viewer_graph_element],
                [sg.Check('Enable Viewer', key='viewer_enable')]
            ])],
        [text_element, sg.Button('Quit')
         ]
    ]

    # TODO: remove
    editor_layout = [[sg.Image(None, size=(240, 400), background_color='Black', key='raw_digit'),
                      sg.Image(None, size=(240, 400), background_color='Blue', key='processed_digit'),
                      sg.Column([
                          [
                              sg.Text('Name'), sg.Input('Default', size=(20, 2))
                          ],
                          [
                              sg.Column([
                                  [sg.Text('\nMax')],
                                  [sg.Text('Min')]
                              ]),
                              sg.Column([
                                  [sg.Text('Hue     Sat       Val')],
                                  [sg.Spin(list(range(0, 255)), size=(3, 2), key='hue_max'),
                                   sg.Spin(list(range(0, 255)), size=(3, 2), key='hue_min'),
                                   sg.Spin(list(range(0, 255)), size=(3, 2), key='sat_max')],
                                  [sg.Spin(list(range(0, 255)), size=(3, 2), key='sat_min'),
                                   sg.Spin(list(range(0, 255)), size=(3, 2), key='val_max'),
                                   sg.Spin(list(range(0, 255)), size=(3, 2), key='val_min')],
                              ])
                          ],
                          [
                              sg.Checkbox('Show Overlay', key='show_overlay')
                          ],
                          [
                              sg.Save(), sg.Cancel()
                          ]
                      ])
                      ]]

    main_window = sg.Window('OpenScorce', main_layout, return_keyboard_events=True, finalize=True)
    editor_window = sg.Window('Editor', editor_layout)  # maybe finalize = True????? idk wtf it does lol

    graph = main_window['graph']  # type: sg.Graph
    area_selector = main_window['area_selector']  # type: sg.Listbox
    viewer_graph = main_window['viewer']  # type: sg.Graph

    graph_focused = False

    def edit_area(selected: sa):
        pass

    def draw_all():

        for key in area_dict().keys():
            next_area = area_dict()[key]
            if key == selected_key and graph_focused:
                next_area.adjust_rectangle(graph, event, values, True)
            elif key == selected_key and not graph_focused:
                next_area.adjust_rectangle(graph, is_main=True)
            else:
                next_area.adjust_rectangle(graph)

    def get_digits():
        digit_list = []
        for key in area_dict().keys():
            digit_list.append(area_dict()[key].get_digit()[0])
        return digit_list

    viewer.draw_selected(viewer_graph, area_dict)

    cycles = 0

    last_key = list(area_dict().keys())[0]

    wait = 1
    wait_list = []
    perf_text = ''

    start = 0
    frames = 0
    fps = 0

    while True:

        event, values = main_window.read(timeout=1)
        # start = time.time()

        if area_selector.get():
            selected_key = last_key = area_selector.get()[0]
        else:
            selected_key = last_key
        input_name = values['area_name']
        if event is None or event == 'Quit':
            exit(0)
        elif event == 'area_name':
            graph_focused = False
        elif event == 'area_selector':
            graph_focused = True
            main_window['area_name'].update(selected_key)
        elif area_selector.get() and event == '\r' and input_name not in area_dict().keys():
            selected_key = last_key = area_dict.rename(selected_key, input_name)
            area_selector.update(list(area_dict().keys()))
            graph_focused = True
            graph.set_focus()
        elif event == 'Add Digit' or (graph_focused and event == 'r'):
            selected_key = last_key = area_dict.add()
            area_dict()[selected_key].process_area(feed.get_frame()[0])
            area_selector.update(list(area_dict().keys()))
        elif event == 'Add Linked' or (graph_focused and event == 'r'):
            new_link, new_link_name = link_setup(list(area_dict().keys()))
            if new_link:
                area_dict.add_linked(new_link, new_link_name)
        elif (event == 'Remove Last' or (graph_focused and event == 'R')) and len(area_dict.area_dict) > 1:
            area_dict.remove(list(area_dict().keys())[-1])
            area_selector.update(list(area_dict().keys()))
            area_dict.selected = len(area_dict.area_dict) - 1
            selected_key = last_key = list(area_dict().keys())[-1]

        elif event == 'Edit Values':
            pass

        elif event == 'graph':
            graph_focused = True
            graph.set_focus()
            encoded, guessed = area_dict()[selected_key].process_area(feed.get_frame()[0], skip_digit=True)
            # print(guessed)
            main_window['cropped'].update(data=encoded)
            cycles = 1
        elif cycles <= len(area_dict()):
            list(area_dict().values())[cycles - 1].process_area(feed.get_frame()[0])
            cycles += 1
        else:
            cycles = 1

        if values['viewer_enable']:
            viewer.draw_selected(viewer_graph, area_dict)

        main_window['cropped'].update(data=area_dict()[selected_key].get_preview())  # --------
        main_window['digits'].update(get_digits())
        feed.draw_frame(graph, True)
        area_dict.update_xml(filepath, default_unrecognized)
        draw_all()

        wait = (time.time() - start) * 1000
        wait_list.append(wait)
        if len(wait_list) >= 15:
            perf_text = f'{round(mean(wait_list), 3)}ms/frame'
            wait_list.clear()

        main_window['performance_monitor'].update(perf_text)

        if wait <= 33:
            wait = 33 - wait
        else:
            wait = 0
        start = time.time()


if __name__ == '__main__':
    main()
