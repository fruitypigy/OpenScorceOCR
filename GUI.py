import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa
from SelectedViewer import SelectedViewer as sv
from InputSetup import inputSetup
from FilterSetup import filterSetup
import time


def main():
    # sg.theme('DarkTeal6')
    # sg.theme('SystemDefault1')
    # sg.theme('DarkTanBlue')
    sg.theme('Dark2')

    feed = inputSetup()
    feed, area_number = filterSetup(feed)
    feed.resize_for_crop = True
    feed.get_frame()

    area_list = []  # type: list[sa]
    area_combo_list = []  # type: list[str]

    area_selected = 0

    viewer = sv()

    for combo_count in range(0, area_number):
        area_combo_list.append(str('Digit ' + str(combo_count + 1)))

    graph_right_click = [[''], ['Add Digit', 'Remove Last']]

    graph_element = sg.Graph((feed.crop_width, feed.crop_height), (0, feed.crop_height), (feed.crop_width, 0),
                             pad=(10, 10), enable_events=True, key='graph', drag_submits=True, background_color='black',
                             right_click_menu=graph_right_click)
    viewer_graph_element = sg.Graph((480, 390), (0, 390), (480, 0), pad=(10, 10),
                                    enable_events=True, key='viewer', drag_submits=True, background_color='grey')
    selector_element = sg.Listbox(values=area_combo_list, size=(15, 12),
                                  default_values=['Area 0'], enable_events=True, key='area_selector')
    text_element = sg.Text('1, 2, 3, 4, 5, 6, 7, 8, 9, 10', (60, 2),
                           key='digits', text_color='White', background_color='grey')

    selector_col = [[selector_element], [sg.Input(area_combo_list[0], (15, 8), key='area_name', enable_events=True)],
                    [sg.Image(key='cropped')]]

    layout = [[sg.Column(selector_col, vertical_alignment='top'), graph_element, viewer_graph_element],
              [text_element, sg.Button('Quit')]]

    window = sg.Window('OpenScorce', layout, return_keyboard_events=True, finalize=True)
    graph = window['graph']  # type: sg.Graph
    area_selector = window['area_selector']  # type: sg.Listbox
    viewer_graph = window['viewer']  # type: sg.Graph

    ignore_keys = True

    for x in range(0, area_number):
        area_list.append(sa(graph.draw_rectangle((-1, -1), (-1, -1))))
        graph = area_list[x].adjustRectangle(graph)

    def draw_all(event, values):

        for count in range(0, area_number):
            if count == area_selected and not ignore_keys:
                area_list[count].adjustRectangle(graph, event, values, True)
            elif count == area_selected and ignore_keys:
                area_list[count].adjustRectangle(graph, is_main=True)
            elif area_list[count].initiated:
                area_list[count].adjustRectangle(graph)

    def get_digits(areas: list[sa]):
        digits = []  # type: list[int]
        for count in range(len(areas)):
            digits.append(areas[count].getDigit())
        return digits

    for x in range(len(area_list)):
        area_list[x].processArea(feed.get_frame()[0])

    viewer_graph = viewer.draw_selected(viewer_graph, area_list, (3, 6), area_number)

    cycles = 0

    # window['area_name'].block_focus=True

    while True:

        event, values = window.read(timeout=1)

        if event is None or event == 'Quit':
            break
        elif event == 'area_name':
            ignore_keys = True
        elif event == 'area_selector':
            ignore_keys = True
            area_selected = area_selector.get_indexes()[0]
            window['area_name'].update(area_combo_list[area_selector.get_indexes()[0]])
        elif area_selector.get_indexes() and event == '\r' and values['area_name'] not in area_combo_list:
            area_combo_list[area_selector.get_indexes()[0]] = values['area_name']
            area_selector.update(area_combo_list)
        elif event == 'Add Digit' or event == 'r':
            x = len(area_combo_list)
            while f'Digit {x}' in area_combo_list:
                x += 1
            area_combo_list.append(f'Digit {x}')
            area_selector.update(area_combo_list)
            last_area = area_list[-1]
            area_list.append(sa(last_area.rectangle, last_area.pos, (last_area.length, last_area.height)))
            area_list[-1].processArea(feed.get_frame()[0])
            area_selected = len(area_list) - 1
            area_number += 1

        elif (event == 'Remove Last' or event == 'R') and len(area_list) > 1:
            del area_combo_list[-1]
            del area_list[-1]
            area_selected = len(area_list) - 1
            area_number -= 1
            area_selector.update(area_combo_list)

        elif event == 'graph':
            ignore_keys = False
            graph.set_focus()
            encoded, guessed = area_list[area_selected].processArea(feed.get_frame()[0], skip_digit=True)
            window['cropped'].update(data=encoded)
            cycles = 1
        elif cycles <= len(area_list):
            area_list[cycles - 1].processArea(feed.get_frame()[0])
            cycles += 1
        else:
            cycles = 1
        viewer_graph = viewer.draw_selected(viewer_graph, area_list, (3, 6), area_number)
        window['cropped'].update(data=area_list[area_selected].getPreview())
        window['digits'].update((get_digits(area_list)))
        graph = feed.draw_frame(graph, True)
        draw_all(event, values)


if __name__ == '__main__':
    main()
