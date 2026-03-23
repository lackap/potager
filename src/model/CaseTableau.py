from src.model.Culture import Culture


class CaseTableau(object):
    def __init__(self, culture = Culture.NONE, culture_start = False):
        self.culture = culture
        self.init_culture = culture_start
        self.travaillable = False
