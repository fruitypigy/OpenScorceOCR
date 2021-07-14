import PySimpleGUI as sg

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

editor_window = sg.Window('Editor Window', editor_layout)

while True:
    event, values = editor_window.read()
    if event is None or event == 'Cancel':
        break
