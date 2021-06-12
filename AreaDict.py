from SelectedArea import SelectedArea as sa


def remove_special(name: str):
    special_chars = ' `~!@#$%^&*()_+=-,:./<>?;"[]\\\{\}|' + "'"
    scrubbed_name = name
    for special in special_chars:
        scrubbed_name = scrubbed_name.replace(special, '')
    if scrubbed_name[0].isdigit():
        scrubbed_name += 'n'
    return scrubbed_name


class AreaDict:

    def __init__(self, area_number):
        self.area_dict = {'Digit1': sa()}  # type: dict[str, sa]
        for areas in range(area_number - 1):
            self.add()

    def __call__(self):
        return self.area_dict

    def rename(self, original_key: str, new_key: str):
        if not new_key:
            print(Exception(f'Cannot rename to nothing'))
            return original_key
        elif new_key in self.area_dict.keys():
            print(Exception(f"Cannot rename '{original_key}' to '{new_key}': Key already exists"))
            return original_key
        elif original_key in self.area_dict.keys():
            new_key = remove_special(new_key)
            new_dict = {}
            for key in self.area_dict.keys():
                if key == original_key:
                    new_dict[new_key] = self.area_dict[key]
                else:
                    new_dict[key] = self.area_dict[key]
            self.area_dict = new_dict
            return new_key
        else:
            print(Exception(f"Cannot rename '{original_key}' to '{new_key}': Key not in dict"))
            return original_key

    def remove(self, key: str):
        if key in self.area_dict.keys():
            self.area_dict.pop(key)
        else:
            print(Exception(f"Cannot remove '{key}': Key does not exist in dict"))

    def add(self, key=''):
        if not key:
            # TODO Change number if same key already exists
            key = f'Digit{len(self.area_dict) + 1}'
        else:
            key = remove_special(key)
        if key not in self.area_dict.keys():
            print(self.area_dict.values())
            old_area = list(self.area_dict.values())[-1]
            self.area_dict[key] = sa(old_area.pos, (old_area.length, old_area.height))
        else:
            print(Exception(f"Cannot add '{key}': Key already exists in dict"))

        return key

    def update_xml(self, filename: str):
        xml = '<?xml version="1.0"?>\n<root>'
        for key in self.area_dict.keys():
            val = self.area_dict[key].getDigit()[0]
            xml += f'\n\t<{key}>{val}</{key}>'
        # TODO Check for duplicate names after scrubbing
        xml += '\n</root>'

        file = open(filename, 'w')
        file.write(xml)
        return xml


if __name__ == '__main__':
    area_dict = AreaDict(3)
    print(area_dict())
    area_dict.rename('Digit1', 'Other')
    print(area_dict())

    selected_area = 'Digit'
