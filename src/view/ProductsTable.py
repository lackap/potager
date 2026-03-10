from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidget, QListWidget, QTableWidgetItem

from src.model.Culture import Culture


class ProductsTable(QTableWidget):
    def __init__(self, controller, table_rows, table_columns):
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
        self.setRowCount(table_rows)
        self.setGeometry(300, 0, 600, 600)
        self.setColumnCount(table_columns)
        self.verticalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().setDefaultSectionSize(20)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.rowHeight(10)
        self.columnWidth(10)
        self.viewport().installEventFilter(self)
        self.controller = controller

    def add_planche(self, planche):
        sizeX = planche.startX
        while sizeX < planche.endX:
            sizeY = planche.startY
            while sizeY < planche.endY:
                self.setItem(sizeX, sizeY, QTableWidgetItem())
                current = planche.ancienne_culture
                if current is not None and planche.planche_fixe:
                    self.item(sizeX, sizeY).setBackground(current.color)
                else:
                    self.item(sizeX, sizeY).setBackground(Culture.NONE.color)
                    self.item(sizeX, sizeY).setText(str(sizeX) + " " + str(sizeY))
                sizeY = sizeY + 1
            sizeX = sizeX + 1

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.RightButton:
                item = self.itemAt(event.pos())
                if item:
                    self.controller.enlever_culture(item.row(), item.column())
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
                culture = Culture.get_culture(widgetItem.text().split()[0])
                self.controller.placer_culture(culture, self.rowAt(pos.y()), self.columnAt(pos.x()))
        # Cas d'un élément qu'on a bougé dans le tableau
        if isinstance(widget, QTableWidget):
            for widgetItem in widget.selectedItems():
                self.controller.deplacer_culture(widgetItem.row(), widgetItem.column(), self.rowAt(pos.y()), self.columnAt(pos.x()))
        e.accept()

    # Colore la culture donnée dans le tableau
    # A partir de l'index
    def color_culture (self, culture, row, column):
        match culture.taille_necessaire:
            case 0:
                self.item(row, column).setBackground(Culture.NONE.color)
            case 1 | 2 | 3:
                for rows in range(culture.taille_necessaire):
                    for columns in range(culture.taille_necessaire):
                        self.item(row + rows, column + columns).setBackground(culture.color)
        self.setSpan(row, column, culture.taille_necessaire, culture.taille_necessaire)

    def uncolor_culture(self, row, column, size):
        for rows in range(size):
            for columns in range(size):
                self.item(row + rows, column + columns).setBackground(Culture.NONE.color)
                self.item(row, column).setText("")
        self.setSpan(row, column, 1, 1)







