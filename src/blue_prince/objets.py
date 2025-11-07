import random
import pieces
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
        self.is_collected = False  # Nouvel attribut pour vérifier si l'objet a été ramassé

    def ajouter_au_joueur(self, joueur, nb_or=0):
        """Ajoute cet objet à l'inventaire du joueur."""
        if self.nom == "clé":
            joueur.cles += 1
        elif self.nom == "dé":
            joueur.des += 1
        elif self.nom == "gemme":
            joueur.ajouter_gemmes(1)
        elif self.nom == "or":
            joueur.ajouter_or(nb_or)

    def retirer_du_joueur(self, joueur, nb_or=0):
        """Retire cet objet de l'inventaire du joueur."""
        if self.nom == "clé" and joueur.cles > 0:
            joueur.cles -= 1
        elif self.nom == "dé" and joueur.des > 0:
            joueur.des -= 1
        elif self.nom == "gemme" and joueur.gemmes > 0:
            joueur.utiliser_gemmes(1)
        elif self.nom == "or" and nb_or <= joueur.or_:
            joueur.utiliser_or(nb_or)
    
    def appliquer_effet(self, joueur):
        """Applique l'effet de l'objet au joueur, mais seulement si l'objet n'a pas encore été ramassé."""
        if not self.is_collected:
            if self.nom == 'gemme':
                joueur.ajouter_gemmes(1)
                print("Vous avez trouvé 1 gemme")
            elif self.nom == 'pomme':
                joueur.ajouter_pas(2)
                print("Vous avez trouvé une pomme !")
            elif self.nom == 'banane':
                joueur.ajouter_pas(3)
                print("Vous avez trouvé une banane !")
            elif self.nom == 'detecteur de metaux':
                joueur.chance_metaux = 2
                print("Vous avez trouvé un détecteur de métaux !")
            elif self.nom == 'patte de lapin':
                joueur.chance_objets = 2
                print("Vous avez trouvé une patte de lapin !")
            elif self.nom == 'kit de crochetage':
                joueur.kit_crochetage = 1
                print("Vous avez trouvé un kit de crochetage !")
            elif self.nom == 'clé':
                joueur.cles += 1
                print("Vous avez trouvé une clé ")
            elif self.nom == 'dé':
                joueur.des += 1
                print("Vous avez trouvé un dé ")
            

            # Marquer l'objet comme collecté pour éviter qu'il soit pris à nouveau
            self.is_collected = True

cle = Objet('clé', 1)
de = Objet('dé', 2)
gemme = Objet('gemme', 1)
pomme = Objet('pomme', 1)
banane = Objet('banane', 1)
detecteur_metaux = Objet('detecteur de metaux',2)
patte_lapin = Objet('patte de lapin',3)
kit_crochetage= Objet('kit de crochetage', 2)

objets_disponibles = [cle, de, gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage]
