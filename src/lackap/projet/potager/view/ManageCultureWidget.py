from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton

from src.lackap.projet.potager.model.Culture import Culture
from src.lackap.projet.potager.view.ProductCard import ProductCardWidget


class ManageCultureWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.controllers = parent.controllers

        self.product_cards = []
        main_layout = QVBoxLayout()

        count = 0
        layout = QHBoxLayout()

        added = False
        for culture in Culture:
            culture_for_list = self.controllers.espace_controller.espace.list_a_planter.find_culture(culture)
            if culture_for_list is None:
                continue
            product_card = ProductCardWidget(culture, culture_for_list.nombre, culture_for_list.nombre_plantes)
            self.product_cards.append(product_card)
            layout.addWidget(product_card, alignment=Qt.AlignmentFlag.AlignTop)
            if count == 3:
                widget_to_add = QWidget()
                widget_to_add.setLayout(layout)
                main_layout.addWidget(widget_to_add)
                layout = QHBoxLayout()
                count = 0
                added = True
            else:
                count = count + 1
                added = False

        if not added:
            while count < 3:
                layout.addWidget(QWidget())
                count = count + 1
            widget_to_add = QWidget()
            widget_to_add.setLayout(layout)
            main_layout.addWidget(widget_to_add)

        main_layout.addStretch()

        buttons_layout = QHBoxLayout()

        display_culture_button = QPushButton()
        display_culture_button.setFixedWidth(300)
        display_culture_button.setText("Afficher potager")
        display_culture_button.clicked.connect(lambda: self.switch_to_view(0))
        buttons_layout.addWidget(display_culture_button, alignment=Qt.AlignmentFlag.AlignCenter)

        display_culture_button = QPushButton()
        display_culture_button.setFixedWidth(300)
        display_culture_button.setText("Sauvegarder")
        display_culture_button.clicked.connect(self.save)
        buttons_layout.addWidget(display_culture_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def switch_to_view(self, index = 0):
        self.parent().switch_to_view(index)

    def save(self):
        for product_card in self.product_cards:
            self.controllers.espace_controller.update_culture_number(product_card.culture, int(product_card.nombre_a_planter.text()))
        self.parent().switch_to_view(0)

