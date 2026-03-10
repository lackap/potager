from PyQt5 import QtGui

from src.model.CaseTableau import CaseTableau
from src.model.Culture import Culture
from src.model.ListCulture import ListCulture


class EspaceTravaillable(object):
    def __init__(self):
        self.endX = 60
        self.endY = 60
        self.defaultColor = QtGui.QColor(192,192,192)
        self.cultures = {}
        self.list_a_planter = ListCulture()
        self.list_plantes = ListCulture()
        self.count_a_planter = 0
        self.initialize()

    def add_planche(self,planche):
        for row in range(planche.startX, planche.endX):
            for column in range(planche.startY, planche.endY):
                self.cultures[row,column].travaillable = True
                self.cultures[row,column].planche = planche

    def set_culture(self, row, column, culture):
        self.cultures[row,column].culture = culture

    def add_culture(self, culture, nombre):
        self.list_a_planter.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column):
        self.list_a_planter.decrease_culture(culture)
        self.list_plantes.increase_culture(culture)
        match culture.taille_necessaire:
            case 0:
                self.cultures[row, column].culture = Culture.NONE
            case 1 | 2 | 3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        self.cultures[row+rows, column+columns].culture = culture
        return culture

    def enlever_culture(self, row, column):
        culture = self.cultures[row, column].culture
        self.list_plantes.decrease_culture(culture)
        self.list_a_planter.increase_culture(culture)
        match culture.taille_necessaire:
            case 0:
                self.cultures[row, column].culture = Culture.NONE
            case 1 | 2 | 3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        self.cultures[row, column].culture = Culture.NONE
        return culture

    def deplacer_culture(self, rowinit, columninit, row, column):
        culture = self.cultures[rowinit, columninit].culture
        self.placer_culture(Culture.NONE, rowinit,columninit)
        self.placer_culture(culture, row, column)
        return culture

    def get_culture(self, row, column):
        return self.cultures[row, column].culture

    def est_culturable(self, row, column):
        return self.cultures[row, column].travaillable and (not self.cultures[row, column].culture or
                    self.cultures[row, column].culture is None or self.cultures[row, column].culture == Culture.NONE)

    def initialize(self):
        for row in range(self.endX):
            for column in range(self.endY):
                self.cultures[row, column] = CaseTableau(row, column)
