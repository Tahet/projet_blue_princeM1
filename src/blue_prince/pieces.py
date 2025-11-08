import os
import pygame
import random
from objets import gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage

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
        self.a_objet = False

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
    
    def appliquer_rotation(self, angle):
        """Applique une rotation manuelle à la pièce.
        
        Args:
            angle (int): Angle de rotation (0, 90, 180, 270)
        """
        if angle == 0:
            self.directions = self.directions_originales.copy()
            self.icon_img = self.icon_img_original.copy() if self.icon_img_original else None
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
        {"file": "Trophy_Room.tiff", "name": "Trophy Room", "connexions": ["S", "W"],"rarete": '2'},
        {"file": "Kitchen.webp", "name": "Kitchen", "connexions":["S","W"],'cout_gemmes': 1},
        {"file": "Drawing_Room.webp", "name": "Drawing Room","connexions":["S","W","E"],'cout_gemmes': 1},
        {"file": "Chapel.webp", "name": "Chapel","connexions":["S","W","E"]},
        {"file": "The_Pool.webp", "name": "The Pool","connexions":["S","W","E"],"rarete": 2,'cout_gemmes': 1},
        {"file": "Office.webp", "name": "Office","connexions":["S","W"],"rarete":2,'cout_gemmes': 0},
        {"file": "Boudoir.webp", "name": "Boudoir","connexions":["S","W"]},
        {"file": "Security.webp", "name": "Security","connexions":["S","W","E"],"rarete":2,'cout_gemmes': 0},
        {"file": "Patio.webp", "name": "Patio","connexions":["S","W"],"rarete":2,'cout_gemmes': 0},
        {"file": "Foyer.webp", "name": "Foyer","connexions":["S","N"],"rarete":3,'cout_gemmes': 1},
        {"file": "Conservatory.webp", "name": "Conservatory","connexions":["S","W"],"rarete":3,'cout_gemmes': 0},
        {"file": "Casino.webp", "name": "Casino","connexions":["S","W"],"rarete":3,'cout_gemmes': 1},
        {"file": "Cloister.webp", "name": "Cloister","connexions":["S","W","E","N"],"rarete":3,'cout_gemmes': 2},

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

def verifier_validite_piece_avec_rotation(piece, position_future, grid_pieces, grid_rows, grid_cols, orientation_entree_requise):
    """Vérifie si une pièce peut être placée en testant toutes les rotations.
    
    Essaie les 4 orientations possibles (0°, 90°, 180°, 270°) et retourne
    la première orientation valide trouvée qui a aussi la bonne connexion d'entrée.
    
    Args:
        piece (Piece): La pièce à vérifier
        position_future (tuple): Position (col, row) où la pièce serait placée
        grid_pieces (dict): Dictionnaire des pièces déjà placées
        grid_rows (int): Nombre de lignes de la grille
        grid_cols (int): Nombre de colonnes de la grille
        orientation_entree_requise (str): Orientation requise pour l'entrée (N, S, E, W)
        
    Returns:
        tuple: (bool, int) - (est_valide, angle_rotation) où angle_rotation est 0, 90, 180 ou 270
    """
    col, row = position_future
    
    # Mapping des directions vers les déplacements
    direction_offset = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0)
    }
    
    # Mapping des directions opposées
    direction_opposee = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }
    
    # Essayer les 4 rotations possibles
    for angle in [0, 90, 180, 270]:
        # Calculer les directions après rotation
        orientations = ["N", "E", "S", "W"]
        rotation_steps = angle // 90
        directions_tournees = []
        
        for direction in piece.directions_originales:
            idx = orientations.index(direction)
            new_idx = (idx + rotation_steps) % 4
            directions_tournees.append(orientations[new_idx])
        
        # Vérifier d'abord si la pièce a la connexion d'entrée requise
        if orientation_entree_requise not in directions_tournees:
            continue  # Cette rotation n'a pas la bonne connexion d'entrée
        
        # Vérifier si cette orientation est valide (toutes les ouvertures)
        est_valide = True
        
        for direction in directions_tournees:
            offset_col, offset_row = direction_offset[direction]
            voisin_col = col + offset_col
            voisin_row = row + offset_row
            
            # Vérifier si hors de la map
            if voisin_col < 0 or voisin_col >= grid_cols or voisin_row < 0 or voisin_row >= grid_rows:
                est_valide = False
                break
            
            # Vérifier s'il y a une pièce voisine
            voisin_pos = (voisin_col, voisin_row)
            if voisin_pos in grid_pieces:
                piece_voisine = grid_pieces[voisin_pos]
                direction_requise = direction_opposee[direction]
                
                # Si la pièce voisine n'a pas d'ouverture dans notre direction, c'est un mur
                if direction_requise not in piece_voisine.directions:
                    est_valide = False
                    break
        
        if est_valide:
            return True, angle
    
    return False, 0

