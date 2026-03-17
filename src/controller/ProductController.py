from src.model.Culture import Culture
from src.model.EspaceTravaillable import EspaceTravaillable
from src.view.ProductsList import ProductsList
from src.view.ProductsTable import ProductsTable


class ProductController:

    def __init__(self):
        self.espace = EspaceTravaillable()
        self.list_a_planter = ProductsList(self.espace.list_a_planter)
        self.list_a_planter.setFixedWidth(150)
        self.table = ProductsTable(self, self.espace.endX, self.espace.endY)
        self.list_plantes = ProductsList(self.espace.list_plantes)
        self.list_plantes.setFixedWidth(150)
        self.initialize()
        self.refreshDisplay()

    def refreshDisplay(self):
        self.list_a_planter.refresh()
        self.list_plantes.refresh()
        self.table.refresh()

    def add_planche(self, planche):
        self.espace.add_planche(planche)

    def add_culture(self, culture, nombre):
        self.espace.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column):
        if self.espace.can_insert_culture(row, column, culture) and self.espace.list_a_planter.find_culture_number(culture) > 0:
            self.espace.placer_culture(culture, row, column)
            self.refreshDisplay()

    def deplacer_culture(self, rowinit, columninit, row, column):
        if self.espace.can_insert_culture(row, column, self.espace.get_culture(rowinit, columninit)):
            culture = self.espace.deplacer_culture(rowinit, columninit, row, column)
            self.refreshDisplay()

    def enlever_culture(self, row, column):
        culture = self.espace.enlever_culture(row, column)
        self.refreshDisplay()

    def auto_fill(self):
        optimized = True
        cultures_associees = self.espace.list_a_planter.grouper_culture_associable()
        for cultures_associee in cultures_associees:
            for planche in self.espace.planches.planches:
                if planche.can_plant_all(cultures_associee):
                    for culture_associee in cultures_associee.cultures:
                        self.inserer_cultures_planche(planche, culture_associee.culture, culture_associee.nombre)
                    break
        for i in range(2):
            for culture_list in self.espace.list_a_planter.cultures:
                culture = culture_list.culture
                nombre = culture_list.nombre
                for count in range(nombre):
                    planche = self.espace.find_meilleure_planche(culture, nombre, optimized)
                    if planche is not None and self.inserer_cultures_planche(planche, culture, nombre):
                        break
                    #else:
                    #    print("Aucune planche trouvée pour la culture " + culture.culture_type)
            optimized = False

    def inserer_cultures_planche(self, planche, culture, nombre):
            for count in range(nombre):
                if not self.inserer_culture_planche(planche, culture):
                    return False
            return True

    def inserer_culture_planche(self, planche, culture):
        for row in range(planche.startX, planche.endX):
            for column in range(planche.startY, planche.endY):
                if self.espace.can_insert_culture(row, column, culture):
                    self.placer_culture(culture, row, column)
                    #print(culture.culture_type + " inséré sur la planche " + planche.name)
                    return True
        return False

    def initialize(self):
        self.list_a_planter.controller = self
        self.table.controller = self
        self.list_plantes.controller = self
        self.add_culture(Culture.TOMATE, 16)
        self.add_culture(Culture.COURGETTE, 4)
        self.add_culture(Culture.POMME_DE_TERRE, 20)
        self.add_culture(Culture.POIREAU, 25)
        self.add_culture(Culture.CAROTTE, 25)
        self.add_culture(Culture.OIGNON, 15)

        for planche in self.espace.planches.planches:
            self.add_planche(planche)

        self.refreshDisplay()


