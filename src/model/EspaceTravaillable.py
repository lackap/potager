from PyQt5 import QtGui

from src.model.CaseTableau import CaseTableau
from src.model.Culture import Culture
from src.model.ListCulture import ListCulture
from src.model.Planche import Planches
from src.model.Priority import Priority


class EspaceTravaillable(object):
    def __init__(self):
        self.endX = 60
        self.endY = 60
        self.defaultColor = QtGui.QColor(192,192,192)
        self.cultures = {}
        self.list_a_planter = ListCulture()
        self.list_plantes = ListCulture()
        self.initialize()
        self.planches = Planches()

    def add_planche(self,planche):
        for row in range(planche.startX, planche.endX):
            for column in range(planche.startY, planche.endY):
                self.cultures[row,column].travaillable = True
                self.cultures[row,column].planche = planche
                planche.add_culture(row, column, Culture.NONE)

    def add_culture(self, culture, nombre):
        self.list_a_planter.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column, taille = None):
        if taille is None:
            taille = culture.taille_necessaire
        self.list_a_planter.decrease_culture(culture)
        self.list_plantes.increase_culture(culture)
        match taille:
            case 0:
                self.cultures[row, column].culture = Culture.NONE
            case 1 | 2 | 3:
                for rows in range(taille):
                    for columns in range(taille):
                        self.cultures[row+rows, column+columns].culture = culture
                        self.cultures[row+rows, column+columns].planche.add_culture(row+rows, column+columns, culture)
                self.cultures[row, column].planche.set_culture_start(row, column)

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
                        self.cultures[row+rows, column+columns].culture = Culture.NONE
                        self.cultures[row+rows, column+columns].init_culture = None
                        self.cultures[row+rows, column+columns].planche.add_culture(row+rows, column+columns, Culture.NONE)
        return culture

    def deplacer_culture(self, rowinit, columninit, row, column):
        culture = self.cultures[rowinit, columninit].culture
        self.placer_culture(Culture.NONE, rowinit,columninit, culture.taille_necessaire)
        self.placer_culture(culture, row, column)
        return culture

    def get_culture(self, row, column):
        return self.cultures[row, column].culture

    def est_culturable(self, row, column):
        return self.cultures[row, column].travaillable and (not self.cultures[row, column].culture or
                    self.cultures[row, column].culture is None or self.cultures[row, column].culture == Culture.NONE)

    def find_meilleure_planche(self, culture, nombre, optimized):
        priority = Priority(0, 0)
        planche_prioritaire = None
        for planche in self.planches.planches:
            planche_priority = planche.get_priority(culture, nombre, optimized)
            if (priority.level < planche_priority.level
                    or (priority.level == planche_priority.level and priority.nombre < planche_priority.nombre)):
                priority = planche_priority
                planche_prioritaire = planche
        if priority.level > 0:
            print("On a trouvé la planche " + planche_prioritaire.name + " pour la culture " + culture.culture_type + " avec la priorité " + str(priority.level))
            return planche_prioritaire
        else:
            return None

    def can_insert_culture(self, row, column, culture):
        match culture.taille_necessaire:
            case 0:
                current = self.est_culturable(row, column)
                if not current:
                    return False
            case 1|2|3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        current = self.est_culturable(row+rows, column+columns)
                        if not current:
                            return False
        return True

    def initialize(self):
        for row in range(self.endX):
            for column in range(self.endY):
                self.cultures[row, column] = CaseTableau()
