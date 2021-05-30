import PySimpleGUI as sg

graph_element = sg.Graph((400, 400), (0, 400), (400, 0), enable_events=True, key='graph',drag_submits=True)

layout = [[graph_element]]

window = sg.Window('Resizeable Rectangle Test', layout, return_keyboard_events=True, finalize=True)

graph = window['graph'] # type: sg.Graph

dim = ((20,20), (40,40))

def drawRectangle(pos=(200, 200), length=10, height=10):
    top_left = ( (pos[0] - length), (pos[1] + height) )
    bottom_right = ( pos[0] + length), (pos[1] - height)
    return graph.draw_rectangle(top_left, bottom_right)

rectangle = drawRectangle()

length = 10
height = 10
cursor_pos = (0,0)

while True:
    event, values = window.read()
    if event == 'graph':
        cursor_pos = values['graph']
        graph.delete_figure(rectangle)
        rectangle = drawRectangle(cursor_pos, length, height)
    elif event == 'Left:37':
        graph.move_figure(rectangle, -1, 0)
    elif event == 'Up:38':
        graph.move_figure(rectangle, 0, -1)
    elif event == 'Right:39':
        graph.move_figure(rectangle, 1, 0)
    elif event == 'Down:40':
        graph.move_figure(rectangle, 0, 1)
    elif event == 'MouseWheel:Up' and length < 50: 
        length += 5
        height += 5
        graph.delete_figure(rectangle)
        rectangle = drawRectangle(cursor_pos, length, height)
    elif event == 'MouseWheel:Down' and length > 5:
        length -= 5
        height -= 5
        graph.delete_figure(rectangle)
        rectangle = drawRectangle(cursor_pos, length, height)


    if event == None:
        break
    