import os
import pickle


class FileController:

    def __init__(self):
        self.folder = "C://tmp/"
        self.culture_haute_file = "cultures_haute.pkl"
        self.culture_basse_file = "cultures_basse.pkl"
        self.list_a_planter_file = "list_a_planter.pkl"
        self.planches_file = "planches.pkl"

    def save(self, espace):
        with open(self.folder + self.culture_haute_file, 'wb') as outp:
            pickle.dump(espace.cultures_haute, outp, pickle.HIGHEST_PROTOCOL)
        with open(self.folder + self.culture_basse_file, 'wb') as outp:
            pickle.dump(espace.cultures_basse, outp, pickle.HIGHEST_PROTOCOL)
        with open(self.folder + self.list_a_planter_file, 'wb') as outp:
            pickle.dump(espace.list_a_planter, outp, pickle.HIGHEST_PROTOCOL)
        with open(self.folder + self.planches_file, 'wb') as outp:
            pickle.dump(espace.planches, outp, pickle.HIGHEST_PROTOCOL)


    def load(self, espace):
        if os.path.exists(self.folder + self.culture_haute_file):
            with open(self.folder + self.culture_haute_file, 'rb') as culture_haute_file:
                espace.cultures_haute = pickle.load(culture_haute_file)
            with open(self.folder + self.culture_basse_file, 'rb') as culture_basse_file:
                espace.cultures_basse = pickle.load(culture_basse_file)
            with open(self.folder + self.list_a_planter_file, 'rb') as list_a_planter_file:
                espace.list_a_planter = pickle.load(list_a_planter_file)
            with open(self.folder + self.planches_file, 'rb') as planches_file:
                espace.planches = pickle.load(planches_file)
            return True
        return False