def tirer_3_pieces_aleatoires(gestionnaire_pieces, position_future, grid_pieces, grid_rows, grid_cols, direction_entree):
    """Tire 3 pièces aléatoires valides en fonction de leur rareté.
    
    Les pièces tirées doivent avoir des ouvertures valides (pas vers des murs ou hors map).
    Les pièces sont automatiquement tournées pour trouver une orientation valide.
    Chaque pièce ne peut être utilisée que 2 fois maximum.
    
    Args:
        gestionnaire_pieces (GestionnairePieces): Gestionnaire du pool de pièces
        position_future (tuple): Position où la pièce sera placée
        grid_pieces (dict): Dictionnaire des pièces déjà placées
        grid_rows (int): Nombre de lignes
        grid_cols (int): Nombre de colonnes
        direction_entree (str): Direction d'où vient le joueur ("haut", "bas", "gauche", "droite")
        
    Returns:
        list: Liste de 3 pièces valides et orientées (ou moins si insuffisant)
    """
    # Récupérer les pièces disponibles (moins de 2 utilisations)
    pieces_tirables = gestionnaire_pieces.get_pieces_disponibles()
    
    if len(pieces_tirables) < 3:
        # Si moins de 3 pièces disponibles, retourner ce qu'on peut
        pieces_valides = []
        for p in pieces_tirables:
            piece_copie = p.copier()
            orientation_requise = {"haut": "S", "bas": "N", "gauche": "E", "droite": "W"}.get(direction_entree)
            est_valide, angle = verifier_validite_piece_avec_rotation(
                piece_copie, position_future, grid_pieces, grid_rows, grid_cols, orientation_requise
            )
            if est_valide:
                piece_copie.appliquer_rotation(angle)
                pieces_valides.append(piece_copie)
        return pieces_valides
    
    # Mapping direction d'entrée -> orientation requise dans la pièce
    direction_vers_orientation_map = {
        "haut": "S",
        "bas": "N",
        "gauche": "E",
        "droite": "W"
    }
    orientation_entree_requise = direction_vers_orientation_map.get(direction_entree)
    
    # Pondération : rareté 1=100 chances, 2=50, 3=25
    pieces_ponderees = []
    for piece in pieces_tirables:
        poids = 100 // piece.rarete
        pieces_ponderees.extend([piece] * poids)
    
    # Tirage avec validation et rotation
    pieces_tirees = []
    pieces_deja_tirees = []
    tentatives_max = 300
    tentatives = 0
    
    while len(pieces_tirees) < 3 and tentatives < tentatives_max:
        tentatives += 1
        
        # Filtrer les pièces déjà tirées
        pieces_disponibles_tirage = [
            p for p in pieces_ponderees 
            if p.nom not in pieces_deja_tirees
        ]
        
        if not pieces_disponibles_tirage:
            break
        
        # Tirer une pièce
        piece_choisie = random.choice(pieces_disponibles_tirage)
        piece_copie = piece_choisie.copier()
        
        # Vérifier si la pièce est valide (en testant toutes les rotations)
        est_valide, angle_rotation = verifier_validite_piece_avec_rotation(
            piece_copie, position_future, grid_pieces, grid_rows, grid_cols, orientation_entree_requise
        )
        
        if est_valide:
            # Appliquer la rotation trouvée
            piece_copie.appliquer_rotation(angle_rotation)
            pieces_tirees.append(piece_copie)
            pieces_deja_tirees.append(piece_choisie.nom)
    
    return pieces_tirees

