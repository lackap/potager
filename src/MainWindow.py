from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget

from src.ProductsList import ProductsList
from src.ProductsTable import ProductsTable
from src.model.Culture import Culture


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setFixedSize(1600, 1000)

        layout = QHBoxLayout()
        list_produit_a_planter = self.create_product_a_planter()
        list_produit_a_planter.setFixedWidth(150)
        # Set the central widget of the Window.
        layout.addWidget(list_produit_a_planter)

        self.table = ProductsTable()
        layout.addWidget(self.table)

        liste_produit_plantes = ProductsList()
        liste_produit_plantes.setFixedWidth(150)
        layout.addWidget(liste_produit_plantes)

        self.table.set_liste_a_planter(list_produit_a_planter)
        self.table.set_list_plantee(liste_produit_plantes)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_product_a_planter(self):
        products = ProductsList()
        products.add_culture(Culture.TOMATE, 16)
        products.add_culture(Culture.COURGETTE, 3)
        products.add_culture(Culture.POMME_DE_TERRE, 16)
        products.add_culture(Culture.FRAISE, 8)
        products.add_culture(Culture.FRAMBOISE, 2)
        return products


