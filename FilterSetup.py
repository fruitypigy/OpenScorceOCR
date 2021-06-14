from ImageProcess import hsv_process, resize, warpPerspective
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
                      sg.Spin((list(range(100, 800))), 300, size=(6, 4), key='height', enable_events=True)]

    spin_element = sg.Text('Number of Digits'), sg.Spin([i for i in range(1, 19)], 1, size=(3, 2), key='segment_number')

    point_selector = [sg.Radio('Point 1', 'point_sel', key='point1', default=True),
                      sg.Radio('Point 2', 'point_sel', key='point2'),
                      sg.Radio('Point 3', 'point_sel', key='point3'),
                      sg.Radio('Point 4', 'point_sel', key='point4')]

    input_graph_element = sg.Graph(canvas_size=(feed.width, feed.height), graph_bottom_left=(0, feed.height),
                                   graph_top_right=(feed.width, 0), enable_events=True, drag_submits=True,
                                   key="graph", background_color='green')

    preview_element = [sg.Text('Preview')], [
        sg.Graph((600, 400), (0, 400), (600, 0), background_color='grey', key='preview')]

    setup_layout = [[input_graph_element,
                     sg.Column(slider_elements),
                     sg.Column(preview_element)],
                    point_selector, input_elements,
                    [sg.Button('Confirm', disabled=True),
                     sg.Button('Quit'), spin_element]]
    setup_window = sg.Window('Setup', setup_layout, return_keyboard_events=True)

    graph = setup_window['graph']  # type: sg.Graph
    preview = setup_window['preview']  # type: sg.Graph

    coords = []
    warped = feed.get_frame(True)[0]
    skip_warp = False
    saved_coords = None

    while True:
        event, values = setup_window.read(timeout=100)
        graph.erase()
        preview.erase()
        graph.draw_image(data=feed.get_frame(True)[1], location=(0, 0))

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
        apply_hsv = values['apply_hsv']
        if event is None or event == 'Quit':
            exit(0)
        elif event == 'Confirm':
            feed = Feed(feed.feed_input, desired_height=600, desired_width=600)
            print(feed.feed_input)
            feed.configRotHSV(rot, (hsv_vals[0], hsv_vals[1]),
                              (hsv_vals[2], hsv_vals[3]),
                              (hsv_vals[4], hsv_vals[5]))

            print(saved_coords)
            feed.configWarp(coords, (width, height))
            feed.get_frame()
            setup_window.close()

            return feed, values['segment_number']
            pass
        elif event.endswith('+UP'):
            if len(coords) > 3:
                coords.clear()
            coords.append(values['graph'])
            print(f'Added: {coords}')
            skip_warp = False
        elif len(coords) == 4 and ((not skip_warp) or
                                   (event == 'width' or
                                    event == 'height') or
                                   event in ['w', 'a', 's', 'd']):
            setup_window['Confirm'].update(disabled=False)

            if event in ['w', 'a', 's', 'd']:
                point_count = 0
                for point in ['point1', 'point2', 'point3', 'point4']:
                    if values[point]:
                        print(f'Point: {point}')
                        break
                    point_count += 1
                point = coords[point_count]
                if event == 'w':
                    point = point[0], point[1] - 1
                if event == 'a':
                    point = point[0] - 1, point[1]
                if event == 's':
                    point = point[0], point[1] + 1
                if event == 'd':
                    point = point[0] + 1, point[1]
                coords[point_count] = point
                print(f'Adjusted: {coords}')
            warped, warped_encoded = warpPerspective(feed.get_frame(True)[0], coords, dims=(width, height))
            skip_warp = True
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
    frame = hsv_process(img, hsv_vals[0], hsv_vals[1], hsv_vals[2],
                       hsv_vals[3], hsv_vals[4], hsv_vals[5])
    return cv2.imencode('.png', frame)[1].tobytes()


def scaleFrame(img, desired_height=400, desired_width=300):
    height = img.shape[0]
    width = img.shape[1]

    scale = 1
    while height * scale > desired_height and width * scale > desired_width:
        scale -= 0.1

    # TODO Fix scale up
    # while not resized and (height*scale < desired_height or width*scale < desired_width):
    #     print(f'Resizing Up: {scale}, {int(width*scale), int(height*scale)}')
    #     scale += 0.1

    height = int(height * scale - 0.1)
    width = int(width * scale - 0.1)

    # print(f'Resized to {width, height} with scale {scale}')

    return resize(img, (width, height)), scale


def center(input_dim, preview_dim=(600, 400)):
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
