from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from src.model.Culture import Culture
from src.view.ProductCard import ProductCardWidget


class ManageCultureWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.controllers = parent.controllers
        main_layout = QVBoxLayout()
        count = 0
        layout = QHBoxLayout()
        added = False
        for culture in Culture:
            layout.addWidget(ProductCardWidget(culture, 1, 1))
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

        self.setLayout(main_layout)

    def autofill_click(self):
        self.controllers.auto_fill()
    def save_click(self):
        self.controllers.save()
    def load_click(self):
        self.controllers.load()
    def switch_to_view(self, index = 1):
        self.parent().switch_to_view(index)
