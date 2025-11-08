class GestionnairePieces:
    """Gère le pool de pièces disponibles avec un système de deck limité.
    
    Chaque pièce (sauf Entrance Hall et Antechamber) ne peut être utilisée que 2 fois.
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
        """Vérifie si une pièce est encore disponible (utilisée moins de 2 fois).
        
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
            list: Liste des pièces utilisables (moins de 2 fois)
        """
        return [
            p for p in self.toutes_les_pieces 
            if p.nom not in ["Entrance Hall", "Antechamber"] 
            and self.piece_disponible(p.nom)
        ]