from PyQt5.QtWidgets import QTableWidgetItem


class ProductTableItem(QTableWidgetItem):
    def __init__(self, type, culture = None):
        super().__init__(type)
        self.product = culture
        self.culturable = False

    def setCulturable(self):
        self.culturable = True