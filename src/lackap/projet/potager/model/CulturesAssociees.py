
class CulturesAssociees(object):
    def __init__(self):
        self.cultures = []
        self.taille = 0

    def add_culture(self, culture_for_list):
        taille_culture = culture_for_list.culture.taille_necessaire * culture_for_list.nombre
        self.taille = self.taille + taille_culture
        self.cultures.append(culture_for_list)