import pandas as pd
from id3 import ID3

class ResultValues():

    def __init__(self):

        # Task 1
        self.arbre = None
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

        # Task 1
        self.task1()
        #Task 2


    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

    def importData(self,filename):

        """ Import data from a .csv file and transforms it into usable data containers.

            :param file: .csv data file
            :return: the data ID3 ready
        """

        #import data as a panda dataframe
        data = pd.read_csv(filename)

        target = data.iloc[:,-1]

        donnees = []
        for i in range(len(target)):
            if target.iloc[i] == 1 :
                donnee = ['sick',{}]
            elif target.iloc[i] == 0 :
                donnee = ['not sick',{}]
            for indexAttribut in range(len(data.iloc[i])-1):
                donnee[1].update({data.columns[indexAttribut]:data.iloc[i,indexAttribut]})
            donnees.append(donnee)

        return donnees

    def task1(self,printTree = True):
        donnees = self.importData('train_bin.csv')

        id3 = ID3()
        self.arbre = id3.construit_arbre(donnees)

        if printTree:
            print('Arbre de décision :')
            print(self.arbre)
        return self.arbre


    def only_class(self,rep):
        str='Alors'
        sol = ''
        if str in rep:
            start=rep.find(str)+6
            sol=rep[start:]
        else:
            sol = 'Not a class'

        return sol

    def precision(self,donnees):
        id3 = ID3()
        self.arbre = id3.construit_arbre(donnees)

        trueValues=[]
        for donnee in donnees:
            if donnee[0]=='sick':
                trueValues.append(1)
            if donnee[0]=='not sick':
                trueValues.append(0)


        predValues=[]
        for donnee in donnees:
            classification = self.arbre.classifie(donnee[1])
            classe = self.only_class(classification)
            if classe == 'sick':
                predValues.append(1)
            if classe == 'not sick':
                predValues.append(0)
            if classe == 'u':
                predValues.append(-1)

        count=0
        for i in range(len(trueValues)):
            if trueValues[i]==predValues[i]:
                count=+1

        precision = (count/len(trueValues))*100
        return precision
