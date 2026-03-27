from src.lackap.projet.potager.view.ProductsList import ProductsList
from src.lackap.projet.potager.view.ProductsTable import ProductsTable


class UiController:

    def __init__(self, size_x, size_y):
        self.list_a_planter = ProductsList()
        self.table = ProductsTable(size_x, size_y)

    def refresh_display(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)
        self.table.refresh(espace.planches)

    def refresh_list(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)

    def refresh_table(self,espace):
        self.table.refresh(espace.planches)

    def switch_level(self, espace):
        self.table.switch_level()
        self.table.refresh(espace.planches)

    def initialize(self, controllers):
        self.list_a_planter.controllers = controllers
        self.table.controllers = controllers