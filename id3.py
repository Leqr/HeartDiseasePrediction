from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """

    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """

        # Nous devons extraire les domaines de valeur des
        # attributs, puisqu'ils sont nécessaires pour
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)

        arbre = self.construit_arbre_recur(donnees, attributs)

        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """

        if len(donnees) == 0:
            return None

        elif len(set([donnee[0] for donnee in donnees])) == 1:
            return NoeudDeDecision(None,donnees,None)

        else:
            #get the attribute minimizing the classifaction entropy
            entropyAttribut = {}
            for attribut,valeurs in attributs.items():
                entropyAttribut.update({attribut: self.h_C_A(donnees,attribut,valeurs)})
            bestAttribut = min(entropyAttribut, key=entropyAttribut.get)

            valeurs = attributs.pop(bestAttribut)
            child = {}
            partitions = self.partitionne(donnees, bestAttribut, valeurs)

            for v in valeurs:
                child.update({v : self.construit_arbre_recur(partitions[v],attributs)})
            return NoeudDeDecision(bestAttribut,donnees,child)





    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        dic = {}
        for val in valeurs:
            dic.update({val:[]})

        for donnee in donnees:
            a_j = donnee[1].pop(attribut)
            l_j = dic[a_j]
            l_j.append(donnee)
            dic.update({a_j:l_j})
        return dic


    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: p(a_j)
        """
        n = 0
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                n = n + 1
        return n/len(donnees)


    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """

        #p(c_i|a_j) = p(c_i and a_j)/p(a_j) = n(c_i and a_j)/n(a_j)

        n = 0
        #get the data subset that validate the attribute value
        donneesCondi = []
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                donneesCondi.append(donnee)
        #calculate the probability of having c = classe inside this subset
        for donnee in donneesCondi:
            if donnee[0] == classe:
                n = n + 1
        if len(donneesCondi) != 0:
            return n/len(donneesCondi)
        else :
            return 0


    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """

        classes = list(set([donnee[0] for donnee in donnees]))
        entropy = 0
        for c in classes:
            p = self.p_ci_aj(donnees, attribut, valeur, c)
            if p != 0:
                entropy = entropy - p*log(p)
        return entropy

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        entropyClassification = 0
        for i in valeurs:
            entropyClassification = entropyClassification + self.p_aj(donnees,attribut,i)*self.h_C_aj(donnees,attribut,i)
        return entropyClassification
