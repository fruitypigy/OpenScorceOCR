from ImageProcess import hsvProcess, resize, warpPerspective
import PySimpleGUI as sg
import cv2
from Feed import Feed


def filterSetup(feed: Feed):
    # def filterSetup():
    slider_elements = [sg.Text('Hue Min', size=(7, 1)),
                       sg.Slider((0, 255), 0, orientation='vertical', key='HUE_MN', enable_events=True),
                       sg.Text('Hue Max', size=(7, 1)),
                       sg.Slider((0, 255), 255, orientation='vertical', key='HUE_MX', enable_events=True)], \
                      [sg.Text('Sat Min', size=(7, 1)),
                       sg.Slider((0, 255), 0, orientation='vertical', key='SAT_MN', enable_events=True),
                       sg.Text('Sat Max', size=(7, 1)),
                       sg.Slider((0, 255), 255, orientation='vertical', key='SAT_MX', enable_events=True)], \
                      [sg.Text('Val Min', size=(7, 1)),
                       sg.Slider((0, 255), 0, orientation='vertical', key='VAL_MN', enable_events=True),
                       sg.Text('Val Max', size=(7, 1)),
                       sg.Slider((0, 255), 255, orientation='vertical', key='VAL_MX', enable_events=True)], \
                      [sg.Text('Rotation'), sg.Spin((list(range(-179, 180))), 0, key='ROT', size=(4, 4))], \
                      [sg.Checkbox('Apply HSV Filter', key='apply_hsv')]

    input_elements = [sg.Text('Width'),
                      sg.Spin((list(range(100, 800))), 600, size=(6, 4), key='width', enable_events=True),
                      sg.Text('Height'),
                      sg.Spin((list(range(100, 800))), 300, size=(6, 4), key='height', enable_events=True),
                      sg.Text('Horizontal Stretch'),
                      sg.Spin((list(range(-20, 20))), 0, size=(4, 4), key='hor_stretch', enable_events=True),
                      sg.Text('Vertical Stretch'),
                      sg.Spin((list(range(-20, 20))), 0, size=(4, 4), key='vert_stretch', enable_events=True),
                      sg.Text('Horizontal Stretch 2'),
                      sg.Spin((list(range(-20, 20))), 0, size=(4, 4), key='hor2_stretch', enable_events=True),
                      sg.Text('Vertical Stretch 2'),
                      sg.Spin((list(range(-20, 20))), 0, size=(4, 4), key='vert2_stretch', enable_events=True)]

    spin_element = sg.Text('Number of Digits'), sg.Spin([i for i in range(1, 19)], 1, size=(3, 2), key='segment_number')

    input_graph_element = sg.Graph(canvas_size=(feed.width, feed.height), graph_bottom_left=(0, feed.height),
                                   graph_top_right=(feed.width, 0), enable_events=True, drag_submits=True,
                                   key="graph", background_color='green')

    preview_element = [sg.Text('Preview')], [
        sg.Graph((600, 300), (0, 300), (600, 0), background_color='grey', key='preview')]

    setup_layout = [[input_graph_element, sg.Column(slider_elements), sg.Column(preview_element)], input_elements,
                    [sg.Button('Confirm'), sg.Button('Quit'), spin_element]]
    # setup_layout = [[sg.Column(slider_elements), sg.Column(preview_element)], [sg.Button('Confirm'), sg.Button('Quit'), spin_element]]

    setup_window = sg.Window('Setup', setup_layout)

    graph = setup_window['graph']  # type: sg.Graph
    preview = setup_window['preview']  # type: sg.Graph

    hsv_vals = (0, 255, 0, 255, 0, 255)

    dragging = False

    # dims = (feed.width, feed.height)
    startpoint = endpoint = (-1, -1)
    # crop_vals = getCrop((1,1),(dims[0], dims[1]),dims)

    coords = []
    adj_coords = [(), (), (), ()]
    warped = feed.getFrame(True)[0]
    warped_encoded = None
    skip_warp = False
    saved_coords = None

    while True:
        event, values = setup_window.read(timeout=100)
        graph.erase()
        preview.erase()
        graph.draw_image(data=feed.getFrame(True)[1], location=(0, 0))

        height = int(values['height'])
        width = int(values['width'])

        hsv_vals = (values['HUE_MN'], values['HUE_MX'],
                    values['SAT_MN'], values['SAT_MX'],
                    values['VAL_MN'], values['VAL_MX'],)
        rot_input = values['ROT']
        if type(rot_input) == int and 180 > rot_input > -180:
            rot = rot_input
        else:
            rot = 0
        feed.configRotHSV(rot)
        # graph = feed.drawFrame(graph, True)
        apply_hsv = values['apply_hsv']
        if event is None or event == 'Quit':
            exit()
        elif event == 'Confirm':
            feed = Feed(feed.feed_input, desired_height=600, desired_width=600)
            print(feed.feed_input)
            feed.configRotHSV(rot, (hsv_vals[0], hsv_vals[1]),
                              (hsv_vals[2], hsv_vals[3]),
                              (hsv_vals[4], hsv_vals[5]))

            print(saved_coords)
            feed.configWarp(coords, (width, height))
            feed.getFrame()
            # feed.configCrop(crop_vals[2], crop_vals[3], 
            #                 crop_vals[0], crop_vals[1])
            # feed.configScale(desired_height=400, desired_width=400)
            setup_window.close()

            return feed, values['segment_number']
            pass
        elif event.endswith('+UP'):
            if len(coords) > 3:
                coords.clear()
            coords.append(values['graph'])
            print(f'Added: {coords}')
            warped_encoded = None
            skip_warp = False
        elif len(coords) == 4 and ((not skip_warp) or
                                   (event == 'width' or event == 'height') or event.endswith('stretch')):
            print(f'Coords: {coords}')
            adj_coords[0] = (coords[0][0] + int(values['hor_stretch'])), (coords[0][1] + int(values['vert_stretch']))
            adj_coords[1] = (coords[1][0] + int(values['hor_stretch'])), (coords[1][1] + int(values['vert2_stretch']))
            adj_coords[2] = (coords[2][0] + int(values['hor2_stretch']), coords[2][1] + int(values['vert_stretch']))
            adj_coords[3] = (coords[3][0] + int(values['hor2_stretch']), coords[3][1] + int(values['vert2_stretch']))
            print(f'Adjusted: {adj_coords}')
            warped, warped_encoded = warpPerspective(feed.getFrame(True)[0], adj_coords, dims=(width, height))
            skip_warp = True

        # print(f'Length of Coords: {len(coords)}, Skip Warp: {skip_warp}')
        location = center((warped.shape[1], warped.shape[0]))

        if apply_hsv:
            frame = processFeed(warped, hsv_vals)
        else:
            frame = cv2.imencode('.png', warped)[1].tobytes()

        preview.draw_image(data=frame, location=location)
        graph = drawPoints(graph, coords)


