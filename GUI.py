import PySimpleGUI as sg
from SelectedArea import SelectedArea as sa 
from SelectedViewer import SelectedViewer as sv
from InputSetup import inputSetup
from FilterSetup import filterSetup

def main():
    # sg.theme('DarkTeal6')
    # sg.theme('SystemDefault1')
    # sg.theme('DarkTanBlue')
    sg.theme('Dark2')
    
    feed = inputSetup()
    feed, area_number = filterSetup(feed) 
    feed.resize_for_crop = True
    feed.getFrame()

    area_list = [] # type: list[sa]
    area_combo_list = []

    area_selected = 0

    viewer = sv()

    for combo_count in range(0, area_number):
        area_combo_list.append(str('Segment ' + str(combo_count+1))) 

    graph_element = sg.Graph((feed.crop_width, feed.crop_height), (0, feed.crop_height), (feed.crop_width, 0), pad=(10,10), 
                        enable_events=True, key='graph', drag_submits=True, background_color='black')
    viewer_graph_element = sg.Graph((480, 390), (0, 390), (480, 0), pad=(10,10), 
                        enable_events=True, key='viewer', drag_submits=True, background_color='grey')
    selector_element = sg.Listbox(values=area_combo_list, size=(15, 12), 
                        default_values = 'Area 0', enable_events=True, key='area_selector' )
    text_element = sg.Text('1, 2, 3, 4, 5, 6, 7, 8, 9, 10', (60, 2), 
                        key='digits', text_color='White', background_color='grey')

    selector_col = [[selector_element], [sg.Input(area_combo_list[0], (15, 8), key='area_name', enable_events=True)], [sg.Image(key='cropped')]]

    layout = [[sg.Column(selector_col, vertical_alignment='top'), graph_element, viewer_graph_element], [text_element, sg.Button('Quit')]]

    window = sg.Window('OpenScorce', layout, return_keyboard_events=True, finalize=True)
    graph = window['graph'] # type: sg.Graph
    area_selector = window['area_selector'] # type: sg.Listbox
    viewer_graph = window['viewer'] # type: sg.Graph
    
    ignore_keys = True

    for x in range(0, area_number):
        area_list.append(sa(graph.draw_rectangle((-1,-1), (-1,-1))))
        graph = area_list[x].adjustRectangle(graph)    

    def drawAll(event, values):

        for count in range(0, area_number):
            if count == area_selected and not ignore_keys:
                area_list[count].adjustRectangle(graph, event, values, True)
            elif count == area_selected and ignore_keys:
                area_list[count].adjustRectangle(graph, is_main=True)
            elif area_list[count].initiated:
                area_list[count].adjustRectangle(graph)

    def getDigits(areas: list[sa]):
        digits = [] # type: list[int]
        for count in range(len(areas)):
            digits.append(areas[count].getDigit())
        return digits

    for x in range(len(area_list)):
        area_list[x].processArea(feed.getFrame()[0])


    viewer_graph = viewer.drawSelected(viewer_graph, area_list, (3,6), area_number)

    cycles = 0

    # window['area_name'].block_focus=True
    
    while True:
        
        event, values = window.read(timeout=0.1)

        if event == None or event == 'Quit':
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
        # TODO Allow right click to add segment
        elif event == 'graph':
            ignore_keys = False
            graph.set_focus()
            encoded, guessed = area_list[area_selected].processArea(feed.getFrame()[0], skip_digit=True)
            window['cropped'].update(data=encoded)
            cycles = 1
        elif cycles <= len(area_list):    
            area_list[cycles-1].processArea(feed.getFrame()[0])
            cycles += 1
        else:
            cycles = 1
        viewer_graph = viewer.drawSelected(viewer_graph, area_list, (3,6), area_number)
        window['cropped'].update(data=area_list[area_selected].getPreview())
        window['digits'].update((getDigits(area_list)))
        graph = feed.drawFrame(graph, True)
        drawAll(event, values)

if __name__ == '__main__':
    main()