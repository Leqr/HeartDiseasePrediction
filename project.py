import pandas as pd
from id3 import ID3
import pdb

class ResultValues():

    def __init__(self):

        # Task 1
        self.arbre = None
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

        #Tasks are performed upon inililization

        # Task 1
        self.task1(printTree = True)
        #Task 2
        self.task2(printPrecision = True)
        #Task3
        self.task3()

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
            #print(classe)
            if classe == 'sick':
                predValues.append(1)
            if classe == 'not sick':
                predValues.append(0)
            if classe == 'undefined':
                predValues.append(-1)

        count=0
        for i in range(len(trueValues)):
            if trueValues[i]==predValues[i]:
                count+=1


        precision = (count/len(trueValues))*100
        return precision

    def generateRulesFromTree(self, tree, propositions):
        #the rules will have the following form
        # rule = [[[(att, value),...,(att, value)],res 1],...,[[(att, value),...,(att, value)],res m]]

        for value, child in tree.enfants.items():
            if child.terminal():
                self.regles.append([propositions,child.classe()])
            elif not (child.undefined() and child.terminal()):
                propositions.append((tree.attribut,value))
                self.generateRulesFromTree(child,propositions)
                del propositions[-1]

    def task3(self):
        pdb.set_trace()
        self.regles = []
        propositions = []
        self.generateRulesFromTree(self.arbre,propositions)
        for i in self.regles:
            print(i)


    def task1(self,printTree = True):
        """ Performs task 1.
        """
        print('Building the tree (Task 1)...')
        donnees = self.importData('train_bin.csv')

        id3 = ID3()
        self.arbre = id3.construit_arbre(donnees)
        if printTree:
            print('Decision tree :')
            print(self.arbre)

        depthData = self.arbre.getDepth()
        print('Average Depth : ' + "{:5.2f}".format(depthData[0]))
        print('Maximum Depth : ' + "{:5.2f}".format(depthData[1]))
        print()

    def task2(self,printPrecision = True) :
        """ Performs task 2.
        """
        print('Testing the tree (Task 2)...')
        precision = self.precision(self.importData("test_public_bin.csv"))
        if printPrecision:
            print('Accuracy = ' + "{:5.2f}".format(precision) + '%')
