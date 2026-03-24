from PyQt5 import QtWidgets

import sys

from src.lackap.projet.potager.view.MainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    app.exec()