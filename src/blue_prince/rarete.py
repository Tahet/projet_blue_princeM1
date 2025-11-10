import random

class GestionnairePieces:
    """Gère le pool de pièces disponibles avec un système de deck limité.
    
    Chaque pièce (sauf Entrance Hall et Antechamber) ne peut être utilisée que 3 fois.
    """
    
    def __init__(self, toutes_les_pieces):
        """Initialise le gestionnaire avec toutes les pièces du jeu.
        
        Args:
            toutes_les_pieces (list): Liste de toutes les pièces chargées
        """
        self.toutes_les_pieces = toutes_les_pieces
        self.compteur_utilisation = {}
        
        # Initialiser le compteur pour toutes les pièces (sauf les pièces spéciales)
        for piece in toutes_les_pieces:
            if piece.nom not in ["Entrance Hall", "Antechamber"]:
                self.compteur_utilisation[piece.nom] = 0
    
    def piece_disponible(self, nom_piece):
        """Vérifie si une pièce est encore disponible (utilisée moins de 3 fois).
        
        Args:
            nom_piece (str): Nom de la pièce
            
        Returns:
            bool: True si la pièce peut encore être utilisée
        """
        return self.compteur_utilisation.get(nom_piece, 0) < 3
    
    def utiliser_piece(self, nom_piece):
        """Marque une pièce comme utilisée (incrémente son compteur).
        
        Args:
            nom_piece (str): Nom de la pièce utilisée
        """
        if nom_piece in self.compteur_utilisation:
            self.compteur_utilisation[nom_piece] += 1
    
    def get_pieces_disponibles(self):
        """Retourne la liste des pièces encore disponibles.
        
        Returns:
            list: Liste des pièces utilisables (moins de 3 fois)
        """
        return [
            p for p in self.toutes_les_pieces 
            if p.nom not in ["Entrance Hall", "Antechamber"] 
            and self.piece_disponible(p.nom)
        ]
    
    def determiner_niveau_verrou(self, ligne):
        """Détermine le niveau de verrouillage d'une porte en fonction de la ligne.
        
        Système de progression :
        - Lignes 7-8 : Toujours ouvert (0 clé)
        - Lignes 5-6 : Mix 0 clé (50%) / 1 clé (50%)
        - Lignes 3-4 : Mix 1 clé (50%) / 2 clés (50%)
        - Lignes 0-2 : Toujours 2 clés
        
        Args:
            ligne (int): Numéro de ligne (0 = haut, 8 = bas)
            
        Returns:
            int: Niveau de verrouillage (0, 1 ou 2)
        """
        if ligne >= 7:  # Lignes 7-8
            return 0
        elif ligne >= 5:  # Lignes 5-6
            return random.choice([0, 1])
        elif ligne >= 3:  # Lignes 3-4
            return random.choice([1, 2])
        else:  # Lignes 0-2
            return 2
    
    def initialiser_verrous_piece(self, piece, ligne):
        """Initialise les niveaux de verrouillage de toutes les portes d'une pièce.
        
        Args:
            piece (Piece): La pièce dont on initialise les verrous
            ligne (int): Ligne où se trouve la pièce (0-8)
        """
        if not hasattr(piece, 'verrous'):
            piece.verrous = {}
        
        if not hasattr(piece, 'portes_ouvertes'):
            piece.portes_ouvertes = {}
        
        # Pour chaque direction possible
        for direction in ["N", "S", "E", "W"]:
            # Si la pièce a une ouverture dans cette direction
            if direction in piece.directions:
                # Déterminer le niveau de verrouillage en fonction de la ligne
                piece.verrous[direction] = self.determiner_niveau_verrou(ligne)
                # La porte n'est pas encore ouverte
                piece.portes_ouvertes[direction] = False
            else:
                # Pas d'ouverture = pas de verrou
                piece.verrous[direction] = None
                piece.portes_ouvertes[direction] = None