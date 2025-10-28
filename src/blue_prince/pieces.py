import os
import pygame
import random

class Piece:
    """Représente une pièce du jeu avec ses connexions et propriétés.
    
    Attributes:
        directions (list): Liste des connexions cardinales actuelles (N, E, S, W)
        directions_originales (list): Directions avant rotation
        visitee (bool): Indique si la pièce a été visitée
        objets (list): Liste des objets présents dans la pièce
        icon_img (Surface): Image pygame de la pièce (peut être tournée)
        icon_img_original (Surface): Image originale non tournée
        nom (str): Nom de la pièce
        cles_nes (list): Liste des directions nécessitant une clé
        rarete (int): Niveau de rareté (1=commun, 2=rare, 3=très rare)
        cout_gemmes (int): Coût en gemmes pour placer cette pièce
    """
    
    def __init__(self, directions, nom, cles_nes=[], icon_img=None, rarete=1, cout_gemmes=0):
        self.directions = directions
        self.directions_originales = directions.copy()
        self.visitee = False
        self.objets = []
        self.icon_img = icon_img
        self.icon_img_original = icon_img.copy() if icon_img else None
        self.nom = nom
        self.cles_nes = cles_nes
        self.rarete = rarete
        self.cout_gemmes = cout_gemmes

    def ajouter_objet(self, objet):
        """Ajoute un objet à la pièce.
        
        Args:
            objet (Objet): Objet à ajouter
        """
        self.objets.append(objet)

    def retirer_objet(self, objet):
        """Retire un objet de la pièce.
        
        Args:
            objet (Objet): Objet à retirer
        """
        if objet in self.objets:
            self.objets.remove(objet)

    def acheter_objet(self, objet, joueur):
        """Achète un objet si le joueur a assez d'or.
        
        Args:
            objet (Objet): Objet à acheter
            joueur (Joueur): Joueur effectuant l'achat
            
        Returns:
            bool: True si achat réussi, False sinon
        """
        if objet in self.objets:
            if joueur.utiliser_or(objet.prix):
                self.retirer_objet(objet)
                return True
        return False
    
    def changer_orientation(self, direction_origine):
        """Oriente la pièce selon la direction d'approche du joueur.
        
        Applique une rotation à la pièce pour qu'elle ait une connexion
        correspondant à la direction d'arrivée. Si direction_origine="haut",
        aucune rotation n'est appliquée (orientation par défaut).
        
        Args:
            direction_origine (str): Direction d'approche ("haut", "bas", "gauche", "droite")
        """
        self.directions = self.directions_originales.copy()
        self.icon_img = self.icon_img_original.copy() if self.icon_img_original else None
        
        if direction_origine == "haut":
            return
        
        mapping_direction_angle = {
            "bas": 180,
            "gauche": 270,
            "droite": 90
        }
        
        angle = mapping_direction_angle.get(direction_origine, 0)
        if angle == 0:
            return
        
        # Rotation des directions cardinales
        orientations = ["N", "E", "S", "W"]
        rotation_steps = angle // 90
        nouvelles_directions = []
        
        for direction in self.directions_originales:
            idx = orientations.index(direction)
            new_idx = (idx + rotation_steps) % 4
            nouvelles_directions.append(orientations[new_idx])
        
        self.directions = nouvelles_directions
        
        # Rotation de l'image
        if self.icon_img_original:
            self.icon_img = pygame.transform.rotate(self.icon_img_original, -angle)
    
    def copier(self):
        """Crée une copie indépendante de la pièce.
        
        Returns:
            Piece: Nouvelle instance de Piece avec données copiées
        """
        if self.icon_img_original:
            nouvelle_image = self.icon_img_original.copy()
        else:
            nouvelle_image = None
        
        nouvelle_piece = Piece(
            directions=self.directions_originales.copy(),
            nom=self.nom,
            cles_nes=self.cles_nes.copy() if self.cles_nes else [],
            icon_img=nouvelle_image,
            rarete=self.rarete,
            cout_gemmes=getattr(self, 'cout_gemmes', 0)
        )
        
        if self.icon_img_original:
            nouvelle_piece.icon_img_original = self.icon_img_original.copy()
        
        nouvelle_piece.visitee = False
        nouvelle_piece.objets = self.objets.copy()
        
        return nouvelle_piece

