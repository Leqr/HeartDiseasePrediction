import pandas as pd

class ResultValues():

    def __init__(self):

        # Do computations here

        # Task 1
        self.arbre = None
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

    def importData(self,filename):

        """ Import data from a .csv file and transforms it into usable data containers.

            :param file: .csv data file
            :return: the data ID3 ready
        """
        data = pd.read_csv(filename)

        def precision(self,donnees):
            id3 = ID3()
            arbre = id3.construit_arbre(donnees)

            trueValues=[]
            for donnee in donnees:
                for attribut, valeur in donnee[1].items():
                    if attribut="target":
                        valeur=float(valeur)
                        trueValues.append(valeur)

            predValues=[]
            for donnee in donnees:
                #faut changer classifie ou créer une nouvelle fonction qui s'inspire
                #pour return seulement la classe et non tout le raisonnement
                predValues.append(arbre.classifie(donne[1]))

            count=0
            for i in range(len(trueValues)):
                if tureValues[i]=predValues[i]:
                    count=+1

            precision = (count/len(trueValues))*100
            return precision
