class NoeudDeDecision:
    """ Un noeud dans un arbre de décision.

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, if we can not classify a data point, we return the predominant class (see lines 53 - 56).
    """

    def __init__(self, attribut, donnees, p_class, enfants=None):
        """
            :param attribut: l'attribut de partitionnement du noeud (``None`` si\
            le noeud est un noeud terminal).
            :param list donnees: la liste des données qui tombent dans la\
            sous-classification du noeud.
            :param enfants: un dictionnaire associant un fils (sous-noeud) à\
            chaque valeur de l'attribut du noeud (``None`` si le\
            noeud est terminal).
        """

        self.attribut = attribut
        self.donnees = donnees
        self.enfants = enfants
        self.p_class = p_class

    def terminal(self):
        """ Vérifie si le noeud courant est terminal. """

        return self.enfants is None

    def undefined(self):
        """ Check if the node is undefined (means that no data has this combination of attributes). """

        return isinstance(self.donnees[0], str)

    def classe(self):
        """ Si le noeud est terminal, retourne la classe des données qui\
            tombent dans la sous-classification (dans ce cas, toutes les\
            données font partie de la même classe.
        """

        if self.terminal() and not self.undefined():
            return self.donnees[0][0]
        elif self.undefined() :
            return self.donnees[0]

    def classifie(self, donnee):
        """
         Classifie une donnée à l'aide de l'arbre de décision duquel le noeud\
            courant est la racine.

            :param donnee: la donnée à classifier.
            :return: la classe de la donnée selon le noeud de décision courant.
        """

        rep = ''
        if self.terminal():
            rep += 'Alors {}'.format(self.classe())
        else:

            valeur = donnee[self.attribut]

            #this part takes into account the case where an attribute value from the
            #test dataset doesn't exist in the training dataset.
            if valeur in self.enfants.keys():
                enfant = self.enfants[valeur]
                rep += 'Si {} = {}, '.format(self.attribut, valeur)
                rep += enfant.classifie(donnee)
            else :
                rep += 'Si {} = {}, '.format(self.attribut, valeur)
                rep += 'Alors undefined'

        return rep

    def repr_arbre(self, level=0):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine.
        """

        rep = ''
        if self.terminal() and not self.undefined():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            rep += '---'*level
            rep += 'Décision basée sur les données:\n'
            for donnee in self.donnees:
                rep += '---'*level
                rep += str(donnee) + '\n'

        elif self.undefined():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            rep += '---'*level
            rep += 'Décision basée sur la classe la plus représentée dans le noeud précédent.\n'

        else:
            for valeur, enfant in self.enfants.items():
                rep += '---'*level
                rep += 'Si {} = {}: \n'.format(self.attribut, str(valeur).upper())
                rep += enfant.repr_arbre(level+1)

        return rep

    def getDepth(self,level = 0, endLevels = []):
        """
        Return the mean and max depth of the tree, no parameters needed.

            :return: A list with the mean depth and max depth.
        """
        maxi = 0
        if self.terminal() or self.undefined():
            endLevels.append(level)
            maxi = level
        else :
            maxs = []

            for valeur, enfant in self.enfants.items():
                endLevels,maxi = enfant.getDepth(level+1,endLevels)
                maxs.append(maxi)
            maxi = max(maxs)

        if level == 0:
            meanLevel = sum(endLevels)/len(endLevels)
            return [meanLevel,maxi]

        return [endLevels,maxi]

    def __repr__(self):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine.
        """

        return str(self.repr_arbre(level=0))
