from src.lackap.projet.potager.model.CultureForList import CultureForList
from src.lackap.projet.potager.model.CulturesAssociees import CulturesAssociees


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
            item.nombre_plantes = item.nombre_plantes - 1
        else:
            self.cultures.append(CultureForList(culture, 1))

    def decrease_culture(self, culture):
        item = self.find_culture(culture)
        if item is not None:
            item.nombre = item.nombre - 1
            item.nombre_plantes = item.nombre_plantes + 1
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

    def grouper_culture_associable(self):
        cultures_associees = []
        for culture_for_list in self.cultures:
            added = False
            for cultures_associee in cultures_associees:
                if self.est_associable_groupe(culture_for_list, cultures_associee):
                    cultures_associee.add_culture(culture_for_list)
                    added = True
                    break
            if not added:
                cultures_associee = CulturesAssociees()
                cultures_associee.add_culture(culture_for_list)
                cultures_associees.append(cultures_associee)
        cultures_associees.sort(key=lambda x: x.taille, reverse=True)
        return cultures_associees

    def est_associable_groupe(self, culture_for_list, cultures_associe):
        for culture_associee in cultures_associe.cultures:
            if not culture_for_list.culture.associable(culture_associee.culture):
                return False
        return True

