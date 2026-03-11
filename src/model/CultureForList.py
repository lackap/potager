class CultureForList(object):
    def __init__(self, culture, nombre):
        self.culture = culture
        self.nombre = nombre
        self.taille_requise = nombre * culture.taille_necessaire