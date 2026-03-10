from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget


class ProductsList(QListWidget):
     def __init__(self):
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

     def add_culture(self, culture, nombre):
            item = QtWidgets.QListWidgetItem(self.get_label(culture, nombre))
            self.addItem(item)

     def remove_culture(self, culture):
            item = self.find_item(culture)
            self.takeItem(self.row(item))

     def update_label(self, culture, nombre):
            item = self.find_item(culture)
            if item is None:
                   self.add_culture(culture, 1)
            else:
                   item.setText(self.get_label(culture, nombre))

     def find_item(self, culture):
           for x in range(self.count()):
                  if self.item(x).text().startswith(culture.culture_type):
                         return self.item(x)

           return None

     @staticmethod
     def get_label(culture, nombre):
            return culture.culture_type + " " + str(nombre)



