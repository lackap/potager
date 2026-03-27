import calendar

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QGroupBox


class ProductCardWidget(QGroupBox):
    def __init__(self, culture, nombre_a_planter, nombre_plantes):
        super().__init__()
        self.culture = culture
        self.nombre_a_planter = nombre_a_planter
        self.nombre_plantes = nombre_plantes
        self.setMaximumHeight(250)

        if nombre_a_planter == 0 and nombre_plantes > 0:
            self.setStyleSheet("background-color: #9FFD9F;")
        else:
            if nombre_a_planter > 0:
                self.setStyleSheet("background-color: #ff8a8a;")


        main_layout = QHBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Nom"), QLabel(culture.culture_type))
        form_layout.addRow(QLabel("Famille"), QLabel(culture.famille.culture_name))
        form_layout.addRow(QLabel("Nombre à planter"), QLabel(str(nombre_a_planter)))
        form_layout.addRow(QLabel("Nombre plantés"), QLabel(str(nombre_plantes)))
        form_layout.addRow(QLabel("Mois semi"), QLabel(calendar.month_name[culture.mois_semi]))
        form_layout.addRow(QLabel("Mois plantation"), QLabel(calendar.month_name[culture.mois_plantation]))

        main_layout.addLayout(form_layout)

        image_label = QLabel(self)
        pixmap = QPixmap("resources/culture_image/" + culture.culture_type + ".jpg")
        scaled_pixmap = pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        main_layout.addWidget(image_label)

        self.setLayout(main_layout)





