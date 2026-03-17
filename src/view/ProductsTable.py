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

    def refresh(self):
        for planche in self.controller.espace.planches.planches:
            for row in range(planche.startX, planche.endX):
                for column in range(planche.startY, planche.endY):
                    case_tableau = planche.cultures[row-planche.startX, column-planche.startY]
                    if self.item(row, column):
                        self.item(row, column).setBackground(planche.cultures[row-planche.startX, column-planche.startY].culture.color)
                    else:
                        self.setItem(row, column, QTableWidgetItem())
                        self.item(row, column).setBackground(case_tableau.culture.color)
                    init_culture = case_tableau.init_culture
                    if init_culture is None:
                        self.setSpan(row, column, 1, 1)
                        self.item(row, column).setText("")
                        case_tableau.init_culture = False
                    if init_culture:
                        taille = case_tableau.culture.taille_necessaire
                        self.item(row, column).setText(case_tableau.culture.culture_type)
                        self.setSpan(row, column, taille, taille)

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
