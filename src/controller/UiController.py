from src.view.ProductsList import ProductsList
from src.view.ProductsTable import ProductsTable


class UiController:

    def __init__(self, size_x, size_y):
        self.list_a_planter = ProductsList()
        self.table = ProductsTable(size_x, size_y)

    def refresh_display(self, espace):
        self.list_a_planter.refresh(espace.list_a_planter)
        self.table.refresh(espace.planches)

    def initialize(self, controllers):
        self.list_a_planter.controllers = controllers
        self.table.controllers = controllers