def charger_pieces_blue_prince(cell_w, cell_h, Piece):
    """Charge toutes les pièces du jeu depuis les fichiers images.
    
    Args:
        cell_w (int): Largeur d'une cellule en pixels
        cell_h (int): Hauteur d'une cellule en pixels
        Piece (class): Classe Piece pour instancier les pièces
        
    Returns:
        list: Liste des pièces chargées
    """
    base_dir = os.path.join(os.path.dirname(__file__), "data")
    
    pieces_data = [
        {"file": "Entrance_Hall.webp", "name": "Entrance Hall", "connexions": ["N", "E", "W"]},
        {"file": "Antechamber.webp", "name": "Antechamber", "connexions": ["N", "E", "S", "W"], "cles_nes": ["N", "E", "S", "W"]},
        {"file": "Bedroom.webp", "name": "Bedroom", "connexions": ["S", "W"]},
        {"file": "Closet.webp", "name": "Closet", "connexions": ["S"], 'rarete':'3'},
        {"file": "Commissary.webp", "name": "Commissary", "connexions": ["S","W"], 'rarete':'2', 'cout_gemmes': 1},
        {"file": "Corridor.webp", "name": "Corridor", "connexions": ["N", "S"]},
        {"file": "Den.webp", "name": "Den", "connexions": ["E", "S", "W"]},
        {"file": "East_Wing_Hall.webp", "name": "East Wing Hall", "connexions": ["E", "S", "W"], 'cout_gemmes': 0},
        {"file": "Locksmith.webp", "name": "Locksmith", "connexions": ["S"], 'rarete':'2', 'cout_gemmes': 1},
        {"file": "Master_Bedroom.webp", "name": "Master Bedroom", "connexions": ["N", "E", "S", "W"], 'rarete':'2', 'cout_gemmes': 2},
        {"file": "Passageway.webp", "name": "Passageway", "connexions": ["N", "E", "S", "W"]},
        {"file": "Rumpus_Room.webp", "name": "Rumpus Room", "connexions": ["N", "S"], 'cout_gemmes': 1},
        {"file": "Vault.webp", "name": "Vault", "connexions": ["S"], 'rarete':'3'},
        {"file": "Weight_Room.webp", "name": "Weight Room", "connexions": ["N", "E", "S", "W"], 'rarete':'2'},
        {"file": "Pantry.tiff", "name": "Pantry", "connexions": ["W", "S"]},
        {"file": "Lavatory.webp", "name": "Lavatory", "connexions": ["S"], "rarete": '2'},
        {"file": "Nook.tiff", "name": "Nook", "connexions": ["S", "W"],"rarete": '2'},
        {"file": "Trophy_Room.tiff", "name": "Trophy_Room", "connexions": ["S", "W"],"rarete": '2'},
    ]

    salles_chargees = []
    base_dir = os.path.join(os.path.dirname(__file__), "data")

    for data in pieces_data:
        img_path = os.path.join(base_dir, data["file"])
        
        try:
            icon_img = pygame.image.load(img_path).convert_alpha()
            icon_img = pygame.transform.scale(icon_img, (cell_w, cell_h))
            
            cles_necessaires = data.get("cles_nes", [])
            rarete_val = int(data.get("rarete", 1))
            cout_gemmes_val = int(data.get("cout_gemmes", 0))
            
            nouvelle_piece = Piece(
                data["connexions"],
                data["name"],
                cles_necessaires, 
                icon_img,
                rarete_val,
                cout_gemmes_val
            )
            salles_chargees.append(nouvelle_piece)
            
        except pygame.error as e:
            print(f"Erreur de chargement pour {data['file']} : {e}")

    return salles_chargees

