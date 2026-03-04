import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from MainWindow import MainWindow



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
