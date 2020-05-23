import pandas as pd
from id3 import ID3
import numpy as np
import matplotlib.pyplot as plt

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
        self.task1(printTree = False)
        #Task 2
        self.task2(printPrecision = True)
        #Task3
        self.task3(printRules = True,  printDiagnostic = True)
        #Task4
        self.task4()
        #Task 5
        self.task5(printTree = False, printPrecision = True)


        print('Arbre')
        print(self.arbre)
        print('Faits')
        print(self.faits_initiaux)
        print('Regles')
        print(self.regles)
        print('Arbre Advance')
        print(self.arbre_advance)
        

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
                donnee = ['1',{}]
            elif target.iloc[i] == 0 :
                donnee = ['0',{}]
            for indexAttribut in range(len(data.iloc[i])-1):
                donnee[1].update({data.columns[indexAttribut]:data.iloc[i,indexAttribut]})
            donnees.append(donnee)

        return donnees

    def only_class(self,rep):

        """ Used to isolate the class ('0' or '1') from rep. rep is the\
        output of the function NoeudDeDecision.classifie(self,donnee).

        Args:
            rep(string): justification of the classification
        Returns:
            sol(string): the classification

        """

        sol=rep[-1]

        return sol

    def precision(self,donnees,continuous = False):

        """ Compute the precision of the tree

        Args:
            donnees: import a .csv file using importData which returns donnees
        Returns:
            precision(float): the computed precision

        """

        trueValues=[]
        for donnee in donnees:
            if donnee[0]=='0':
                trueValues.append(0)
            if donnee[0]=='1':
                trueValues.append(1)

        predValues=[]
        for donnee in donnees:
            if not continuous:
                classification = self.arbre.classifie(donnee[1])
            else :
                classification = self.arbre_advance.classifie_cont(donnee[1])

            classe = self.only_class(classification)
            #print(classe)
            if classe == '0':
                predValues.append(0)
            if classe == '1':
                predValues.append(1)

        count=0
        countSick = 0
        for i in range(len(trueValues)):
            if trueValues[i]==predValues[i]:
                count+=1
            if trueValues[i] == 0:
                countSick += 1

        #calculate accuracy thta we would get by just estimating the bernouilli probability for 0 and 1 and the sampling
        #from that estimated distribution to compare with what we get for our

        precision = (count/len(trueValues))*100
        return precision

    def cure(self,donnees):

        """ Search for the cures if '0'. Print the justification before the
        cure print the cure that is needed and print the justification after the
        cure. If '1' prints "No treatment needed" if no cure founded prints
        "No treatment founded"

        Args:
            donnees: donnees: import a .csv file using importData which returns donnees

        """

        found2=False
        before=[]
        treatments=[]
        rep=[]
        rep_sol=[]

        for donnee in donnees:
            found1=False
            if donnee[0]=='0':
                print("No treatments needed")
            elif donnee[0]=='1':
                rep.append(self.arbre.classifie(donnee[1]))
                attributs=list(donnee[1].keys())
                #look if by changing only one value it is possible to found a cure
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
                            if classe=='0':
                                rep_sol.append(self.arbre.classifie(donnee[1]))
                                found1=True
                                cure1[attributs[i]]=value
                                treatments.append(cure1)
                                before_cure1[attributs[i]]=saved_data[attributs[i]]
                                before.append(before_cure1)
                                break
                    if found1:
                        break
                #if no cure founded with only one attribut changing. Try combinations\
                #of different attributs.
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
                                            if classe=='0':
                                                rep_sol.append(self.arbre.classifie(donnee[1]))
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

    def ruleAsString(self,rule):

        """ Return the rule as the conjontion of conditions in a string.

            :param donnee: a rule to return as a string

            :return: Conjonction of conditions as a string

        """

        rep = 'If '
        for t in rule[0]:
            if t != rule[0][-1]:
                rep += str(t[0]) + '=' +  str(t[1]) + ' ' +'AND' +' '
            else:
                rep += str(t[0]) + '=' + str(t[1]) + ' ' + '-->' + ' '+ rule[1]
        return rep

    def classifyFromRule(self,donnee):

        """ Give an explanation of the diagnostic using the parameters of one data point.

            :param donnee: a data to analyze

            :return: 'Error' if no rule explains the data or an explanation if a rule is found

        """

        #converts the attributes and values of the data in the same manner as it is stored in self.regles
        dataAttributes = [(attribs,value) for attribs,value in donnee[1].items()]

        #this functions uses the properties of sets so a conversion is needed
        dataAttributesSet = set(dataAttributes)
        found = False

        #finds the attribute
        for regle in self.regles:
            regleSet = set(regle[0])
            inter = dataAttributesSet.intersection(regleSet)
            if inter == regleSet:
                diagnosticRule = regle
                found = True
        if found == False:
            return 'Error, no suitable diagnostic found'
        if found == True:
            return diagnosticRule[1]

    def explanationForDiagnostic(self,donnee):

        """ Give an explanation of the diagnostic using the parameters of one data point.

            :param donnee: a data to analyze

            :return: 'Error' if no rule explains the data or an explanation if a rule is found

        """

        #converts the attributes and values of the data in the same manner as it is stored in self.regles
        dataAttributes = [(attribs,value) for attribs,value in donnee[1].items()]

        #this functions uses the properties of sets so a conversion is needed
        dataAttributesSet = set(dataAttributes)
        found = False

        #finds the attribute
        for regle in self.regles:
            regleSet = set(regle[0])
            inter = dataAttributesSet.intersection(regleSet)
            if inter == regleSet:
                diagnosticRule = regle
                found = True
        if found == False:
            return 'Error, no suitable diagnostic found'
        if found == True:
            return self.ruleAsString(diagnosticRule)

    def generateTrainingFacts(self,trainingData):

        """ Create a list of initial facts for each training data.

            :param trainingData: a data to analyze

        """
        self.faits_initiaux = []
        for donnee in trainingData:
            faits = []
            for key,value in donnee[1].items():
                faits.append((key,value))
            self.faits_initiaux.append(faits)

    def task1(self,printTree = True):

        """ Performs task 1.
        """

        print('Building the tree (Task 1)...')
        donnees = self.importData('train_bin.csv')

        id3 = ID3()

        s = id3.construit_arbre(donnees)
        self.attributs = s[1]
        self.arbre = s[0]

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
            print('Accuracy of the tree classification = ' + "{:5.2f}".format(precision) + '%')

        print()

    def task3(self, printRules=True, printDiagnostic = True):

        """ Performs task 3.
        """

        print('Generating rules from the tree (Task 3)...')

        donnees = self.importData('train_bin.csv')

        self.regles = []
        propositions = []

        # generate self.faits_initiaux
        self.generateTrainingFacts(donnees)

        self.DFSgenerateRulesFromTree(self.arbre,propositions)
        if printRules:
            for i in self.regles:
                print(i)
        print()

        if printDiagnostic:

            countTrue = 0
            count= 0

            for i in self.importData('test_public_bin.csv'):
                r = self.classifyFromRule(i)
                count += 1
                if r == i[0]:
                    countTrue +=1
            print('Accuracy with the rule searching algorithm :')
            print("{:5.2f}".format((countTrue/count)*100)+'%')


            print('The diagnostic for this data is : ')
            print(self.explanationForDiagnostic(self.importData('train_bin.csv')[26]))
            print()

    def task4(self):

        """ Performs task 4.
        """

        print('Finding cures (Task 4)...')

        donnees=self.importData("train_bin.csv")[28:32]
        self.cure(donnees)

        print()

    def task5(self,printTree = True, printPrecision = True):

        """ Performs task 5.
        """
        #this part can create multiple replicates if the tree construction
        #in order to create an accuracy plot
        """
        print('Building the tree (Task 5)...')
        donnees = self.importData('train_continuous.csv')
        precisions = []
        for i in np.linspace(0.4,4,60):
            id3 = ID3()
            print(i)
            self.arbre_advance = id3.construit_arbre(donnees,True,i)[0]
            if printTree:
                print('Decision tree :')
                print(self.arbre_advance.__repr__(notEg = True))
            #print()
            precision = self.precision(self.importData("test_public_continuous.csv"),True)
            if printPrecision:
                print('Testing the tree...')
                print('Accuracy = ' + "{:5.2f}".format(precision) + '%')
            #print()
            precisions.append(precision)
        plt.plot(np.linspace(0.4,4,60),precisions)
        plt.xlabel('accuracy_factor')
        plt.ylabel('Accuracy %')
        plt.show()
        """

        print('Building the tree (Task 5)...')
        donnees = self.importData('train_continuous.csv')
        precisions = []
        id3 = ID3()

        self.arbre_advance = id3.construit_arbre(donnees,True,0.7)[0]

        if printTree:
            print('Decision tree :')
            print(self.arbre_advance.__repr__(notEg = True))

        print()

        precision = self.precision(self.importData("test_public_continuous.csv"),True)
        if printPrecision:
            print('Testing the tree...')
            print('Accuracy = ' + "{:5.2f}".format(precision) + '%')

        print()
