from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout


class DisplayCultureWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.controllers = parent.controllers
        layout = QHBoxLayout()

        layout_left = QVBoxLayout()
        clear_button = QPushButton()
        clear_button.setText("Clear table")
        clear_button.clicked.connect(self.clear)
        display_culture_button = QPushButton()
        display_culture_button.setText("Afficher les cultures")
        display_culture_button.clicked.connect(lambda: self.switch_to_view(1))
        auto_fill_button = QPushButton()
        auto_fill_button.setText("Autofill")
        auto_fill_button.clicked.connect(self.autofill_click)
        save_button = QPushButton()
        save_button.setText("Save")
        save_button.clicked.connect(self.save_click)
        load_button = QPushButton()
        load_button.setText("Load")
        load_button.clicked.connect(self.load_click)
        switch_level_button = QPushButton()
        switch_level_button.setText("Changer vue hauteur")
        switch_level_button.clicked.connect(self.switch_display_level)

        layout_left.addWidget(self.controllers.ui_controller.list_a_planter)
        layout_left.addWidget(clear_button)
        layout_left.addWidget(switch_level_button)
        layout_left.addWidget(display_culture_button)
        layout_left.addWidget(auto_fill_button)
        layout_left.addWidget(save_button)
        layout_left.addWidget(load_button)

        widget_left = QWidget()
        widget_left.setLayout(layout_left)
        widget_left.setFixedWidth(250)
        layout.addWidget(widget_left)

        layout.addWidget(self.controllers.ui_controller.table)

        self.setLayout(layout)

    def clear(self):
        self.controllers.clear()
    def autofill_click(self):
        self.controllers.auto_fill()
    def save_click(self):
        self.controllers.save()
    def load_click(self):
        self.controllers.load()
    def switch_to_view(self, index = 1):
        self.parent().switch_to_view(index)
    def switch_display_level(self):
        self.controllers.ui_controller.switch_level(self.controllers.espace_controller.espace)