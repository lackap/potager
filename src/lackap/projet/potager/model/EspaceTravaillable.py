from PyQt5 import QtGui

from src.lackap.projet.potager.model.CaseTableau import CaseTableau
from src.lackap.projet.potager.model.Culture import Culture, HauteurCulture
from src.lackap.projet.potager.model.ListCulture import ListCulture
from src.lackap.projet.potager.model.Planche import Planches
from src.lackap.projet.potager.model.Priority import Priority


class EspaceTravaillable(object):
    def __init__(self):
        self.endX = 60
        self.endY = 60
        self.defaultColor = QtGui.QColor(192,192,192)
        self.cultures_haute = {}
        self.cultures_basse = {}
        self.list_a_planter = ListCulture()
        self.initialize()
        self.planches = Planches()

    def add_planche(self,planche):
        for row in range(planche.start_x, planche.end_x):
            for column in range(planche.start_y, planche.end_y):
                self.cultures_haute[row,column].travaillable = True
                self.cultures_basse[row,column].travaillable = True
                if planche.planche_fixe:
                    planche.add_culture(row, column, planche.ancienne_culture)
                else:
                    planche.add_culture(row, column, Culture.NONE)

    def add_culture(self, culture, nombre):
        self.list_a_planter.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column, taille = None):
        if taille is None:
            taille = culture.taille_necessaire
        self.list_a_planter.decrease_culture(culture)
        match taille:
            case 0:
                self.cultures_haute[row, column].culture = Culture.NONE
                self.cultures_basse[row, column].culture = Culture.NONE
            case 1 | 2 | 3:

                for rowindex in range(row, row+taille):
                    for columnindex in range(column, column+taille):
                        if culture.hauteur_culture == HauteurCulture.BASSE or culture.hauteur_culture == HauteurCulture.COMPLETE:
                            self.cultures_basse[rowindex, columnindex].culture = culture
                        if culture.hauteur_culture == HauteurCulture.HAUTE or culture.hauteur_culture == HauteurCulture.COMPLETE:
                            self.cultures_haute[rowindex, columnindex].culture = culture
                        self.planches.find_planche(rowindex, columnindex).add_culture(rowindex, columnindex, culture)
                self.planches.find_planche(row, column).set_culture_start(row, column, True, culture.hauteur_culture)

        return culture

    def enlever_culture(self, row, column):
        culture_haute = self.cultures_haute[row, column].culture
        culture_basse = self.cultures_basse[row, column].culture
        if culture_haute is not None and not culture_haute == Culture.NONE:
            self.enlever_culture_hauteur(row, column, culture_haute, self.cultures_haute)
        if culture_basse is not None and not culture_basse == Culture.NONE:
            self.enlever_culture_hauteur(row, column, culture_basse, self.cultures_basse)
        if culture_haute is not None and not culture_haute == Culture.NONE:
            self.list_a_planter.increase_culture(culture_haute)
            if culture_basse is not None and not culture_basse == Culture.NONE and culture_basse.hauteur_culture == HauteurCulture.BASSE:
                self.list_a_planter.increase_culture(culture_basse)
        else:
            if culture_basse is not None and not culture_basse == Culture.NONE:
                self.list_a_planter.increase_culture(culture_basse)

    def enlever_culture_hauteur(self, row, column, culture, cultures):
        if culture is not None and not culture == Culture.NONE:
            match culture.taille_necessaire:
                case 0:
                    self.cultures_haute[row, column].culture = Culture.NONE
                case 1 | 2 | 3:
                    for rowindex in range(row, row+culture.taille_necessaire):
                        for columnindex in range(column, column+culture.taille_necessaire):
                            cultures[rowindex,columnindex].culture = Culture.NONE
                            self.planches.find_planche(rowindex, columnindex).set_culture_start(rowindex, columnindex, None)
                            self.planches.find_planche(rowindex, columnindex).add_culture(rowindex, columnindex, Culture.NONE)


    def deplacer_culture(self, rowinit, columninit, row, column):
        culture_haute = self.cultures_haute[rowinit, columninit].culture
        culture_basse = self.cultures_haute[rowinit, columninit].culture
        if self.enlever_culture(rowinit, columninit) is not None:
            self.placer_culture(culture_haute, row, column)
            self.placer_culture(culture_basse, row, column)
        return culture_haute

    def get_culture(self, row, column, hauteur = HauteurCulture.BASSE):
        if hauteur == HauteurCulture.BASSE:
            return self.cultures_basse[row, column].culture
        else:
            return self.cultures_haute[row, column].culture

    def est_culturable(self, row, column, hauteur_culture):
        culturable = True
        if hauteur_culture == HauteurCulture.BASSE or hauteur_culture == HauteurCulture.COMPLETE:
            culturable = self.cultures_basse[row, column].travaillable and (not self.cultures_basse[row, column].culture or self.cultures_basse[row, column].culture is None or self.cultures_basse[row, column].culture == Culture.NONE)
        if hauteur_culture == HauteurCulture.HAUTE or hauteur_culture == HauteurCulture.COMPLETE:
            culturable = culturable and self.cultures_haute[row, column].travaillable and (not self.cultures_haute[row, column].culture or self.cultures_haute[row, column].culture is None or self.cultures_haute[row, column].culture == Culture.NONE)
        return culturable

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
                current = self.est_culturable(row, column, culture.hauteur_culture)
                if not current:
                    return False
            case 1|2|3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        current = self.est_culturable(row+rows, column+columns, culture.hauteur_culture)
                        if not current:
                            return False
        return True

    def initialize(self):
        for row in range(self.endX):
            for column in range(self.endY):
                self.cultures_haute[row, column] = CaseTableau()
                self.cultures_basse[row, column] = CaseTableau()
