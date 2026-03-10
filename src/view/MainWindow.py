from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from src.controller.ProductController import ProductController


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(1600, 1000)
        self.controller = ProductController()

        layout = QHBoxLayout()

        layout_left = QVBoxLayout()
        auto_fill_button = QPushButton()
        auto_fill_button.setText("Autofill")
        auto_fill_button.clicked.connect(self.autofill_click)

        layout_left.addWidget(self.controller.list_a_planter)
        layout_left.addWidget(auto_fill_button)

        widget_left = QWidget()
        widget_left.setLayout(layout_left)
        widget_left.setFixedWidth(150)
        layout.addWidget(widget_left)

        layout.addWidget(self.controller.table)

        layout.addWidget(self.controller.list_plantes)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def autofill_click(self):
        self.controller.auto_fill()



