from sys import version
from numpy import heaviside
from ImageProcess import hsvProcess, resize
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Window
import cv2
from Feed import Feed

def filterSetup(feed: Feed):

    slider_elements = [sg.Text('Hue Min', size=(7,1)), sg.Slider((0, 255), 0, orientation='vertical', key='HUE_MN', enable_events=True),
                    sg.Text('Hue Max', size=(7,1)), sg.Slider((0, 255), 255, orientation='vertical', key='HUE_MX', enable_events=True)],[
                    sg.Text('Sat Min', size=(7,1)), sg.Slider((0, 255), 0, orientation='vertical', key='SAT_MN', enable_events=True),
                    sg.Text('Sat Max', size=(7,1)), sg.Slider((0, 255), 255, orientation='vertical', key='SAT_MX', enable_events=True)],[
                    sg.Text('Val Min', size=(7,1)), sg.Slider((0, 255), 0, orientation='vertical', key='VAL_MN', enable_events=True),
                    sg.Text('Val Max', size=(7,1)), sg.Slider((0, 255), 255, orientation='vertical', key='VAL_MX', enable_events=True)],[
                    sg.Text('Rotation'), sg.Slider((0,360), 0, orientation='horizontal', key='ROT')],[
                        sg.Checkbox('Apply HSV Filter', key='apply_hsv')]

    input_graph_element = sg.Graph(canvas_size=(feed.width, feed.height), graph_bottom_left=(0, feed.height), 
                                graph_top_right=(feed.width, 0), enable_events=True, drag_submits=True,
                                key="graph", background_color='green')
    
    preview_element = [sg.Text('Preview')], [sg.Graph((400, 300), (0, 300), (400, 0), background_color='green', key='preview')]

    setup_layout = [[input_graph_element, sg.Column(slider_elements), sg.Column(preview_element)], [sg.Button('Confirm'), sg.Button('Quit')]]

    setup_window = sg.Window('Setup', setup_layout)

    graph = setup_window['graph'] # type: sg.Graph
    preview = setup_window['preview'] # type: sg.Graph

    cycles = 0

    hsv_vals = (0, 255, 0, 255, 0, 255)
    
    dragging = False

    dims = (feed.width, feed.height)
    startpoint = endpoint = (-1,-1)
    crop_vals = getCrop((1,1),(dims[0], dims[1]),dims)

    while True:
        event, values = setup_window.read(timeout=0.01)
        
        hsv_vals = (values['HUE_MN'], values['HUE_MX'], 
                    values['SAT_MN'], values['SAT_MX'], 
                    values['VAL_MN'], values['VAL_MX'],)
        rot = values['ROT']
        feed.configRotHSV(rot)
        graph = feed.drawFrame(graph, True)
        apply_hsv = values['apply_hsv']
        if event == None or event == 'Quit':
            exit()
        elif event == 'Confirm':
            feed = Feed(feed.feed_input, desired_height=600, desired_width=600)
            print(feed.feed_input)
            feed.configRotHSV(rot, (hsv_vals[0], hsv_vals[1]),
                            (hsv_vals[2], hsv_vals[3]),
                            (hsv_vals[4], hsv_vals[5]))
            feed.configCrop(crop_vals[2], crop_vals[3], 
                            crop_vals[0], crop_vals[1])
            # feed.configScale(desired_height=400, desired_width=400)
            setup_window.close()
            
            return feed
            graph.get
        elif event == 'graph' or event.endswith('+UP'):
            # print(event, values)
            # print(f'Startpoint: {startpoint}, Endpoint: {endpoint}, Dim {dims}')
            coords = values['graph']
            if event.endswith('+UP'):
                endpoint = coords
                dragging = False
            elif dragging:
                endpoint = coords
            else:
                startpoint = coords
                dragging = True

        if startpoint != endpoint and not dragging:
            crop_vals = getCrop(startpoint, endpoint, dims)
        img, location, scale = processFeed(feed, hsv_vals, crop_vals, apply_hsv)
        # setup_window['preview'].update(data=img)
        preview.erase()
        preview.draw_image(data=img, location=location)
        graph.draw_rectangle(startpoint, endpoint, line_color='white', line_width=3)


def processFeed(feed: Feed, hsv_vals, crop_vals, apply_hsv):
    frame = feed.getFrame(True)[0]
    
    x1, x2, y1, y2 = crop_vals
    # print(f'Crop: x1: {x1}, x2: {x2}, y1: {y1}, y2: {y2}')
    if apply_hsv:
        frame = hsvProcess(frame, hsv_vals[0], hsv_vals[1], hsv_vals[2], 
                        hsv_vals[3], hsv_vals[4], hsv_vals[5])
    frame = frame[y1:y2, x1:x2]
    frame, scale = scaleFrame(frame)

    location = center((frame.shape[1], frame.shape[0]))

    return cv2.imencode('.png', frame)[1].tobytes(), location, scale

def scaleFrame(img, desired_height=400, desired_width=300):
    height = img.shape[0]
    width = img.shape[1]

    scale = 1
    resized = False

    # print(f'Input Resolution: {width, height}')
    while height*scale > desired_height and width*scale > desired_width:
        # print(f'Resizing Down: {scale}, {int(width*scale), int(height*scale)}')
        resized = True
        scale -= 0.1

    # TODO add scale up toggle
    while not resized and (height*scale < desired_height and width*scale < desired_width):
        # print(f'Resizing Up: {scale}, {int(width*scale), int(height*scale)}')
        scale += 0.1

    height = int(height * scale-0.1)
    width = int(width * scale-0.1)
    
    # print(f'Resized to {width, height} with scale {scale}')

    return resize(img, (width, height)), scale

def getCrop(startpoint=(1,1), endpoint=(384, 288), dims=(-1,-1)):
    x1, y1 = startpoint
    x2, y2 = endpoint

    if x2 < 0 or y2 < 0 or x2 > dims[0] or y2 > dims[1]:
        x1, y1 = 0, 0
        x2, y2 = dims[0], dims[1]
    else:
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
            # exit()
    
    return x1, x2, y1, y2

def center(input_dim, preview_dim=(400, 300)):
    # print(input_dim)
    hor_dif = preview_dim[0] - input_dim[0]
    vert_dif = preview_dim[1] - input_dim[1]
    if hor_dif < -1:
        hor_dif = 0
    elif vert_dif < -1:
        vert_dif = 0
    location = int(0.5*hor_dif), int(0.5*vert_dif)
    # print(location)
    return location


if __name__ == '__main__':
    # center((200, 150))

    # feed = Feed(0, 300, 400)
    # filterSetup(feed)
    
    filterSetup(Feed('Tests\RealTwo.jpg', 600, 600))