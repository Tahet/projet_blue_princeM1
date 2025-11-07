class Joueur:
    """Représente le joueur avec son inventaire et sa position.
    
    Attributes:
        pas (int): Nombre de pas restants
        or_ (int): Quantité d'or possédée
        gemmes (int): Nombre de gemmes possédées
        cles (int): Nombre de clés possédées
        des (int): Nombre de dés possédés
        position (list): Position [colonne, ligne] sur la grille
    """
    
    def __init__(self):
        self.pas = 50
        self.or_ = 0
        self.gemmes = 2
        self.cles = 1
        self.des = 1
        self.position = [2, 8]
        self.chance_metaux = 1
        self.chance_objets = 1
        self.kit_crochetage = 0

    def ajouter_pas(self, nombre):
        """Ajoute des pas au joueur.
        
        Args:
            nombre (int): Nombre de pas à ajouter
        """
        self.pas += nombre
    
    def utiliser_pas(self):
        """Consomme un pas.
        
        Returns:
            bool: False si pas insuffisants, True sinon
        """
        if self.pas <= 0:
            return False
        self.pas -= 1
        return True

    def ajouter_or(self, montant):
        """Ajoute de l'or au joueur.
        
        Args:
            montant (int): Quantité d'or à ajouter
        """
        self.or_ += montant

    def utiliser_or(self, montant):
        """Consomme de l'or.
        
        Args:
            montant (int): Quantité d'or à consommer
            
        Returns:
            bool: False si or insuffisant, True sinon
        """
        if montant > self.or_:
            return False
        self.or_ -= montant
        return True
    
    def ajouter_gemmes(self, nb):
        """Ajoute des gemmes au joueur.
        
        Args:
            nb (int): Nombre de gemmes à ajouter
        """
        self.gemmes += nb
        
    def utiliser_gemmes(self, nb):
        """Consomme des gemmes.
        
        Args:
            nb (int): Nombre de gemmes à consommer
            
        Returns:
            bool: False si gemmes insuffisantes, True sinon
        """
        if nb > self.gemmes:
            return False
        self.gemmes -= nb
        return True
    
    def ajouter_cle(self):
        """Ajoute une clé au joueur."""
        self.cles += 1

    def utiliser_cle(self):
        """Consomme une clé.
        
        Returns:
            bool: False si pas de clé, True sinon
        """
        if self.cles <= 0:
            return False
        self.cles -= 1
        return True
    
    def deplacer(self, direction):
        """Déplace le joueur dans une direction.
        
        Args:
            direction (str): Direction du mouvement ("haut", "bas", "gauche", "droite")
            
        Returns:
            bool: False si mouvement hors limites, True sinon
        """
        temp_pos = list(self.position)
        moved = False

        if direction == "gauche" and self.position[0] > 0:
            temp_pos[0] -= 1
            moved = True
        elif direction == "droite" and self.position[0] < 4:
            temp_pos[0] += 1
            moved = True
        elif direction == "haut" and self.position[1] > 0:
            temp_pos[1] -= 1
            moved = True
        elif direction == "bas" and self.position[1] < 8:
            temp_pos[1] += 1
            moved = True
        
        if moved:
            self.position = temp_pos
            return True
        
        return False