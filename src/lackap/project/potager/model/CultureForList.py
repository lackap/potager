class CultureForList(object):
    def __init__(self, culture, nombre, nombre_plantes = 0):
        self.culture = culture
        self.nombre = nombre
        self.nombre_plantes = nombre_plantes
        self.taille_requise = nombre * culture.taille_necessaire