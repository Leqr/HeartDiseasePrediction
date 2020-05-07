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
        self.attributs = None
        #Tasks are performed upon inililization

        # Task 1
        self.task1(printTree = False)
        #Task 2
        self.task2(printPrecision = True)
        #Task3
        self.task3(printRules = False)
        #Task4
        self.task4()

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

        count=0
        for i in range(len(trueValues)):
            if trueValues[i]==predValues[i]:
                count+=1


        precision = (count/len(trueValues))*100
        return precision

    def cure(self,donnees):
        found2=False
        before=[]
        treatments=[]
        rep=[]
        rep_sol=[]

        for donnee in donnees:
            found1=False
            if donnee[0]=='not sick':
                print("No treatments needed")
            elif donnee[0]=='sick':
                rep.append(self.arbre.classifie(donnee[1]))
                attributs=list(donnee[1].keys())
                #Checker si en changeant un seul attribut on peut guérir
                for i in range(len(attributs)):
                    cure1={}
                    before_cure1={}
                    if not attributs[i]=='age' and not attributs[i]=='sex':
                        saved_data={attributs[i]:donnee[1][attributs[i]]}
                        values_range=self.attributs[attributs[i]]
                        #print(attribut)
                        for value in values_range:
                            #print(value)
                            donnee[1][attributs[i]]=value
                            classe=self.only_class(self.arbre.classifie(donnee[1]))
                            #print(classe)
                            if classe=='not sick':
                                rep_sol.append(self.arbre.classifie(donnee[1]))
                                found1=True
                                cure1[attributs[i]]=value
                                treatments.append(cure1)
                                before_cure1[attributs[i]]=saved_data[attributs[i]]
                                before.append(before_cure1)
                                break
                    if found1:
                        break
                #Si on a pas trouvé de remède avec un seul attribut --> check avec\
                # la combinaison de deux autres attributs. Mais trop de combinaison\
                # sont essayées --> problème avec les break surement
                if found1==False:
                    found2=False
                    for i in range(len(attributs)):
                        cure2={}
                        before_cure2={}
                        if not attributs[i]=='age' and not attributs[i]=='sex':
                            saved_data={attributs[i]:donnee[1][attributs[i]]}
                            values_range1=self.attributs[attributs[i]]
                            for value in values_range1:
                                donnee[1][attributs[i]]=value
                                for j in range(i+1,len(attributs)):
                                    if not attributs[j]=='age' and not attributs[j]=='sex':
                                        saved_data={attributs[j]:donnee[1][attributs[j]]}
                                        values_range2=self.attributs[attributs[j]]
                                        for val in values_range2:
                                            donnee[1][attributs[j]]=val
                                            classe=self.only_class(self.arbre.classifie(donnee[1]))
                                            if classe=='not sick':
                                                found2=True
                                                cure2[attributs[i]]=value
                                                cure2[attributs[j]]=val
                                                treatments.append(cure2)
                                                before_cure2[attributs[i]]=saved_data[attributs[i]]
                                                before_cure2[attributs[j]]=saved_data[attributs[j]]
                                                before.append(before_cure2)
                                                break
                                    if found2:
                                        break
                                if found2:
                                    break
                            if found2:
                                break

        if len(treatments)!=0:
            for i in range(len(treatments)):
                list_attributs=list(treatments[i].keys())
                for j in range(len(list_attributs)):
                    i_str=str(i)
                    print(rep[i])
                    print('Cure: '+"{}".format(list_attributs[j])+": "+"{}-->{}".format
                        (before[i][list_attributs[j]],treatments[i][list_attributs[j]]))
                    print(rep_sol[i])
                    print('')
        else:
            print("No treatment founded")

    def DFSgenerateRulesFromTree(self, tree, propositions):

        """ DFS over all the tree to generate a set of rules.

            :param tree: useful for the recursive algorithm
            :param propositions: useful for the recursive algorithm

        """
        #the rules will have the following form
        # rule = [[[(att, value),...,(att, value)],res 1],...,[[(att, value),...,(att, value)],res m]]
        for value, child in tree.enfants.items():
            if child.terminal():
                newProp = propositions.copy()
                newProp.append((tree.attribut,value))
                self.regles.append([newProp,child.classe()])
            elif not (child.undefined() and child.terminal()):
                newProp2 = propositions.copy()
                newProp2.append((tree.attribut,value))
                self.DFSgenerateRulesFromTree(child,newProp2)


    def explanationForDiagnostic(self,donnee):
        """ Give an explanation of the diagnostic using the parameters of the data.

            :param donnee: a data to analyze

            :return:

        """








    def task1(self,printTree = True):
        """ Performs task 1.
        """
        print('Building the tree (Task 1)...')
        donnees = self.importData('train_bin.csv')

        id3 = ID3()
        self.arbre = id3.construit_arbre(donnees)[0]
        self.attributs = id3.construit_arbre(donnees)[1]
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

        print()

    def task3(self,printRules = True):
        """ Performs task 3.
        """
        print('Generating rules from the tree (Task 3)...')

        self.regles = []
        propositions = []
        self.DFSgenerateRulesFromTree(self.arbre,propositions)
        if printRules:
            for i in self.regles:
                print(i)
        print()

    def task4(self):
        """ Performs task 4.
        """
        print('Finding cures (Task 4)...')

        donnees=self.importData("train_bin.csv")
        self.cure(donnees)

        print()
