from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from src.lackap.projet.potager.model.Culture import Culture
from src.lackap.projet.potager.view.ProductsList import ProductsList


class ProductsTable(QTableWidget):
    def __init__(self, table_rows, table_columns):
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setAcceptDrops(True)
        self.setRowCount(table_rows)
        self.setColumnCount(table_columns)
        self.viewport().installEventFilter(self)
        self.controllers = None
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(1)
        self.verticalHeader().setMinimumSectionSize(1)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def refresh(self, planches):
        for planche in planches.planches:
            for row in range(planche.start_x, planche.end_x):
                for column in range(planche.start_y, planche.end_y):
                    case_tableau = planche.cultures_basse[row-planche.start_x, column-planche.start_y]
                    if self.item(row, column):
                        self.item(row, column).setBackground(planche.cultures_basse[row-planche.start_x, column-planche.start_y].culture.color)
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
        if event.type() == QEvent.Type.MouseButtonPress:
            mouse_event = QMouseEvent(event)
            if mouse_event.buttons() == Qt.MouseButton.RightButton:
                item = self.itemAt(mouse_event.pos())
                if item:
                    if self.controllers.enlever_culture(item.row(), item.column()) is not None:
                        return True
        return False

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        # Cas d'un élément drop depuis la liste des éléments a planter
        if isinstance(widget, ProductsList):
            for widgetItem in widget.selectedItems():
                culture = Culture.get_culture(widgetItem.text(0).split()[0])
                self.controllers.placer_culture(culture, self.rowAt(pos.y()), self.columnAt(pos.x()))
        # Cas d'un élément qu'on a bougé dans le tableau
        if isinstance(widget, QTableWidget):
            for widgetItem in widget.selectedItems():
                self.controllers.deplacer_culture(widgetItem.row(), widgetItem.column(), self.rowAt(pos.y()), self.columnAt(pos.x()))
        e.accept()
