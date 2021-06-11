def rename(dict: dict, key: str, new: str):
        if new in dict.keys():
            print(Exception(f"Cannot rename '{key}' to '{new}': Key already exists"))
        elif key in dict.keys():
            new = removeSpecial(new)
            val = dict.get(key)
            dict.pop(key)
            dict[new] = val
        else:
            print(Exception(f"Cannot rename '{key}' to '{new}': Key not in dict"))
        return dict

def removeSpecial(name: str):
    special_chars = '`~!@#$%^&*()_+=-,./<>?;"[]\\\{\}|' + "'"
    for special in special_chars:
        print(special)
        name = name.replace(special, '')
    if name[0].isdigit():
        name = 'n' + name
    return name

def remove(dict: dict, key: str):
        if key in dict.keys():
            dict.pop(key)
        else:
            print(Exception(f"Cannot remove '{key}': Key does not exist in dict"))
        return dict

def add(dict: dict, key: str, val: tuple):
        if key not in dict.keys():
            key = removeSpecial(key)
            dict[key] = val
        else:
            print(Exception(f"Cannot add '{key}': Key already exists in dict"))
        return dict

def updateXML(dict: dict, filename: str):

    xml = '<?xml version="1.0"?>\n<root>'
    for key in dict.keys():
        val = dict[key][0]
        xml += f'\n\t<{key}>{val}</{key}>'
    xml += '\n</root>'

    file = open(filename, 'w')
    file.write(xml)
    return xml
