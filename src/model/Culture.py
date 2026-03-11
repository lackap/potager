from enum import Enum

from PyQt5 import QtGui

class FamilleCulture(Enum):
    # Oignon, Poireau, Echalote
    AMARYLLIDACEE = (1, "Amaryllidacee", [4, 5, 11], [1, 2])
    # Carotte Celeri Fenouil Panais
    APIACEE = (2, "Apiacee", [4, 5, 11], [1, 2])
    # Choux
    BRASSICACEE = (3, "Brassicacee", [1, 2, 11])
    # Concombre, courgette, courge, butternutt...
    CUCURBITACEE = (4, "Cucurbitacee", [9, 11])
    # Tomate, Aubergine, piment, poivron
    SOLANACEE = (5, "Solanacee", [9, 11])
    # Haricots, lentilles, pois
    FABACEE = (6, "Fabacee", [3, 7, 8, 11])
    #Betterave, Epinard
    AMARANTHACEE = (7, "Amaranthacee", [1, 2, 11])
    # Salade, Artichaud, endive, tournesol
    ASTERACEE = (8, "Astéracee", [1, 2, 11])
    # Pdt, engrais vert
    NETTOYAGE = (9, "Solanacee", [6, 11])
    # Famille des éléments fixes
    FIXE = (10, "Fixe", [])
    # Famille pour le rien, on peut tout planter
    RIEN = (11, "Aucune", [1, 2, 3, 4, 5, 6, 7, 8, 9], [])

    def __init__(self, culture_type, culture_name, culture_anterieure_ok = None, culture_associable = None):
        self.culture_type = culture_type
        self.culture_name = culture_name
        self.culture_anterieure_ok = culture_anterieure_ok
        self.culture_associable = culture_associable

    def is_associable(self, famille):
        if self.culture_associable is not None and famille is not FamilleCulture.RIEN and famille.culture_type in self.culture_associable:
            return True
        return False

    def is_plantable_apres(self, famille):
        if self.culture_anterieure_ok is not None and famille in self.culture_anterieure_ok:
            return True
        return False



class Culture(Enum):
    NONE = ("", 0, QtGui.QColor(128,128,128), 3, 3, FamilleCulture.RIEN)
    FRAMBOISE = ("Framboise", 3, QtGui.QColor(102,0,51), 0, 0, FamilleCulture.FIXE)
    FRAISE = ("Fraise", 2, QtGui.QColor(255,51,51), 0, 0, FamilleCulture.FIXE)
    OLIVIER = ("Olivier", 4, QtGui.QColor(204,255,153), 0, 0, FamilleCulture.FIXE)
    TOMATE = ("Tomate", 3, QtGui.QColor(255,0,0), 3, 5, FamilleCulture.SOLANACEE)
    COURGETTE = ("Courgette", 3, QtGui.QColor(25,102,29), 3, 5, FamilleCulture.CUCURBITACEE)
    POMME_DE_TERRE = ("Pdt", 2, QtGui.QColor(194,167,31), 4, 4, FamilleCulture.NETTOYAGE)
    POIREAU = ("Poireau", 1, QtGui.QColor(76, 166, 107), 3, 3, FamilleCulture.AMARYLLIDACEE)
    OIGNON = ("Oignon", 1, QtGui.QColor(213,132,144), 3, 3, FamilleCulture.AMARYLLIDACEE)
    CAROTTE = ("Carotte", 1, QtGui.QColor(244,102,27), 3, 3, FamilleCulture.APIACEE)

    def __init__(self, culture_type, taille_necessaire, color = None, mois_semi = None, mois_plantation = None, famille = None):
        self.culture_type = culture_type
        if color is not None:
            self.color = color
        else:
            self.color = QtGui.QColor(255,255,255)
        self.taille_necessaire = taille_necessaire
        self.mois_semi = mois_semi
        self.mois_plantation = mois_plantation
        self.famille = famille

    def plantable_apres(self, ancienne_culture):
        if not ancienne_culture or ancienne_culture is None or self.famille.is_plantable_apres(ancienne_culture.famille.culture_type):
            return True
        else:
            return False

    def associable(self, culture_associee):
        if not culture_associee or culture_associee is None or culture_associee.famille.is_associable(self.famille):
            return True
        else:
            return False

    @staticmethod
    def get_culture(culture_type):
        for culture in Culture:
            if culture.culture_type == culture_type:
                return culture
        return None