from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from src.controller.ProductController import ProductController


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.controller = ProductController()

        layout = QHBoxLayout()

        layout_left = QVBoxLayout()
        auto_fill_button = QPushButton()
        auto_fill_button.setText("Autofill")
        auto_fill_button.clicked.connect(self.autofill_click)
        save_button = QPushButton()
        save_button.setText("Save")
        save_button.clicked.connect(self.save_click)
        load_button = QPushButton()
        load_button.setText("Load")
        load_button.clicked.connect(self.load_click)

        layout_left.addWidget(self.controller.ui_controller.list_a_planter)
        layout_left.addWidget(auto_fill_button)
        layout_left.addWidget(save_button)
        layout_left.addWidget(load_button)

        widget_left = QWidget()
        widget_left.setLayout(layout_left)
        widget_left.setFixedWidth(150)
        layout.addWidget(widget_left)

        layout.addWidget(self.controller.ui_controller.table)

        layout.addWidget(self.controller.ui_controller.list_plantes)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def autofill_click(self):
        self.controller.auto_fill()
    def save_click(self):
        self.controller.save()
    def load_click(self):
        self.controller.load()



