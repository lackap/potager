from src.lackap.projet.potager.model.CaseTableau import CaseTableau
from src.lackap.projet.potager.model.Culture import Culture
from src.lackap.projet.potager.model.Priority import Priority


class Planche(object):
    def __init__(self, name, startX, endX, startY, endY, ancienne_culture = None, planche_fixe = None):
        self.name = name
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.taille = (endX - startX) * (endY - startY)
        self.ancienne_culture = ancienne_culture
        self.planche_fixe = planche_fixe
        self.cultures = {}
        self.initialize()

    def initialize(self):
        for row in range(self.endX-self.startX):
            for column in range(self.endY-self.startY):
                self.cultures[row, column] = CaseTableau()

    def is_plantable(self,culture):
        return culture.plantable_apres(self.ancienne_culture)

    def set_culture_start(self, row, column, is_start):
        self.cultures[row-self.startX, column-self.startY].init_culture = is_start

    def add_culture(self, row, column, culture):
        self.cultures[row-self.startX, column-self.startY].culture = culture

    def has_culture(self):
        for row in range(self.endX-self.startX):
            for column in range(self.endY-self.startY):
                if self.cultures[row, column].culture is not Culture.NONE:
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
        temporary_cultures = {}
        for row in range(self.endX-self.startX):
            for column in range(self.endY-self.startY):
                temporary_cultures[row, column] = self.cultures[row, column].culture
        count = 0
        count_total = 0
        for culture_for_list in cultures_associees.cultures:
            count = count + self.can_plant(culture_for_list.culture, culture_for_list.nombre, temporary_cultures)
            count_total = count_total + culture_for_list.nombre
        return count == count_total


    def can_plant(self, culture, nombre, temporary_cultures=None):
        if temporary_cultures is None:
            temporary_cultures = {}
            for row in range(self.endX-self.startX):
                for column in range(self.endY-self.startY):
                    temporary_cultures[row, column] = self.cultures[row, column].culture
        count = 0
        for count in range(nombre):
            size_x = self.endX-self.startX
            size_y = self.endY-self.startY
            if not self.check_plant_iteration(size_x, size_y, culture, temporary_cultures):
                return count
            else:
                count = count + 1
        return count

    def check_plant_iteration(self, size_x, size_y, culture, temporary_cultures):
        for row in range(size_x-culture.taille_necessaire+1):
            for column in range(size_y-culture.taille_necessaire+1):
                if self.check_plant_cell(row, column, culture.taille_necessaire, culture, temporary_cultures):
                    return True
        return False

    def check_plant_cell(self, row, column, taille, culture, temporary_cultures):
        for rows in range(taille):
            for columns in range(taille):
                if temporary_cultures[row+rows, column+columns] is not None and temporary_cultures[row+rows, column+columns] is not Culture.NONE :
                    return False
                else:
                    temporary_cultures[row+rows, column+columns] = culture
        return True

    def validate_association(self, culture):
        for row in range(self.endX-self.startX):
            for column in range(self.endY-self.startY):
                if not self.cultures[row, column] == Culture.NONE and not self.cultures[row, column].culture.associable(culture):
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
        self.planches = {self.plancheFraise, self.plancheFramboise, self.plancheOlivier, self.plancheGauche,
                        self.plancheCentreHaut,self.plancheCentreBasse,self.plancheBasse, self.plancheDroite,
                         self.carre1,self.carre2,self.carre3, self.carre4}

    def find_planche(self, row, column):
        for planche in self.planches:
            if planche.startX <= row <= planche.endX:
                if planche.startY <= column <= planche.endY:
                    return planche
        return None
