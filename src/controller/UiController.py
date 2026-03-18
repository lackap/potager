from src.view.ProductsList import ProductsList
from src.view.ProductsTable import ProductsTable


class UiController:

    def __init__(self, size_x, size_y):
        self.list_a_planter = ProductsList()
        self.table = ProductsTable(size_x, size_y)
        self.list_plantes = ProductsList()
        self.list_plantes.setFixedWidth(150)

    def refresh_display(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)
        self.list_plantes.refresh(espace.list_plantes)
        self.table.refresh(espace.planches)

    def initialize(self, controllers):
        self.list_a_planter.controller = controllers
        self.table.controllers = controllers
        self.list_plantes.controller = controllers