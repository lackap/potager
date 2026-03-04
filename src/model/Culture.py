from enum import Enum

from PyQt5 import QtGui

class FamilleCulture(Enum):
    # Oignon, Poireau, Echalote
    AMARYLLIDACEE = (1, "Amaryllidacee", [4, 5])
    # Carotte Celeri Fenouil Panais
    APIACEE = (2, "Apiacee", [4, 5])
    # Choux
    BRASSICACEE = (3, "Brassicacee", [1, 2])
    # Concombre, courgette, courge, butternutt...
    CUCURBITACEE = (4, "Cucurbitacee", [9])
    # Tomate, Aubergine, piment, poivron
    SOLANACEE = (5, "Solanacee", [9])
    # Haricots, lentilles, pois
    FABACEE = (6, "Fabacee", [3, 7, 8])
    #Betterave, Epinard
    AMARANTHACEE = (7, "Amaranthacee", [1, 2])
    # Salade, Artichaud, endive, tournesol
    ASTERACEE = (8, "Astéracee", [1, 2])
    # Pdt, engrais vert
    NETTOYAGE = (9, "Solanacee", [6])

    def __init__(self, type, culture_anterieure_ok = None, culture_anterieure_ko = None):
        self.type = type
        self.culture_anterieure_ok = culture_anterieure_ok
        self.culture_anterieure_ko = culture_anterieure_ko


class Culture(Enum):
    NONE = ("", 0, QtGui.QColor(255,255,255), 3, 3)
    FRAMBOISE = ("Framboise", 3, QtGui.QColor(102,0,51))
    FRAISE = ("Fraise", 2, QtGui.QColor(255,51,51))
    OLIVIER = ("Olivier", 4, QtGui.QColor(204,255,153))
    TOMATE = ("Tomate", 3, QtGui.QColor(255,0,0), 3, 5, FamilleCulture.SOLANACEE)
    COURGETTE = ("Courgette", 3, QtGui.QColor(25,102,29), 3, 5, FamilleCulture.CUCURBITACEE)
    POMME_DE_TERRE = ("Pomme de terre", 2, QtGui.QColor(194,167,31), 4, 4, FamilleCulture.NETTOYAGE)

    def __init__(self, type, taille_necessaire, color = None, mois_semi = None, mois_plantation = None, famille = NONE):
        self.type = type
        if color is not None:
            self.color = color
        else:
            self.color = QtGui.QColor(255,255,255)
        self.taille_necessaire = taille_necessaire
        self.mois_semi = mois_semi
        self.mois_plantation = mois_plantation