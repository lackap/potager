from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget


class ProductsList(QListWidget):
     def __init__(self, data_list):
            super().__init__()
            self.setFrameShape(QtWidgets.QFrame.WinPanel)
            self.setFrameShadow(QtWidgets.QFrame.Raised)
            self.setDragEnabled(True)
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.setDefaultDropAction(QtCore.Qt.CopyAction)
            self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.setMovement(QtWidgets.QListView.Snap)
            self.setProperty("isWrapping", True)
            self.setWordWrap(True)
            self.setSortingEnabled(True)
            self.setAcceptDrops(True)
            self.data_list = data_list

     def refresh(self):
        self.clear()
        for data in self.data_list.cultures:
             item = QtWidgets.QListWidgetItem(self.get_label(data.culture, data.nombre))
             self.addItem(item)

     @staticmethod
     def get_label(culture, nombre):
            return culture.culture_type + " " + str(nombre)



