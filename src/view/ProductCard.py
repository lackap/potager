from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QHBoxLayout, QPushButton
from pyqt_color_button import ColorButton


class ProductCardWidget(QWidget):
    def __init__(self, culture, nombre_a_planter, nombre_plantes):
        super().__init__()
        self.culture = culture
        self.nombre_a_planter = nombre_a_planter
        self.nombre_plantes = nombre_plantes
        main_layout = QHBoxLayout()
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Nom"), QLabel(culture.culture_type))
        form_layout.addRow(QLabel("Famille"), QLabel(culture.famille.culture_name))
        form_layout.addRow(QLabel("Nombre à planter"), QLabel(str(nombre_a_planter)))
        form_layout.addRow(QLabel("Nombre plantés"), QLabel(str(nombre_plantes)))
        form_layout.addRow(QLabel("Mois semi"), QLabel(str(culture.mois_semi)))
        form_layout.addRow(QLabel("Mois plantation"), QLabel(str(culture.mois_plantation)))
        colored_square = ColorButton(20)
        colored_square.setColor(culture.color)
        form_layout.addRow(QLabel("Couleur"), colored_square)

        main_layout.addLayout(form_layout)

        icons_layout = QVBoxLayout()
        image_label = QLabel(self)
        pixmap = QPixmap("resources/culture_image/" + culture.culture_type + ".jpg")
        scaled_pixmap = pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        icons_layout.addWidget(image_label)

        main_layout.addLayout(icons_layout)

        QLabel()

        self.setLayout(main_layout)





