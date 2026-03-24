from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidget, QTreeView, QTreeWidget, QTreeWidgetItem


class ProductsList(QTreeWidget):
     def __init__(self):
            super().__init__()
            self.setFrameShape(QtWidgets.QFrame.WinPanel)
            self.setFrameShadow(QtWidgets.QFrame.Raised)
            self.setDragEnabled(True)
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.setDefaultDropAction(QtCore.Qt.CopyAction)
            self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.setSortingEnabled(True)
            self.setAcceptDrops(True)
            self.header().setVisible(False)
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.menuContextTree)
            self.controllers = None


     def refresh(self, data_list):
        self.clear()
        root = QTreeWidgetItem(None, ["Cultures"])
        self.insertTopLevelItem(0, root)
        for data in data_list.cultures:
            inserted = False
            for index in range(root.childCount()):
                famille = root.child(index)
                if famille.text(0) == data.culture.famille.culture_name:
                    famille.addChild(QTreeWidgetItem(None, [self.get_label(data)]))
                    inserted = True
                    break
            if not inserted:
                famille = QTreeWidgetItem(None, [data.culture.famille.culture_name])
                famille.addChild(QTreeWidgetItem(None,  [self.get_label(data)]))
                root.addChild(famille)
        self.expandAll()

     def dropEvent(self, e):
        e.accept()

     @staticmethod
     def get_label(culture_list):
            return culture_list.culture.culture_type + " " + str(culture_list.nombre) + ", " + str(culture_list.nombre_plantes) + " plantés."

     def menuContextTree(self, point):
         index = self.indexAt(point)
         menu = QtWidgets.QMenu()
         if index.isValid():
             menu.addSeparator()
             action_ajout = menu.addAction("Ajouter 1 ")
             action_ajout.triggered.connect(lambda: self.ajouter_culture(index))
             action_retrait = menu.addAction("Enlever 1")
             action_retrait.triggered.connect(self.enlever_culture)
         action_manage = menu.addAction("Gerer mes cultures")
         action_manage.triggered.connect(self.switch_to_view)
         menu.exec_(self.mapToGlobal(point))

     def ajouter_culture(self, index):
        self.controllers.espace_controller.espace.self.itemFromIndex(index).text(0)

     def enlever_culture(self, index):
         self.controllers.self.itemFromIndex(index).text(0)

     def switch_to_view(self):
         self.parent().parent().switch_to_view(1)



