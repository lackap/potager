from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QListWidget

from src.model.Culture import Culture
from src.model.EspaceTravaillable import EspaceTravaillable
from src.model.Planche import Planches
from src.model.ProductTableItem import ProductTableItem
from src.model.TableItemType import TableItemType


class ProductsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        espace = EspaceTravaillable()
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
        self.setRowCount(espace.endX)
        self.setGeometry(300, 0, 600, 600)
        self.setColumnCount(espace.endY)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.rowHeight(10)
        self.columnWidth(10)
        self.set_fixed_elements(espace)
        self.viewport().installEventFilter(self)

    def set_liste_a_planter(self, list):
        self.liste_a_planter = list

    def set_list_plantee(self, list):
        self.list_plantee = list

    def set_fixed_elements(self, espace):
        planches = Planches()
        sizeX = 1
        while sizeX < espace.endX:
            sizeY = 1
            while sizeY < espace.endY:
                self.setItem(sizeX, sizeY, ProductTableItem(TableItemType.PRODUCT_ITEM_TYPE.value))
                self.item(sizeX, sizeY).setBackground(espace.defaultColor)
                self.item(sizeX, sizeY).setText(str(sizeX) + " " + str(sizeY))
                sizeY = sizeY + 1
            sizeX = sizeX + 1
        for planche in planches.planches:
            for count_x in range(planche.startX, planche.endX):
                for count_y in range(planche.startY, planche.endY):
                    current = self.item(count_x, count_y)
                    if current.type() == TableItemType.PRODUCT_ITEM_TYPE.value:
                        current.product = planche.ancienne_culture
                        if current.product is not None and planche.planche_fixe:
                            current.setBackground(current.product.color)
                        else:
                            current.setBackground(Culture.NONE.color)
                            current.setCulturable()

    def item(self, row, column):
        return super().item(row, column)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.RightButton:
                item = self.itemAt(event.pos())
                if item:
                    culture = item.data(TableItemType.CULTURE.value)
                    if culture:
                        self.uncolor_culture(item.row(), item.column(), culture.taille_necessaire)
                        self.list_plantee.decrease_culture(culture)
                        self.liste_a_planter.increase_culture(culture)
                        return True
        return False

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        # Cas d'un élément drop depuis la liste des éléments a planter
        if isinstance(widget, QListWidget):
            for widgetItem in widget.selectedItems():
                culture = widgetItem.data(TableItemType.CULTURE.value)
                if culture and self.check_culture(self.rowAt(pos.y()), self.columnAt(pos.x()), culture.taille_necessaire):
                    nombre_culture = widgetItem.data(TableItemType.NOMBRE_CULTURE.value)
                    if nombre_culture > 0:
                        self.color_culture(culture, self.rowAt(pos.y()), self.columnAt(pos.x()))
                        widget.decrease_culture(culture)
                        self.list_plantee.increase_culture(culture)
        # Cas d'un élément qu'on a bougé dans le tableau
        if isinstance(widget, QTableWidget):
            for widgetItem in widget.selectedItems():
                culture = widgetItem.data(TableItemType.CULTURE.value)
                if culture and self.check_culture(self.rowAt(pos.y()), self.columnAt(pos.x()), culture.taille_necessaire):
                    self.uncolor_culture(widgetItem.row(), widgetItem.column(), culture.taille_necessaire)
                    self.color_culture(culture, self.rowAt(pos.y()), self.columnAt(pos.x()))
        e.accept()

    # Colore la culture donnée dans le tableau
    # A partir de l'index
    def color_culture (self, culture, row, column):
        match culture.taille_necessaire:
            case 0:
                self.item(row, column).setBackground(Culture.NONE.color)
                self.item(row, column).setData(TableItemType.CULTURE.value, culture)
            case 1 | 2 | 3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        self.item(row + rows, column + columns).setBackground(culture.color)
                        self.item(row, column).setData(TableItemType.CULTURE.value, culture)
        self.setSpan(row, column, culture.taille_necessaire, culture.taille_necessaire)
        self.item(row, column).setText(culture.type)

    def uncolor_culture(self, row, column, size):
        for rows in range(size):
            for columns in range(size):
                self.item(row + rows, column + columns).setBackground(Culture.NONE.color)
                self.item(row, column).setData(TableItemType.CULTURE.value, Culture.NONE)
                self.item(row, column).setText("")
        self.setSpan(row, column, 1, 1)

    def check_culture(self, row, column, size):
        match size:
            case 0:
                current = self.item(row, column)
                if current.type() == TableItemType.PRODUCT_ITEM_TYPE.value:
                    if not current.culturable:
                        return False
            case 1|2|3:
                for rows in range(size):
                    for columns in range(size):
                        current = self.item(row+rows, column+columns)
                        if current.type() == TableItemType.PRODUCT_ITEM_TYPE.value:
                            if not current.culturable:
                                return False
                        else:
                            return False
        return True