def drawPoints(graph: sg.Graph, points: list[tuple]):
    for point in points:
        graph.draw_circle(point, 3, fill_color='red')
    return graph


def processFeed(img, hsv_vals):
    frame = hsvProcess(img, hsv_vals[0], hsv_vals[1], hsv_vals[2],
                       hsv_vals[3], hsv_vals[4], hsv_vals[5])
    return cv2.imencode('.png', frame)[1].tobytes()


def scaleFrame(img, desired_height=400, desired_width=300):
    height = img.shape[0]
    width = img.shape[1]

    scale = 1
    resized = False

    # print(f'Input Resolution: {width, height}')
    while height * scale > desired_height and width * scale > desired_width:
        # print(f'Resizing Down: {scale}, {int(width*scale), int(height*scale)}')
        resized = True
        scale -= 0.1

    # TODO Fix scale up
    # while not resized and (height*scale < desired_height or width*scale < desired_width):
    #     print(f'Resizing Up: {scale}, {int(width*scale), int(height*scale)}')
    #     scale += 0.1

    height = int(height * scale - 0.1)
    width = int(width * scale - 0.1)

    # print(f'Resized to {width, height} with scale {scale}')

    return resize(img, (width, height)), scale


def center(input_dim, preview_dim=(600, 300)):
    # print(input_dim)
    hor_dif = preview_dim[0] - input_dim[0]
    vert_dif = preview_dim[1] - input_dim[1]
    if hor_dif < -1:
        hor_dif = 0
    elif vert_dif < -1:
        vert_dif = 0
    location = int(0.5 * hor_dif), int(0.5 * vert_dif)
    # print(location)
    return location


if __name__ == '__main__':
    pass
    # center((200, 150))

    # feed = Feed(0, 300, 400)
    # filterSetup(feed)

    filterSetup(Feed('TestInputs\WarpTest2.jpg', 600, 600))
    # print(number)
    # filterSetup()
