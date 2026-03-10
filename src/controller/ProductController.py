from src.model.Culture import Culture
from src.model.EspaceTravaillable import EspaceTravaillable
from src.model.Planche import Planches
from src.view.ProductsList import ProductsList
from src.view.ProductsTable import ProductsTable


class ProductController:

    def __init__(self):
        self.espace = EspaceTravaillable()
        self.list_a_planter = ProductsList()
        self.list_a_planter.setFixedWidth(150)
        self.table = ProductsTable(self, self.espace.endX, self.espace.endY)
        self.list_plantes = ProductsList()
        self.list_plantes.setFixedWidth(150)
        self.espace = EspaceTravaillable()
        self.initialize()


    def add_planche(self, planche):
        self.espace.add_planche(planche)
        self.table.add_planche(planche)

    def add_culture(self, culture, nombre):
        self.list_a_planter.add_culture(culture, nombre)
        self.espace.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column):
        if self.check_culture(row, column, culture):
            self.espace.placer_culture(culture, row, column)
            self.table.color_culture(culture, row, column)
            self.list_plantes.update_label(culture, self.espace.list_plantes.find_culture_number(culture))
            self.list_a_planter.update_label(culture, self.espace.list_a_planter.find_culture_number(culture))

    def deplacer_culture(self, rowinit, columninit, row, column):
        if self.check_culture(row, column, self.espace.get_culture(rowinit, columninit)):
            culture = self.espace.deplacer_culture(rowinit, columninit, row, column)
            self.table.uncolor_culture(rowinit, columninit,culture.taille_necessaire)
            self.table.color_culture(culture, row, column)

    def enlever_culture(self, row, column):
        culture = self.espace.enlever_culture(row, column)
        self.table.uncolor_culture(row, column, culture.taille_necessaire)
        self.list_plantes.update_label(culture, self.espace.list_plantes.find_culture_number(culture))
        self.list_a_planter.update_label(culture, self.espace.list_a_planter.find_culture_number(culture))

    def check_culture(self, row, column, culture):
        match culture.taille_necessaire:
            case 0:
                current = self.espace.est_culturable(row, column)
                if not current:
                        return False
            case 1|2|3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        current = self.espace.est_culturable(row+rows, column+columns)
                        if not current:
                            return False
        return True

    def auto_fill(self):
        for culture_list in self.espace.list_a_planter.cultures:
            culture = culture_list.culture
            nombre = culture_list.nombre
            planches = Planches()
            for count in range(nombre):
                for planche in planches.planches:
                    print("On essaie d'insérer la valeur " + culture.culture_type + " dans la planche " + planche.name)
                    if self.inserer_culture_planche(planche, culture):
                        break


    def inserer_culture_planche(self, planche, culture):
        if planche.is_plantable(culture):
            for row in range(planche.startX, planche.endX):
                for column in range(planche.startY, planche.endY):
                    print("On check si on peut insérer sur la planche en position " + str(row) + " / " + str(column))
                    if self.check_culture(row, column, culture):
                        print("On insère la culture " + culture.culture_type + " dans la planche " + planche.name + " en position " + str(row) + " / " + str(column))
                        self.placer_culture(culture, row, column)
                        return True
        return False

    def initialize(self):
        self.list_a_planter.controller = self
        self.table.controller = self
        self.list_plantes.controller = self
        self.add_culture(Culture.TOMATE, 16)
        self.add_culture(Culture.COURGETTE, 5)
        self.add_culture(Culture.POMME_DE_TERRE, 15)
        self.add_culture(Culture.CAROTTE, 25)
        self.add_culture(Culture.POIREAU, 25)
        self.add_culture(Culture.OIGNON, 15)

        planches = Planches()
        for planche in planches.planches:
            self.add_planche(planche)


