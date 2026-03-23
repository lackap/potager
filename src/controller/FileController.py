import os
import pickle


class FileController:

    def __init__(self):
        self.folder = "C://tmp/"
        self.cultures_file = "cultures.pkl"
        self.list_a_planter_file = "list_a_planter.pkl"
        self.planches_file = "planches.pkl"

    def save(self, espace):
        with open(self.folder + self.cultures_file, 'wb') as outp:
            pickle.dump(espace.cultures, outp, pickle.HIGHEST_PROTOCOL)
        with open(self.folder + self.list_a_planter_file, 'wb') as outp:
            pickle.dump(espace.list_a_planter, outp, pickle.HIGHEST_PROTOCOL)
        with open(self.folder + self.planches_file, 'wb') as outp:
            pickle.dump(espace.planches, outp, pickle.HIGHEST_PROTOCOL)


    def load(self, espace):
        if os.path.exists(self.folder + self.cultures_file):
            with open(self.folder + self.cultures_file, 'rb') as cultures_file:
                del espace.cultures
                espace.cultures = pickle.load(cultures_file)
            with open(self.folder + self.list_a_planter_file, 'rb') as list_a_planter_file:
                espace.list_a_planter = pickle.load(list_a_planter_file)
            with open(self.folder + self.planches_file, 'rb') as planches_file:
                espace.planches = pickle.load(planches_file)
            return True
        return False
