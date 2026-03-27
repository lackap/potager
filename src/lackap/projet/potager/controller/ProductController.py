from src.lackap.projet.potager.controller.EspaceController import EspaceController
from src.lackap.projet.potager.controller.FileController import FileController
from src.lackap.projet.potager.controller.UiController import UiController
from src.lackap.projet.potager.model.Culture import Culture
from src.lackap.projet.potager.model.Planche import Planche


class ProductController:

    def __init__(self):
        self.file_controller = FileController()
        self.espace_controller = EspaceController()
        self.ui_controller = UiController(self.espace_controller.espace.endX, self.espace_controller.espace.endY)
        self.initialize()

    def clear(self):
        self.espace_controller.clear()
        self.ui_controller.refresh_display(self.espace_controller.espace)

    def add_planche_by_values(self, name, start_x, start_y, end_x, end_y):
        self.add_planche(Planche(name, start_x, end_x, start_y, end_y, Culture.NONE, False))
        self.ui_controller.refresh_display(self.espace_controller.espace)

    def add_planche(self, planche):
        self.espace_controller.add_planche(planche)

    def add_culture(self, culture, nombre):
        self.espace_controller.add_culture(culture, nombre)

    def placer_culture(self, culture, row, column):
        if self.espace_controller.placer_culture(culture, row, column):
            self.ui_controller.refresh_display(self.espace_controller.espace)

    def deplacer_culture(self, rowinit, columninit, row, column):
        if self.espace_controller.deplacer_culture(rowinit, columninit, row, column, self.ui_controller.display_level):
            self.ui_controller.refresh_display(self.espace_controller.espace)

    def enlever_culture(self, row, column):
        if self.espace_controller.enlever_culture(row, column) is not None:
            self.ui_controller.refresh_display(self.espace_controller.espace)

    def auto_fill(self):
        self.espace_controller.auto_fill()
        self.ui_controller.refresh_display(self.espace_controller.espace)

    def save(self):
        self.file_controller.save(self.espace_controller.espace)

    def load(self, refresh = True):
        loaded = self.file_controller.load(self.espace_controller.espace)
        if refresh:
            self.ui_controller.refresh_display(self.espace_controller.espace)
        return loaded

    def initialize(self):
        #if not self.load(False):
        self.espace_controller.initialize()
        self.ui_controller.initialize(self)
        self.ui_controller.refresh_display(self.espace_controller.espace)


