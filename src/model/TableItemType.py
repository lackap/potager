from enum import Enum

from PyQt5.QtWidgets import QTableWidgetItem


class TableItemType(Enum):
    PRODUCT_ITEM_TYPE = QTableWidgetItem.UserType + 1
    CULTURE = QTableWidgetItem.UserType + 2
    NOMBRE_CULTURE = QTableWidgetItem.UserType + 3