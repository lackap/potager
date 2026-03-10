
class CaseTableau(object):
    def __init__(self, row, column, culture = None):
        self.row = row
        self.column = column
        self.culture = culture
        self.planche = None
        self.travaillable = False
