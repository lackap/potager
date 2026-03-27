from PyQt6.QtWidgets import QDialog, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QDialogButtonBox


class AddPlancheDialog(QDialog):
    def __init__(self, window):
        super(AddPlancheDialog, self).__init__(window)

        self.setWindowTitle("Créer planche")
        layout = QHBoxLayout()
        form_layout = QFormLayout()
        self.planche_name = QLineEdit()
        form_layout.addRow(QLabel("Nom planche :"), self.planche_name)
        self.start_x = QLineEdit()
        form_layout.addRow(QLabel("Start X :"), self.start_x)
        self.end_x = QLineEdit()
        form_layout.addRow(QLabel("End X :"), self.end_x)
        self.start_y = QLineEdit()
        form_layout.addRow(QLabel("Start Y : "), self.start_y)
        self.end_y = QLineEdit()
        form_layout.addRow(QLabel("End Y : "), self.end_y)
        layout.addLayout(form_layout)
        self.setLayout(layout)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)



