from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget

from src.model.Culture import Culture
from src.model.TableItemType import TableItemType


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
            item = QtWidgets.QListWidgetItem(culture.type + " " + str(nombre))
            self.addItem(item)
            item.setData(TableItemType.CULTURE.value, culture)
            item.setData(TableItemType.NOMBRE_CULTURE.value, nombre)
     def remove_culture(self, culture):
            item = self.find_item(culture)
            self.takeItem(self.row(item))

     def increase_culture(self, culture):
            item = self.find_item(culture)
            if item is None:
                   self.add_culture(culture, 1)
            else:
                   nombre = item.data(TableItemType.NOMBRE_CULTURE.value)+1
                   item.setData(TableItemType.NOMBRE_CULTURE.value, nombre)
                   item.setText(culture.type + " " + str(nombre))
     def decrease_culture(self, culture):
            item = self.find_item(culture)
            if item is not None:
                   nombre = item.data(TableItemType.NOMBRE_CULTURE.value)-1
                   if nombre == 0:
                          self.remove_culture(culture)
                   else:
                          item.setData(TableItemType.NOMBRE_CULTURE.value, nombre)
                          item.setText(culture.type + " " + str(nombre))

     def find_item(self, culture):
           for x in range(self.count()):
                  if self.item(x).data(TableItemType.CULTURE.value).type == culture.type:
                         return self.item(x)

           return None


