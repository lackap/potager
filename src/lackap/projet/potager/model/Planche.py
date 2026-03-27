from src.lackap.projet.potager.model.CaseTableau import CaseTableau
from src.lackap.projet.potager.model.Culture import Culture, HauteurCulture
from src.lackap.projet.potager.model.Priority import Priority


def check_plant_cell(row, column, taille, culture, temporary_cultures):
    for rows in range(taille):
        for columns in range(taille):
            if temporary_cultures[row+rows, column+columns] is not None and temporary_cultures[row+rows, column+columns] is not Culture.NONE :
                return False
            else:
                temporary_cultures[row+rows, column+columns] = culture
    return True


def check_plant_iteration(size_x, size_y, culture, temporary_cultures_haute, temporary_cultures_basse):
    for row in range(size_x-culture.taille_necessaire+1):
        for column in range(size_y-culture.taille_necessaire+1):
            if culture.hauteur_culture == HauteurCulture.BASSE:
                if check_plant_cell(row, column, culture.taille_necessaire, culture, temporary_cultures_basse):
                    return True
            if culture.hauteur_culture == HauteurCulture.HAUTE:
                if check_plant_cell(row, column, culture.taille_necessaire, culture, temporary_cultures_haute):
                    return True
            if culture.hauteur_culture == HauteurCulture.COMPLETE:
                if check_plant_cell(row, column, culture.taille_necessaire, culture, temporary_cultures_haute) and check_plant_cell(row, column, culture.taille_necessaire, culture, temporary_cultures_basse):
                    return True
    return False


class Planche(object):
    def __init__(self, name, start_x, end_x, start_y, end_y, ancienne_culture = None, planche_fixe = None):
        self.name = name
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.taille = (end_x - start_x) * (end_y - start_y)
        self.ancienne_culture = ancienne_culture
        self.planche_fixe = planche_fixe
        self.cultures_basse = {}
        self.cultures_haute = {}
        self.initialize()

    def initialize(self):
        for row in range(self.end_x-self.start_x):
            for column in range(self.end_y-self.start_y):
                self.cultures_basse[row, column] = CaseTableau()
                self.cultures_haute[row, column] = CaseTableau()

    def is_plantable(self,culture):
        return culture.plantable_apres(self.ancienne_culture)

    def set_culture_start(self, row, column, is_start, hauteur_culture):
        if hauteur_culture == HauteurCulture.BASSE or hauteur_culture == HauteurCulture.COMPLETE:
            self.cultures_basse[row-self.start_x, column-self.start_y].init_culture = is_start
        if hauteur_culture == HauteurCulture.HAUTE or hauteur_culture == HauteurCulture.COMPLETE:
            self.cultures_haute[row-self.start_x, column-self.start_y].init_culture = is_start

    def add_culture(self, row, column, culture):
        if culture.hauteur_culture == HauteurCulture.BASSE or culture.hauteur_culture == HauteurCulture.COMPLETE:
            self.cultures_basse[row-self.start_x, column-self.start_y].culture = culture
        if culture.hauteur_culture == HauteurCulture.HAUTE or culture.hauteur_culture == HauteurCulture.COMPLETE:
            self.cultures_haute[row-self.start_x, column-self.start_y].culture = culture

    def has_culture(self, ):
        for row in range(self.end_x-self.start_x):
            for column in range(self.end_y-self.start_y):
                if self.cultures_haute[row, column].culture is not Culture.NONE or self.cultures_basse[row, column].culture is not Culture.NONE:
                    return True
        return False

    def get_priority(self, culture, nombre, optimized):
        priority = Priority(0,0)
        if not optimized or self.is_plantable(culture):
            priority.level = priority.level + 1
        if priority.level >= 1 and self.can_plant(culture, 1):
            priority.level = priority.level + 1
        else:
            priority.level = 0
        if priority.level >= 2:
            count = self.can_plant(culture, nombre)
            priority.level = priority.level + 1
            priority.nombre = count
        if priority.level >= 3:
            if self.validate_association(culture):
                priority.level = priority.level + 2
            else:
                if not self.has_culture():
                    priority.level = priority.level + 1
        return priority

    def can_plant_all(self, cultures_associees):
        temporary_cultures_haute = {}
        temporary_cultures_basse = {}
        for row in range(self.end_x-self.start_x):
            for column in range(self.end_y-self.start_y):
                temporary_cultures_haute[row, column] = self.cultures_haute[row, column].culture
                temporary_cultures_basse[row, column] = self.cultures_basse[row, column].culture
        count = 0
        count_total = 0
        for culture_for_list in cultures_associees.cultures:
            count = count + self.can_plant(culture_for_list.culture, culture_for_list.nombre, temporary_cultures_haute, temporary_cultures_basse)
            count_total = count_total + culture_for_list.nombre
        return count == count_total


    def can_plant(self, culture, nombre, temporary_cultures_haute=None,  temporary_cultures_basse=None):
        if temporary_cultures_haute is None:
            temporary_cultures_haute = {}
            temporary_cultures_basse = {}
            for row in range(self.end_x-self.start_x):
                for column in range(self.end_y-self.start_y):
                    temporary_cultures_haute[row, column] = self.cultures_haute[row, column].culture
                    temporary_cultures_basse[row, column] = self.cultures_basse[row, column].culture
        count = 0
        for count in range(nombre):
            size_x = self.end_x-self.start_x
            size_y = self.end_y-self.start_y
            if not check_plant_iteration(size_x, size_y, culture, temporary_cultures_haute, temporary_cultures_basse):
                return count
            else:
                count = count + 1
        return count

    def validate_association(self, culture):
        for row in range(self.end_x-self.start_x):
            for column in range(self.end_y-self.start_y):
                if (not self.cultures_haute[row, column] == Culture.NONE and not self.cultures_haute[row, column].culture.associable(culture))\
                        or (not self.cultures_basse[row, column] == Culture.NONE and not self.cultures_basse[row, column].culture.associable(culture)):
                    return False
        return True



class Planches(object):
    def __init__(self):
        self.plancheFramboise = Planche("Framboise", 4, 6, 15, 22, Culture.FRAMBOISE, True)
        self.plancheFraise = Planche("Fraise", 9, 13, 12, 25, Culture.FRAISE, True)
        self.plancheOlivier = Planche("Olivier", 8, 12, 29, 32, Culture.OLIVIER, True)
        self.plancheGauche = Planche("Gauche", 20, 34, 5, 9, Culture.TOMATE, False)
        self.plancheCentreHaut = Planche("Centre haut", 16, 21, 12, 29, Culture.COURGETTE, False)
        self.plancheCentreBasse = Planche("Centre bas", 24, 29, 12, 29, Culture.POMME_DE_TERRE, False)
        self.plancheBasse = Planche("Basse", 32, 38, 12, 29, Culture.TOMATE, False)
        self.plancheDroite = Planche("Droite", 24, 29, 40, 52, Culture.NONE, False)
        self.carre1 = Planche("Carre1", 16, 21, 32, 37, Culture.NONE, False)
        self.carre2 = Planche("Carre2", 24, 29, 32, 37, Culture.NONE,False)
        self.carre3 = Planche("Carre3", 32, 37, 32, 37, Culture.NONE,False)
        self.carre4 = Planche("Carre4", 40, 45, 32, 37, Culture.NONE,False)
        self.planches = []

    def find_planche(self, row, column):
        for planche in self.planches:
            if planche.start_x <= row <= planche.end_x:
                if planche.start_y <= column <= planche.end_y:
                    return planche
        return None

    def clear(self):
        self.planches.clear()