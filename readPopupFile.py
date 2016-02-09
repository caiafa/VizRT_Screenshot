import xlrd
import configuration


def is_integer(string):
    try:
        int(string)
        return int(string)
    except ValueError:
        return False


class Popups:
    def __init__(self, popup_list):
        self.popup_list = popup_list
        self.ws = xlrd.open_workbook(self.popup_list).sheet_by_index(0)
        self.active = None
        self.active_popups()

    def active_popups(self):
        active_items = []

        for row in range(1, self.ws.nrows):
            number = is_integer(self.ws.cell(row, 0).value)
            description = str(self.ws.cell(row, 1).value)
            if number:
                item = str(number) + " - " + str(description)
                active_items.append(item)

        self.active = active_items

if __name__ == "__main__":
    popup_ids = Popups(popup_list=configuration.popup_list_path)
    print(popup_ids.active)

