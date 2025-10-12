class Objet:
    def __init__(self, nom, prix, description):
        self.nom = nom
        self.prix = prix
        self.description = description

    def ajouter_au_joueur(self, joueur, nb_or=0):
        if self.nom == "clé":
            joueur.cles += 1
        elif self.nom == "dé":
            joueur.des += 1
        elif self.nom == "gemme":
            joueur.ajouter_gemmes(1)
        elif self.nom == "or":
            joueur.ajouter_or(nb_or)  # Le prix de l'objet "or" est la quantité d'or ajoutée

    def retirer_du_joueur(self, joueur, nb_or=0):
        if self.nom == "clé" and joueur.cles > 0:
            joueur.cles -= 1
        elif self.nom == "dé" and joueur.des > 0:
            joueur.des -= 1
        elif self.nom == "gemme" and joueur.gemmes > 0:
            joueur.utiliser_gemmes(1)
        elif self.nom == "or" and nb_or <= joueur.or_:
            joueur.utiliser_or(nb_or)  # Le prix de l'objet "or" est la quantité d'or retirée