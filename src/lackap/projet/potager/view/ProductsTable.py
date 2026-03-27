from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QMouseEvent, QColor
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

from src.lackap.projet.potager.model.Culture import Culture, HauteurCulture
from src.lackap.projet.potager.view.AddPlancheDialog import AddPlancheDialog
from src.lackap.projet.potager.view.ProductsList import ProductsList


class ProductsTable(QTableWidget):
    def __init__(self, table_rows, table_columns):
        super().__init__()
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
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
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuContextTree)

    def reset_view(self, espace):
        for x in range(espace.endX):
            for y in range(espace.endY):
                self.setSpan(x, y, 1, 1)
                if self.item(x, y):
                    self.item(x, y).setText("")
                    self.item(x, y).setBackground(QColor(255, 255, 255))

    def refresh(self, planches, display_level):
        for planche in planches.planches:
            for row in range(planche.start_x, planche.end_x):
                for column in range(planche.start_y, planche.end_y):
                    if display_level == HauteurCulture.BASSE:
                        case_tableau = planche.cultures_basse[row - planche.start_x, column - planche.start_y]
                    else:
                        case_tableau = planche.cultures_haute[row - planche.start_x, column - planche.start_y]

                    if self.item(row, column):
                        self.item(row, column).setBackground(case_tableau.culture.color)
                        if case_tableau.culture == Culture.NONE:
                            self.setSpan(row, column, 1, 1)
                            self.item(row, column).setText("")
                    else:
                        self.setItem(row, column, QTableWidgetItem())
                        self.item(row, column).setBackground(case_tableau.culture.color)

                    if case_tableau.init_culture is None:
                        self.setSpan(row, column, 1, 1)
                        self.item(row, column).setText("")
                        case_tableau.init_culture = False
                    if case_tableau.init_culture:
                        taille = case_tableau.culture.taille_necessaire
                        self.item(row, column).setText(case_tableau.culture.culture_type)
                        self.setSpan(row, column, taille, taille)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            mouse_event = event
            if mouse_event.buttons() == Qt.MouseButton.RightButton:
                item = self.itemAt(mouse_event.pos())
                if item:
                    if self.controllers.enlever_culture(item.row(), item.column()) is not None:
                        return True
                else:
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
                self.controllers.deplacer_culture(widgetItem.row(), widgetItem.column(), self.rowAt(pos.y()),
                                                  self.columnAt(pos.x()))
        e.accept()

    def menuContextTree(self, point):
        index = self.indexAt(point)
        menu = QtWidgets.QMenu()
        if index.isValid():
            menu.addSeparator()
            action_ajout = menu.addAction("Ajouter une planche")
            action_ajout.triggered.connect(self.add_planche)
            action_retrait = menu.addAction("Enlever 1")
        action_manage = menu.addAction("Gerer mes cultures")
        menu.exec(self.mapToGlobal(point))

    def add_planche(self):

        planche_dialog = AddPlancheDialog(self.window())
        if planche_dialog.exec():
            self.controllers.add_planche_by_values(planche_dialog.planche_name.text(),
                                                   int(planche_dialog.start_x.text()),
                                                   int(planche_dialog.start_y.text()), int(planche_dialog.end_x.text()),
                                                   int(planche_dialog.end_y.text()))
            print("Success!")
        else:
            print("Cancel!")
