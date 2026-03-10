from src.model.CultureForList import CultureForList


class ListCulture(object):
    def __init__(self):
        self.cultures = []

    def add_culture(self, culture, nombre):
        item = self.find_culture(culture)
        if item is not None:
            item.nombre = nombre
        else:
            self.cultures.append(CultureForList(culture, nombre))

    def increase_culture(self, culture):
        item = self.find_culture(culture)
        if item is not None:
            item.nombre = item.nombre + 1
        else:
            self.cultures.append(CultureForList(culture, 1))

    def decrease_culture(self, culture):
        item = self.find_culture(culture)
        if item is not None:
            item.nombre = item.nombre - 1
        else:
            self.cultures.append(CultureForList(culture, 0))


    def find_culture(self, culture):
        for item in self.cultures:
            if item.culture.culture_type == culture.culture_type:
                return item
        return None

    def find_culture_number(self, culture):
        item = self.find_culture(culture)
        if item is not None:
            return item.nombre
        else:
            return 0

