import sys

from PyQt5.QtWidgets import QApplication
from src.lackap.project.potager.view.MainWindow import MainWindow



app = QApplication(sys.argv)

window = MainWindow()
window.showMaximized()

app.exec()