def tirer_3_pieces_aleatoires(pieces_disponibles):
    """Tire 3 pièces aléatoires en fonction de leur rareté.
    
    Utilise un système de pondération basé sur la rareté :
    - Rareté 1 : 100 chances
    - Rareté 2 : 50 chances
    - Rareté 3 : 25 chances
    
    Args:
        pieces_disponibles (list): Liste des pièces disponibles
        
    Returns:
        list: Liste de 3 pièces uniques (ou moins si insuffisant)
    """
    # Exclure les pièces spéciales
    pieces_tirables = [p for p in pieces_disponibles 
                       if p.nom not in ["Antechamber", "Entrance Hall"]]
    
    if len(pieces_tirables) < 3:
        return pieces_tirables.copy()
    
    # Pondération : rareté 1=100 chances, 2=50, 3=25
    pieces_ponderees = []
    for piece in pieces_tirables:
        poids = 100 // piece.rarete
        pieces_ponderees.extend([piece] * poids)
    
    # Tirage sans doublons
    pieces_tirees = []
    pieces_deja_tirees = []
    
    for _ in range(3):
        if not pieces_ponderees:
            break
        
        pieces_disponibles = [p for p in pieces_ponderees if p.nom not in pieces_deja_tirees]
        
        if not pieces_disponibles:
            break
            
        piece_choisie = random.choice(pieces_disponibles)
        piece_copie = piece_choisie.copier()
        pieces_tirees.append(piece_copie)
        pieces_deja_tirees.append(piece_choisie.nom)
    
    return pieces_tirees

def joueur_tire_pieces(toutes_les_pieces):
    """Permet au joueur de tirer 3 pièces.
    
    Args:
        toutes_les_pieces (list): Liste de toutes les pièces du jeu
        
    Returns:
        list: Liste de 3 pièces tirées
    """
    return tirer_3_pieces_aleatoires(toutes_les_pieces)

def direction_vers_orientation(direction):
    """Convertit une direction de mouvement en orientation cardinale.
    
    Le joueur arrive par le côté opposé dans la nouvelle pièce.
    
    Args:
        direction (str): Direction du mouvement ("haut", "bas", "gauche", "droite")
        
    Returns:
        str: Orientation cardinale requise ("N", "S", "E", "W")
    """
    mapping = {
        "haut": "S",
        "bas": "N",
        "gauche": "E",
        "droite": "W"
    }
    return mapping.get(direction)

def piece_compatible_avec_direction(piece, direction):
    """Vérifie si une pièce peut être placée dans cette direction.
    
    Args:
        piece (Piece): Pièce à vérifier
        direction (str): Direction du mouvement
        
    Returns:
        bool: True si la pièce est compatible, False sinon
    """
    orientation_requise = direction_vers_orientation(direction)
    return orientation_requise in piece.directions

def filtrer_pieces_compatibles(pieces_tirees, direction):
    """Filtre les pièces compatibles avec la direction.
    
    Args:
        pieces_tirees (list): Liste des pièces tirées
        direction (str): Direction du mouvement
        
    Returns:
        list: Liste des pièces compatibles
    """
    return [piece for piece in pieces_tirees if piece_compatible_avec_direction(piece, direction)]

def verifier_cout_piece(piece, joueur):
    """Vérifie si le joueur a assez de gemmes.
    
    Args:
        piece (Piece): Pièce à vérifier
        joueur (Joueur): Joueur effectuant la vérification
        
    Returns:
        bool: True si le joueur a assez de gemmes, False sinon
    """
    cout = getattr(piece, 'cout_gemmes', 0)
    return joueur.gemmes >= cout

def placer_piece_si_possible(piece, joueur, direction):
    """Tente de placer une pièce et consomme les gemmes.
    
    Args:
        piece (Piece): Pièce à placer (déjà orientée)
        joueur (Joueur): Joueur effectuant le placement
        direction (str): Direction du mouvement
        
    Returns:
        bool: True si placement réussi, False sinon
    """
    if not piece_compatible_avec_direction(piece, direction):
        print(f"Pièce {piece.nom} non compatible avec direction {direction}")
        print(f"Directions de la pièce : {piece.directions}")
        return False
    
    cout = getattr(piece, 'cout_gemmes', 0)
    if joueur.gemmes >= cout:
        joueur.utiliser_gemmes(cout)
        return True
    else:
        print(f"Pas assez de gemmes : besoin de {cout}, vous avez {joueur.gemmes}")
    
    return False