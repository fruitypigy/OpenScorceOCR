import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import VerticalSeparator

# a = 'Hello\rWorld'

# print(a)

# for char in a : a=a.replace('\rw', '')
# # for char in hi : hi=hi.replace('\n', '')
# print(a)

QT_ENTER_KEY1 =  'special 16777220'
QT_ENTER_KEY2 =  'special 16777221'

# dict = {0 : 'Item 1'}
#     0 : 'First',
#     1 : 'Second',
#     2 : 'Third',
#     3 : 'Fourth',
#     4 : 'Fifth'
# }

values_list = ['Item 1']

layout = [[sg.Listbox(values_list, default_values='Item 1', key='listbox', size=(8, 8), enable_events=True)], 
        [sg.Input('Item 1', size=(10, 3), key='input')], [sg.Button('New')], [sg.Text(0, key='number')]]

window = sg.Window('Dictionary Test', layout, size=(400, 400), return_keyboard_events=True)

listbox = window['listbox'] # type: sg.Listbox
selected = 0
last_selected = None

while True:
    event, values = window.read()
    
    if event == None:
        exit()
    elif event == 'New':
        if f'Item {len(values_list)+1}' not in values_list:
            values_list.append(f'Item {len(values_list)+1}')
        else:
            values_list.append(f'Item {len(values_list)+2}')
        listbox.update(values_list)
    elif listbox.get_indexes() and event == '\r' and values['input'] not in values_list:
        values_list[listbox.get_indexes()[0]] = values['input']
        listbox.update(values_list)
    elif listbox.get_indexes() and (values_list[listbox.get_indexes()[0]] == values['input'] or event == 'listbox'):
        window['input'].update(values_list[listbox.get_indexes()[0]])


# layout = [[sg.Listbox(list(dict.values()), default_values='Item 1', key='listbox', size=(8, 8), enable_events=True)], 
#         [sg.Input('Item 1', size=(10, 3), key='input')], [sg.Button('New')], [sg.Text(0, key='number')]]

# window = sg.Window('Dictionary Test', layout, size=(400, 400), return_keyboard_events=True)

# listbox = window['listbox'] # type: sg.Listbox
# selected = 0
# last_selected = None

# while True:
#     event, values = window.read()

#     if event == 'listbox':
#         value = values['listbox']
#         length = len(listbox.get_list_values())
#         for i in range(length):
#             if value[0] == list(dict.values())[i]:
#                 # print(f'Value: {value}, Place: {i}')
#                 input_update = list(dict.values())[i]
#                 for char in input_update : input_update = input_update.replace('\n', '')
#                 window['input'].update(input_update)
#                 selected = i
#                 break
#     if ((event == '\r') and (len(values['listbox']))
#      and (last_selected != selected) and values['input'] not in list(dict.values())):
#         dict[selected] = values['input']
#         last_selected = selected
#         listbox.update(list(dict.values()))
#     elif event == 'New':
#         dict.update({len(dict) : f'Item {len(dict)+1}\n'})
#         listbox.update(list(dict.values()))

#     print(listbox.get_indexes())

#     window['number'].update(selected)
#     # print(values['input'])
#     if event == None:
#         break

#
#  dict = {
#     0 : 'devon',
#     1 : 'not devon',
#     2 : 'also not devon',
#     3 : 'really not devon'
# }

# dict[4] = 'definitely not devon'

# list = list(dict)

# print(dict.items)