def joueur_tire_pieces(gestionnaire_pieces, position_future, grid_pieces, grid_rows, grid_cols, direction_entree):
    """Permet au joueur de tirer 3 pièces valides.
    
    Args:
        gestionnaire_pieces (GestionnairePieces): Gestionnaire du pool de pièces
        position_future (tuple): Position où la pièce sera placée
        grid_pieces (dict): Dictionnaire des pièces déjà placées
        grid_rows (int): Nombre de lignes
        grid_cols (int): Nombre de colonnes
        direction_entree (str): Direction d'où vient le joueur
        
    Returns:
        list: Liste de 3 pièces tirées, valides et orientées
    """
    return tirer_3_pieces_aleatoires(gestionnaire_pieces, position_future, grid_pieces, grid_rows, grid_cols, direction_entree)

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

def placer_objets_aleatoires(pieces_disponibles, objets_disponibles, joueur):
    """Place des objets aléatoirement dans les pièces.
    
    Args:
        pieces_disponibles (list): Liste des pièces où placer les objets
        objets_disponibles (list): Liste des objets disponibles
        joueur (Joueur): Le joueur (pour vérifier ses objets)
    """
    for piece in pieces_disponibles:
        # Ne pas placer d'objets dans les pièces spéciales
        if piece.nom in ["Entrance Hall", "Antechamber"]:
            continue
        
        # Objets garantis pour certaines pièces
        if piece.nom == "Den":
            piece.ajouter_objet(gemme.copier())
        elif piece.nom == "Closet":
            objet1 = random.choice(objets_disponibles).copier()
            objet2 = random.choice(objets_disponibles).copier()
            piece.ajouter_objet(objet1)
            piece.ajouter_objet(objet2)
        
        # Objets aléatoires pour les autres pièces
        elif not piece.a_objet:
            # Patte de lapin: 60% de chance au lieu de 40%
            chance_objet = 0.6 if joueur.chance_objets == 2 else 0.4
            
            if random.random() < chance_objet:
                # Détecteur de métaux: augmenter la chance pour les objets métalliques
                if joueur.chance_metaux == 2:
                    # Créer une liste de poids modifiée
                    poids = []
                    for obj in objets_disponibles:
                        # Objets métalliques: clé, gemme
                        if obj.nom in ["clé", "gemme"]:
                            poids.append(obj.chance_app * 2)  # Double la chance
                        else:
                            poids.append(obj.chance_app)
                    
                    objet = random.choices(objets_disponibles, weights=poids)[0].copier()
                else:
                    objet = random.choices(
                        objets_disponibles, 
                        weights=[obj.chance_app for obj in objets_disponibles]
                    )[0].copier()
                
                piece.ajouter_objet(objet)
                piece.a_objet = True


def appliquer_effets_pieces_garantis(piece, joueur):
    """Applique les effets garantis d'une pièce au joueur.
    
    Args:
        piece (Piece): La pièce dont les effets doivent être appliqués
        joueur (Joueur): Le joueur qui reçoit les effets
        
    Returns:
        str: Description de l'objet trouvé, ou None
    """
    # Bedroom: le joueur gagne 2 pas
    if piece.nom == "Bedroom":
        joueur.ajouter_pas(2)
        return "2 pas"
    
    # Pantry: le joueur gagne 4 or
    elif piece.nom == "Pantry":
        joueur.ajouter_or(4)
        return "4 d'or"
    
    # Chapel: le joueur perd 1 or
    elif piece.nom == "Chapel":
        if joueur.or_ > 0:
            joueur.utiliser_or(1)
            return None  # Pas d'affichage pour les pertes
    
    # Rumpus Room: le joueur gagne 8 or
    elif piece.nom == "Rumpus Room":
        joueur.ajouter_or(8)
        return "8 d'or"

    # Nook: le joueur gagne une clé
    elif piece.nom == "Nook":
        joueur.ajouter_cle()
        return "1 clé"

    # Trophy Room: le joueur gagne 8 gemmes
    elif piece.nom == "Trophy Room":
        joueur.ajouter_gemmes(8)
        return "8 gemmes"

    # Vault: le joueur gagne 40 or
    elif piece.nom == "Vault":
        joueur.ajouter_or(40)
        return "40 d'or"
    
    return None


def retirer_objets_uniques_de_toutes_pieces(grid_pieces, nom_objet):
    """Retire tous les objets uniques d'un certain type de toutes les pièces.
    
    Args:
        grid_pieces (dict): Dictionnaire des pièces placées
        nom_objet (str): Nom de l'objet unique à retirer
    """
    for piece in grid_pieces.values():
        objets_a_garder = []
        for objet in piece.objets:
            if objet.nom != nom_objet:
                objets_a_garder.append(objet)
        piece.objets = objets_a_garder