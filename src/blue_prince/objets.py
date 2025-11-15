import random
import pieces

class Objet:
    """Représente un objet du jeu.
    
    Attributes:
        nom (str): Nom de l'objet
        prix (int): Prix d'achat en or
        description (str): Description de l'objet
    """

    def __init__(self, nom, chance_app, unique=False):
        self.nom = nom
        self.chance_app = chance_app
        self.is_collected = False
        self.unique = unique

    def copier(self):
        """Crée une copie indépendante de l'objet."""
        return Objet(self.nom, self.chance_app, self.unique)
    
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
            # Vérifier si l'objet est unique et si le joueur l'a déjà
            if self.unique:
                if self.nom == 'detecteur de metaux' and joueur.chance_metaux == 2:
                    return None
                elif self.nom == 'patte de lapin' and joueur.chance_objets == 2:
                    return None
                elif self.nom == 'kit de crochetage' and joueur.kit_crochetage == 1:
                    return None
            
            # Appliquer l'effet et retourner le nom pour l'affichage
            nom_affichage = None
            
            if self.nom == 'gemme':
                joueur.ajouter_gemmes(1)
                nom_affichage = "1 gemme"
            elif self.nom == 'pomme':
                joueur.ajouter_pas(2)
                nom_affichage = "1 pomme (+2 pas)"
            elif self.nom == 'banane':
                joueur.ajouter_pas(3)
                nom_affichage = "1 banane (+3 pas)"
            elif self.nom == 'gateau':
                joueur.ajouter_pas(10)
                nom_affichage = "1 gâteau (+10 pas)"
            elif self.nom == 'sandwich':
                joueur.ajouter_pas(15)
                nom_affichage = "1 sandwich (+15 pas)"
            elif self.nom == 'repas':
                joueur.ajouter_pas(25)
                nom_affichage = "1 repas (+25 pas)"
            elif self.nom == 'detecteur de metaux':
                joueur.chance_metaux = 2
                nom_affichage = "1 détecteur de métaux"
            elif self.nom == 'patte de lapin':
                joueur.chance_objets = 2
                nom_affichage = "1 patte de lapin"
            elif self.nom == 'kit de crochetage':
                joueur.kit_crochetage = 1
                nom_affichage = "1 kit de crochetage"
            elif self.nom == 'clé':
                joueur.cles += 1
                nom_affichage = "1 clé"
            elif self.nom == 'dé':
                joueur.des += 1
                nom_affichage = "1 dé"
            
            # Marquer l'objet comme collecté
            self.is_collected = True
            
            return nom_affichage
        
        return None

# Objets globaux
cle = Objet('clé', 2)
de = Objet('dé', 2)
gemme = Objet('gemme', 2)
pomme = Objet('pomme', 3)
banane = Objet('banane', 2)
gateau = Objet('gateau', 1)
sandwich = Objet('sandwich', 1)
repas = Objet('repas', 1)
detecteur_metaux = Objet('detecteur de metaux', 2, unique=True)
patte_lapin = Objet('patte de lapin', 2, unique=True)
kit_crochetage = Objet('kit de crochetage', 2, unique=True)

objets_disponibles = [cle, de, gemme, pomme, banane, gateau, sandwich, repas, detecteur_metaux, patte_lapin, kit_crochetage]