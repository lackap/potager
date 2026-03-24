from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from src.controller.ProductController import ProductController
from src.controller.UiController import UiController
from src.view.DisplayCultureWidget import DisplayCultureWidget
from src.view.ManageCultureWidget import ManageCultureWidget


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SuperPopo")
        self.setWindowIcon(QtGui.QIcon('resources/icons/carrot.png'))
        self.controllers = ProductController()

        self.setCentralWidget(DisplayCultureWidget(self))

    def switch_to_view(self, index):
        if index == 0:
            self.controllers.ui_controller = UiController(self.controllers.espace_controller.espace.endX, self.controllers.espace_controller.espace.endY)
            self.controllers.ui_controller.refresh_display(self.controllers.espace_controller.espace)
            self.setCentralWidget(DisplayCultureWidget(self))
        if index == 1:
            self.setCentralWidget(ManageCultureWidget(self))



