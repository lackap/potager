from PyQt5 import QtGui

from src.model.Culture import Culture


class Planche(object):
    def __init__(self, startX, endX, startY, endY, ancienne_culture = None, planche_fixe = None):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.taille = (endX - startX) * (endY - startY)
        self.ancienne_culture = ancienne_culture
        self.planche_fixe = planche_fixe

class Planches(object):
    def __init__(self):
        self.plancheFramboise = Planche(4, 6, 15, 22, Culture.FRAMBOISE, True)
        self.plancheFraise = Planche(9, 13, 12, 25, Culture.FRAISE, True)
        self.plancheOlivier = Planche(8, 12, 29, 32, Culture.OLIVIER, True)
        self.plancheGauche = Planche(20, 34, 6, 9, Culture.TOMATE, False)
        self.plancheCentreHaut = Planche(16, 21, 12, 29, Culture.COURGETTE, False)
        self.plancheCentreBasse = Planche(24, 29, 12, 29, Culture.POMME_DE_TERRE, False)
        self.plancheBasse = Planche(32, 38, 12, 29, Culture.TOMATE, False)
        self.plancheDroite = Planche(24, 29, 40, 52, Culture.NONE, False)
        self.carre1 = Planche(16, 21, 32, 37, False)
        self.carre2 = Planche(24, 29, 32, 37, False)
        self.carre3 = Planche(32, 37, 32, 37, False)
        self.carre4 = Planche(40, 45, 32, 37, False)
        self.planches = {self.plancheFramboise,self.plancheFraise,self.plancheOlivier,self.plancheGauche,
                         self.plancheCentreHaut,self.plancheCentreBasse,self.plancheBasse, self.plancheDroite,
                         self.carre1,self.carre2,self.carre3, self.carre4}