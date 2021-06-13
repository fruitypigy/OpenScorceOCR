from statistics import mean

import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa
from SelectedViewer import SelectedViewer as sv
from InputSetup import inputSetup
from FilterSetup import filterSetup
from AreaDict import AreaDict
import time
from xml.dom.minidom import parseString


def main():
    # sg.theme('DarkTeal6')
    # sg.theme('SystemDefault1')
    # sg.theme('DarkTanBlue')
    sg.theme('Dark2')

    feed = inputSetup()
    # TODO Remove all references to area_number
    # TODO Combine all area lists into area_dict
    feed, area_number = filterSetup(feed)
    feed.resize_for_crop = True
    feed.get_frame()

    default_unrecognized = 0

    area_dict = AreaDict(area_number)
    for key in area_dict().keys():
        area_dict()[key].processArea(feed.get_frame()[0])

    viewer = sv()

    graph_right_click = [[''], ['Add Digit', 'Remove Last']]

    graph_element = sg.Graph((feed.crop_width, feed.crop_height), (0, feed.crop_height), (feed.crop_width, 0),
                             pad=(10, 10), enable_events=True, key='graph', drag_submits=True, background_color='black',
                             right_click_menu=graph_right_click)

    performance_element = sg.Text(size=(30, 5), key='performance_monitor')

    viewer_graph_element = sg.Graph((480, 390), (0, 390), (480, 0), pad=(10, 10),
                                    enable_events=True, key='viewer', drag_submits=True, background_color='grey')
    selector_element = sg.Listbox(list(area_dict().keys()), size=(15, 12), default_values=['Digit1'],
                                  enable_events=True, key='area_selector')
    text_element = sg.Text('1, 2, 3, 4, 5, 6, 7, 8, 9, 10', (60, 2),
                           key='digits', text_color='White', background_color='grey')

    selector_col = [[selector_element], [sg.Input(size=(15, 8), key='area_name', enable_events=True)],
                    [sg.Image(key='cropped')]]

    layout = [[sg.Column(selector_col, vertical_alignment='top'), sg.Column([[performance_element], [graph_element]]),
               viewer_graph_element], [text_element, sg.Button('Quit')]]

    window = sg.Window('OpenScorce', layout, return_keyboard_events=True, finalize=True)
    graph = window['graph']  # type: sg.Graph
    area_selector = window['area_selector']  # type: sg.Listbox
    viewer_graph = window['viewer']  # type: sg.Graph

    graph_focused = False

    def draw_all():

        for key in area_dict().keys():
            next_area = area_dict()[key]
            if key == selected_key and graph_focused:
                next_area.adjustRectangle(graph, event, values, True)
            elif key == selected_key and not graph_focused:
                next_area.adjustRectangle(graph, is_main=True)
            else:
                next_area.adjustRectangle(graph)

    def get_digits():
        digit_list = []
        for key in area_dict().keys():
            digit_list.append(area_dict()[key].getDigit()[0])
        return digit_list

    viewer.draw_selected(viewer_graph, area_dict)

    cycles = 0

    last_key = list(area_dict().keys())[0]

    wait = 1
    wait_list = []
    perf_text = ''

    while True:

        event, values = window.read(timeout=wait)
        start = time.time()

        if area_selector.get():
            selected_key = last_key = area_selector.get()[0]
        else:
            selected_key = last_key
        input_name = values['area_name']
        if event is None or event == 'Quit':
            break
        elif event == 'area_name':
            graph_focused = False
        elif event == 'area_selector':
            graph_focused = True
            window['area_name'].update(selected_key)
        elif area_selector.get() and event == '\r' and input_name not in area_dict().keys():
            selected_key = last_key = area_dict.rename(selected_key, input_name)
            area_selector.update(list(area_dict().keys()))
            graph_focused = True
            graph.set_focus()
        elif event == 'Add Digit' or (graph_focused and event == 'r'):
            selected_key = last_key = area_dict.add()
            area_dict()[selected_key].processArea(feed.get_frame()[0])
            area_selector.update(list(area_dict().keys()))

        # elif (event == 'Remove Last' or (graph_focused and event == 'R')) and len(area_dict.area_dict) > 1:
        #     area_dict.remove(area_dict.name_list[-1])
        #     area_selector.update(area_dict.name_list)
        #     area_dict.selected = len(area_dict.area_dict) - 1

        elif event == 'graph':
            graph_focused = True
            graph.set_focus()
            encoded, guessed = area_dict()[selected_key].processArea(feed.get_frame()[0], skip_digit=True)
            # print(guessed)
            window['cropped'].update(data=encoded)
            cycles = 1
        elif cycles <= len(area_dict()):
            list(area_dict().values())[cycles - 1].processArea(feed.get_frame()[0])
            cycles += 1
        else:
            cycles = 1

        # viewer.draw_selected(viewer_graph, area_dict)
        window['cropped'].update(data=area_dict()[selected_key].getPreview())  # --------
        window['digits'].update(get_digits())
        feed.draw_frame(graph, True)
        area_dict.update_xml('first_real_test.xml', default_unrecognized)
        draw_all()

        wait = 33 - ((time.time() - start) * 1000)
        wait_list.append(wait)
        if len(wait_list) >= 15:
            if mean(wait_list) > 0:
                perf_text = f'Ahead by {round(mean(wait_list), 3)}ms'
            else:
                perf_text = f'Behind by {round((mean(wait_list)*-1), 3)}ms, skipping wait'
                wait = 1
        window['performance_monitor'].update(perf_text)


if __name__ == '__main__':
    main()
