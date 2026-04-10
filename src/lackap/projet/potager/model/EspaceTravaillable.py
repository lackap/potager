
from src.lackap.projet.potager.model.CaseTableau import CaseTableau
from src.lackap.projet.potager.model.Culture import Culture, HauteurCulture
from src.lackap.projet.potager.model.ListCulture import ListCulture
from src.lackap.projet.potager.model.Planche import Planches
from src.lackap.projet.potager.model.Priority import Priority


class EspaceTravaillable(object):
    def __init__(self):
        self.endX = 60
        self.endY = 60
        self.cultures_haute = {}
        self.cultures_basse = {}
        self.list_a_planter = ListCulture()
        self.initialize()
        self.planches = Planches()

    def clear(self):
        self.cultures_haute.clear()
        self.cultures_basse.clear()
        self.planches.clear()
        self.list_a_planter.clear()
        self.initialize()

    def add_planche(self,planche):
        for row in range(planche.start_x, planche.end_x):
            for column in range(planche.start_y, planche.end_y):
                self.cultures_haute[row,column].travaillable = True
                self.cultures_basse[row,column].travaillable = True
                if planche.planche_fixe:
                    planche.add_culture(row, column, planche.ancienne_culture)
                else:
                    planche.add_culture(row, column, Culture.NONE)
        self.planches.planches.append(planche)

    def add_culture(self, culture, nombre):
        self.list_a_planter.add_culture(culture, nombre)

    def update_culture_number(self, culture, nombre):
        self.list_a_planter.update_culture_number(culture, nombre)

    def placer_culture(self, culture, row, column):
        self.list_a_planter.decrease_culture(culture)
        match culture.taille_necessaire:
            case 0:
                self.cultures_haute[row, column].culture = Culture.NONE
                self.cultures_basse[row, column].culture = Culture.NONE
            case 1 | 2 | 3:

                for rowindex in range(row, row+culture.taille_necessaire):
                    for columnindex in range(column, column+culture.taille_necessaire):
                        if culture.hauteur_culture == HauteurCulture.BASSE or culture.hauteur_culture == HauteurCulture.COMPLETE:
                            self.cultures_basse[rowindex, columnindex].culture = culture
                        if culture.hauteur_culture == HauteurCulture.HAUTE or culture.hauteur_culture == HauteurCulture.COMPLETE:
                            self.cultures_haute[rowindex, columnindex].culture = culture
                        self.planches.find_planche(rowindex, columnindex).add_culture(rowindex, columnindex, culture)
                self.planches.find_planche(row, column).set_culture_start(row, column, True, culture.hauteur_culture)

        return culture

    def enlever_culture(self, row, column, display_level):
        if display_level == HauteurCulture.BASSE:
            culture = self.cultures_basse[row, column].culture
        else:
            culture = self.cultures_haute[row, column].culture

        if culture is not None and not culture == Culture.NONE and culture.hauteur_culture == HauteurCulture.BASSE:
            self.enlever_culture_hauteur(row, column, culture, self.cultures_basse)
            self.list_a_planter.increase_culture(culture)
        if culture is not None and not culture == Culture.NONE and culture.hauteur_culture == HauteurCulture.HAUTE:
            self.enlever_culture_hauteur(row, column, culture, self.cultures_haute)
            self.list_a_planter.increase_culture(culture)
        if culture is not None and not culture == Culture.NONE and culture.hauteur_culture == HauteurCulture.COMPLETE:
            self.enlever_culture_hauteur(row, column, culture, self.cultures_basse)
            self.enlever_culture_hauteur(row, column, culture, self.cultures_haute)
            self.list_a_planter.increase_culture(culture)

    def enlever_culture_hauteur(self, row, column, culture, cultures):
        if culture is not None and not culture == Culture.NONE:
            match culture.taille_necessaire:
                case 0:
                    self.cultures_haute[row, column].culture = Culture.NONE
                case 1 | 2 | 3:
                    for rowindex in range(row, row+culture.taille_necessaire):
                        for columnindex in range(column, column+culture.taille_necessaire):
                            cultures[rowindex,columnindex].culture = Culture.NONE
                            self.planches.find_planche(rowindex, columnindex).set_culture_start(rowindex, columnindex, None, culture.hauteur_culture)
                            self.planches.find_planche(rowindex, columnindex).add_culture(rowindex, columnindex, Culture.NONE)


    def deplacer_culture(self, rowinit, columninit, row, column, display_level):
        if display_level == HauteurCulture.BASSE:
            culture = self.cultures_basse[rowinit, columninit].culture
        else:
            culture = self.cultures_haute[rowinit, columninit].culture
        self.enlever_culture(rowinit, columninit, display_level)
        if display_level == HauteurCulture.BASSE:
            self.placer_culture(culture, row, column)
        if display_level == HauteurCulture.HAUTE:
            self.placer_culture(culture, row, column)

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
