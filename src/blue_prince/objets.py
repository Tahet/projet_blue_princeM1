class Objet:
    """Représente un objet du jeu.
    
    Attributes:
        nom (str): Nom de l'objet
        prix (int): Prix d'achat en or
        description (str): Description de l'objet
    """
    
    def __init__(self, nom, chance_app):
        self.nom = nom
        self.chance_app = chance_app

    def ajouter_au_joueur(self, joueur, nb_or=0):
        """Ajoute cet objet à l'inventaire du joueur.
        
        Args:
            joueur (Joueur): Joueur recevant l'objet
            nb_or (int): Quantité d'or si objet de type "or"
        """
        if self.nom == "clé":
            joueur.cles += 1
        elif self.nom == "dé":
            joueur.des += 1
        elif self.nom == "gemme":
            joueur.ajouter_gemmes(1)
        elif self.nom == "or":
            joueur.ajouter_or(nb_or)

    def retirer_du_joueur(self, joueur, nb_or=0):
        """Retire cet objet de l'inventaire du joueur.
        
        Args:
            joueur (Joueur): Joueur perdant l'objet
            nb_or (int): Quantité d'or si objet de type "or"
        """
        if self.nom == "clé" and joueur.cles > 0:
            joueur.cles -= 1
        elif self.nom == "dé" and joueur.des > 0:
            joueur.des -= 1
        elif self.nom == "gemme" and joueur.gemmes > 0:
            joueur.utiliser_gemmes(1)
        elif self.nom == "or" and nb_or <= joueur.or_:
            joueur.utiliser_or(nb_or)
    
    def appliquer_effet(self, joueur):

        if self.nom == 'gemme':
            joueur.ajouter_gemme(1)
            print("Vous avez trouvé 1 gemme")
        if self.nom == 'pomme':
            joueur.ajouter_pas(2)
            print("Vous avez trouvé une pomme bravo")
        if self.nom == 'banane':
            joueur.ajouter_pas(3)
            print("Vous avez trouvé une banene")
        
        if self.nom == 'detecteur de metaux':
            joueur.chance_metaux = 2
            print("Vous avez trouvé le détecteur de métaux")
        if self.nom == 'patte de lapin':
            joueur.chance_objets = 2
            print("Vous avez trouvé la patte de lapin")
        if self.nom == 'kit de crochetage':
            joueur.kit_crochetage = 1
            print("Vous avez trouvé le kit de crochetage")

gemme = Objet('gemme', 1)
pomme = Objet('pomme', 1)
banane = Objet('banane', 1)
detecteur_metaux = Objet('dectecteur de metaux',2)
patte_lapin = Objet('patte de lapin',3)
kit_crochetage= Objet('kit de crochetage', 2)

