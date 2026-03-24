from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from src.lackap.projet.potager.model.Culture import Culture
from src.lackap.projet.potager.view.ProductCard import ProductCardWidget


class ManageCultureWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.controllers = parent.controllers
        main_layout = QVBoxLayout()

        count = 0
        layout = QHBoxLayout()

        added = False
        for culture in Culture:
            culture_for_list = self.controllers.espace_controller.espace.list_a_planter.find_culture(culture)
            if culture_for_list is None:
                continue
            layout.addWidget(ProductCardWidget(culture, culture_for_list.nombre, culture_for_list.nombre_plantes), alignment=Qt.AlignTop)
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

        display_culture_button = QPushButton()
        display_culture_button.setFixedWidth(300)
        display_culture_button.setText("Afficher potager")
        display_culture_button.clicked.connect(lambda: self.switch_to_view(0))
        main_layout.addWidget(display_culture_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def switch_to_view(self, index = 0):
        self.parent().switch_to_view(index)
