from src.lackap.projet.potager.model.Culture import HauteurCulture
from src.lackap.projet.potager.view.ProductsList import ProductsList
from src.lackap.projet.potager.view.ProductsTable import ProductsTable


class UiController:

    def __init__(self, size_x, size_y):
        self.list_a_planter = ProductsList()
        self.table = ProductsTable(size_x, size_y)
        self.display_level = HauteurCulture.BASSE

    def refresh_display(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)
        self.table.reset_view(espace)
        self.table.refresh(espace.planches, self.display_level)

    def refresh_list(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)

    def refresh_table(self,espace):
        self.table.reset_view(espace)
        self.table.refresh(espace.planches, self.display_level)

    def switch_level(self, espace):
        if self.display_level == HauteurCulture.BASSE:
            self.display_level = HauteurCulture.HAUTE
        else:
            self.display_level = HauteurCulture.BASSE
        self.refresh_table(espace)

    def initialize(self, controllers):
        self.list_a_planter.controllers = controllers
        self.table.controllers = controllers