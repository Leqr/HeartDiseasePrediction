from math import log
from noeud_de_decision import NoeudDeDecision
import operator
import numpy as np

class ID3:
    """ Algorithme ID3.

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, in construit_arbre_recur(), if donnees == [] (line 70), it returns a terminal node with the predominant class of the dataset -- as computed in construit_arbre() -- instead of returning None.
        Moreover, the predominant class is also passed as a parameter to NoeudDeDecision().
        This class can also take into account continuous attribute values.
    """

    def construit_arbre(self, donnees, continuous = False,accuracy_factor = 1):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``
            :param continuous: Boolean permettant l'utilisation de donnée continues
            :param accuracy_factor: Facteur de précision pour la discrétisation des données continues

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

        # Find the predominant class
        classes = set([row[0] for row in donnees])
        # print(classes)
        predominant_class_counter = -1
        for c in classes:
            # print([row[0] for row in donnees].count(c))
            if [row[0] for row in donnees].count(c) >= predominant_class_counter:
                predominant_class_counter = [row[0] for row in donnees].count(c)
                predominant_class = c
        # print(predominant_class)
        arbre = self.construit_arbre_recur(donnees, attributs, predominant_class,continuous,accuracy_factor)

        return arbre, attributs

    def construit_arbre_recur(self, donnees, attributs, predominant_class,continuous = False,accuracy_factor = 1):
        """ Construit rédurcivement un arbre de décision à partir
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :param continuous: Boolean permettant l'utilisation de donnée continues
            :param accuracy_factor: Facteur de précision pour la discrétisation des données continues

            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """

        def classe_unique(donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """

            if len(donnees) == 0:
                return True
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False
            return True

        if donnees == []:

            return NoeudDeDecision(None, [str(predominant_class), dict()], str(predominant_class))

        # Si toutes les données restantes font partie de la même classe,
        # on peut retourner un noeud terminal.
        elif classe_unique(donnees):

            return NoeudDeDecision(None, donnees, str(predominant_class))

        else:
            if not continuous:
                # Sélectionne l'attribut qui réduit au maximum l'entropie.
                h_C_As_attribs = [(self.h_C_A(donnees, attribut, attributs[attribut]),
                                   attribut) for attribut in attributs]

                attribut = min(h_C_As_attribs, key=lambda h_a: h_a[0])[1]

                # Crée les sous-arbres de manière récursive.
                attributs_restants = attributs.copy()
                del attributs_restants[attribut]
                partitions = self.partitionne(donnees, attribut, attributs[attribut])

            if continuous:
                #manages the discretization of the continuous data, tries different steps to chose the best.
                h_C_As_attribs = []
                for attribut,valeurs in attributs.items():
                    if len(valeurs) > 3:
                        stepVal = self.step(list(valeurs))
                        pointNumber = accuracy_factor*(max(valeurs)-min(valeurs))/stepVal
                        h_C_As_attrib = [(self.h_C_A_cont(donnees, attribut, split_valeur),
                                       (attribut,split_valeur)) for split_valeur in np.linspace(min(valeurs),max(valeurs),int(pointNumber))]
                        h_C_As_attribs.append(min(h_C_As_attrib, key=lambda h_a: h_a[0]))
                    else:
                        h_C_As_attrib = [(self.h_C_A_cont(donnees, attribut, split_valeur),
                                       (attribut,split_valeur)) for split_valeur in valeurs]
                        h_C_As_attribs.append(min(h_C_As_attrib, key=lambda h_a: h_a[0]))

                a = min(h_C_As_attribs, key=lambda h_a: h_a[0])[1]
                attribut = a[0]
                splitValue = a[1]
                partitions = self.partitionne_cont(donnees, attribut, splitValue)
                attributs_restants = attributs.copy()



            enfants = {}
            for valeur, partition in partitions.items():
                if continuous:
                    val = valeur + ' ' +str(splitValue)
                if not continuous:
                    val = valeur
                enfants[val] = self.construit_arbre_recur(partition,
                                                             attributs_restants,
                                                             predominant_class,continuous,accuracy_factor)

            return NoeudDeDecision(attribut, donnees, str(predominant_class), enfants)

    def step(self,valeurs):
        """ Determine la différence moyenne entre les valeur consecutives.

            :param list valeurs: les données pour le calcul du step.

            :return: Valeur moyenne du step.
        """
        meanStep = 0
        valeurs.sort()
        for i in range(len(valeurs)-1):
            step_ = valeurs[i+1]-valeurs[i]
            meanStep += step_

        meanStep = meanStep/(len(valeurs)-1)

        return meanStep

    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        partitions = {valeur: [] for valeur in valeurs}

        for donnee in donnees:
            partition = partitions[donnee[1][attribut]]
            partition.append(donnee)

        return partitions

    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: p(a_j)
        """
        # Nombre de données.
        nombre_donnees = len(donnees)

        # Permet d'éviter les divisions par 0.
        if nombre_donnees == 0:
            return 0.0

        # Nombre d'occurrences de la valeur a_j parmi les données.
        nombre_aj = 0
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                nombre_aj += 1

        # p(a_j) = nombre d'occurrences de la valeur a_j parmi les données /
        #          nombre de données.
        return nombre_aj / nombre_donnees

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        # Nombre d'occurrences de la valeur a_j parmi les données.
        donnees_aj = [donnee for donnee in donnees if donnee[1][attribut] == valeur]
        nombre_aj = len(donnees_aj)

        # Permet d'éviter les divisions par 0.
        if nombre_aj == 0:
            return 0

        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles
        # A vaut a_j.
        donnees_ci = [donnee for donnee in donnees_aj if donnee[0] == classe]
        nombre_ci = len(donnees_ci)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        return nombre_ci / nombre_aj

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        # Les classes attestées dans les exemples.
        classes = list(set([donnee[0] for donnee in donnees]))

        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs = [self.p_ci_aj(donnees, attribut, valeur, classe)
                    for classe in classes]

        # Si p vaut 0 -> plog(p) vaut 0.
        return -sum([p_ci_aj * log(p_ci_aj, 2.0)
                    for p_ci_aj in p_ci_ajs
                    if p_ci_aj != 0])

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        # Calcule P(a_j) pour chaque valeur a_j de l'attribut A.
        p_ajs = [self.p_aj(donnees, attribut, valeur) for valeur in valeurs]

        # Calcule H_C_aj pour chaque valeur a_j de l'attribut A.
        h_c_ajs = [self.h_C_aj(donnees, attribut, valeur)
                   for valeur in valeurs]

        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])

    def partitionne_cont(self, donnees, attribut, split):
        """ Partitionne les données sur les valeurs binaires de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list split: La valeurs de séparation de la branche de l'abre pour l'attribut.

            :return: un dictionnaire qui associe les opérateurs < et >= au données plus petite et plus grandes que split.
        """
        partitions = {'<': [] , '>=' : []}

        for donnee in donnees:
            if donnee[1][attribut] < split:
                partitions['<'].append(donnee)
            else :
                partitions['>='].append(donnee)

        return partitions

    def p_aj_cont(self, donnees, attribut, valeur,comparator):
        """ p(a_j) - la probabilité que la valeur de l'attribut A < a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur de split.
            :param comparator: l'opérateur logique de comparaison à utiliser.

            :return: p(a_j)
        """
        # Nombre de données.
        nombre_donnees = len(donnees)

        # Permet d'éviter les divisions par 0.
        if nombre_donnees == 0:
            return 0.0

        # Nombre d'occurrences de la valeur a_j parmi les données.
        nombre_aj = 0
        for donnee in donnees:
            if comparator(donnee[1][attribut],valeur):
                nombre_aj += 1

        # p(a_j) = nombre d'occurrences de la valeur a_j parmi les données /
        #          nombre de données.
        return nombre_aj / nombre_donnees

    def p_ci_aj_cont(self, donnees, attribut, valeur, classe,comparator):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A < a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur de split.
            :param classe: la valeur c_i de la classe C.
            :param comparator: l'opérateur logique de comparaison à utiliser.

            :return: p(c_i | a_j)
        """
        # Nombre d'occurrences de la valeur a_j parmi les données.
        donnees_aj = [donnee for donnee in donnees if comparator(donnee[1][attribut],valeur)]
        nombre_aj = len(donnees_aj)

        # Permet d'éviter les divisions par 0.
        if nombre_aj == 0:
            return 0

        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles
        # A < a_j.
        donnees_ci = [donnee for donnee in donnees_aj if donnee[0] == classe]
        nombre_ci = len(donnees_ci)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        return nombre_ci / nombre_aj

    def h_C_aj_cont(self, donnees, attribut, valeur,comparator):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A est < ou >= que la valeur de split.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur de split.
            :param comparator: l'opérateur logique de comparaison à utiliser.

            :return: H(C|a_j)
        """
        # Les classes attestées dans les exemples.
        classes = list(set([donnee[0] for donnee in donnees]))

        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs = [self.p_ci_aj_cont(donnees, attribut, valeur, classe,comparator)
                    for classe in classes]

        # Si p vaut 0 -> plog(p) vaut 0.
        return -sum([p_ci_aj * log(p_ci_aj, 2.0)
                    for p_ci_aj in p_ci_ajs
                    if p_ci_aj != 0])

    def h_C_A_cont(self, donnees, attribut, valeur):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant < ou >= de l'attribut A.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur de split.
            :return: H(C|A)
        """
        # Calcule P(a_j) pour < split et > split.
        p_aj_under = self.p_aj_cont(donnees, attribut, valeur,operator.lt)
        p_aj_upper = self.p_aj_cont(donnees, attribut, valeur,operator.ge)
        p_ajs = [p_aj_under,p_aj_upper]
        # Calcule H_C_aj pour < split et > split.
        h_c_aj_under = self.h_C_aj_cont(donnees, attribut, valeur,operator.lt)
        h_c_aj_upper = self.h_C_aj_cont(donnees, attribut, valeur,operator.ge)
        h_c_ajs = [h_c_aj_under,h_c_aj_upper]


        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])
