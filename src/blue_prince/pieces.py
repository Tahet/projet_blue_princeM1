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
        self.verrous = {}  
        self.portes_ouvertes = {}  

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
        # NOUVEAU : Copier les verrous
        nouvelle_piece.verrous = self.verrous.copy() if hasattr(self, 'verrous') else {}
        nouvelle_piece.portes_ouvertes = self.portes_ouvertes.copy() if hasattr(self, 'portes_ouvertes') else {}
    
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
        {"file": "Master_Bedroom.webp", "name": "Master Bedroom", "connexions": ["N"], 'rarete':'2', 'cout_gemmes': 2},
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
    ]
    
    pieces = []
    for data in pieces_data:
        image_path = os.path.join(base_dir, data["file"])
        
        if os.path.exists(image_path):
            try:
                icon = pygame.image.load(image_path).convert_alpha()
                icon = pygame.transform.scale(icon, (cell_w, cell_h))
            except Exception as e:
                print(f"Erreur chargement image {data['file']}: {e}")
                icon = None
        else:
            print(f"Image non trouvée: {image_path}")
            icon = None
        
        rarete = int(data.get('rarete', 1))
        cout_gemmes = int(data.get('cout_gemmes', 0))
        
        piece = Piece(
            directions=data["connexions"],
            nom=data["name"],
            cles_nes=data.get("cles_nes", []),
            icon_img=icon,
            rarete=rarete,
            cout_gemmes=cout_gemmes
        )
        pieces.append(piece)
    
    return pieces

def tirer_pieces_avec_rarete(gestionnaire_pieces, nombre=3):
    """Tire un certain nombre de pièces selon leur rareté.
    
    Système de rareté:
    - Rareté 1 (Commun): 70% de chance
    - Rareté 2 (Rare): 25% de chance  
    - Rareté 3 (Très rare): 5% de chance
    
    Args:
        gestionnaire_pieces (GestionnairePieces): Gestionnaire contenant les pièces
        nombre (int): Nombre de pièces à tirer
        
    Returns:
        list: Liste des pièces tirées (copies indépendantes)
    """
    pieces_disponibles = gestionnaire_pieces.get_pieces_disponibles()
    
    if len(pieces_disponibles) == 0:
        return []
    
    pieces_par_rarete = {1: [], 2: [], 3: []}
    for piece in pieces_disponibles:
        rarete = getattr(piece, 'rarete', 1)
        pieces_par_rarete[rarete].append(piece)
    
    pool_pieces = []
    if pieces_par_rarete[1]:
        pool_pieces.extend(pieces_par_rarete[1] * 70)
    if pieces_par_rarete[2]:
        pool_pieces.extend(pieces_par_rarete[2] * 25)
    if pieces_par_rarete[3]:
        pool_pieces.extend(pieces_par_rarete[3] * 5)
    
    if not pool_pieces:
        return []
    
    pieces_tirees = []
    noms_tires = set()
    
    tentatives_max = nombre * 10
    tentatives = 0
    
    while len(pieces_tirees) < nombre and tentatives < tentatives_max:
        tentatives += 1
        piece_choisie = random.choice(pool_pieces)
        
        if piece_choisie.nom not in noms_tires:
            pieces_tirees.append(piece_choisie.copier())
            noms_tires.add(piece_choisie.nom)
    
    return pieces_tirees

def verifier_voisinage(dest_pos, grid_pieces, grid_rows, grid_cols):
    """Vérifie les pièces autour d'une position pour contraindre les placements.
    
    Retourne les contraintes de connexion basées sur les pièces voisines existantes.
    
    Args:
        dest_pos (tuple): Position de destination (col, row)
        grid_pieces (dict): Dictionnaire des pièces placées
        grid_rows (int): Nombre de lignes
        grid_cols (int): Nombre de colonnes
        
    Returns:
        dict: Dictionnaire des contraintes {"N": bool, "S": bool, "E": bool, "W": bool}
              True = doit avoir une connexion, False = NE DOIT PAS avoir de connexion, None = pas de contrainte
    """
    col, row = dest_pos
    contraintes = {"N": None, "S": None, "E": None, "W": None}
    
    # Vérifier le Nord
    if row > 0:
        pos_nord = (col, row - 1)
        if pos_nord in grid_pieces:
            piece_nord = grid_pieces[pos_nord]
            # Si la pièce au nord a une connexion Sud, la nouvelle pièce DOIT avoir Nord
            if "S" in piece_nord.directions:
                contraintes["N"] = True
            else:
                contraintes["N"] = False
    else:
        # Bord supérieur de la grille : NE DOIT PAS avoir de connexion Nord
        contraintes["N"] = False
    
    # Vérifier le Sud
    if row < grid_rows - 1:
        pos_sud = (col, row + 1)
        if pos_sud in grid_pieces:
            piece_sud = grid_pieces[pos_sud]
            if "N" in piece_sud.directions:
                contraintes["S"] = True
            else:
                contraintes["S"] = False
    else:
        # Bord inférieur de la grille : NE DOIT PAS avoir de connexion Sud
        contraintes["S"] = False
    
    # Vérifier l'Est
    if col < grid_cols - 1:
        pos_est = (col + 1, row)
        if pos_est in grid_pieces:
            piece_est = grid_pieces[pos_est]
            if "W" in piece_est.directions:
                contraintes["E"] = True
            else:
                contraintes["E"] = False
    else:
        # Bord droit de la grille : NE DOIT PAS avoir de connexion Est
        contraintes["E"] = False
    
    # Vérifier l'Ouest
    if col > 0:
        pos_ouest = (col - 1, row)
        if pos_ouest in grid_pieces:
            piece_ouest = grid_pieces[pos_ouest]
            if "E" in piece_ouest.directions:
                contraintes["W"] = True
            else:
                contraintes["W"] = False
    else:
        # Bord gauche de la grille : NE DOIT PAS avoir de connexion Ouest
        contraintes["W"] = False
    
    return contraintes

def piece_respecte_contraintes(piece, contraintes):
    """Vérifie si une pièce respecte les contraintes de voisinage.
    
    Args:
        piece (Piece): Pièce à vérifier
        contraintes (dict): Contraintes de connexion
        
    Returns:
        bool: True si la pièce respecte toutes les contraintes
    """
    for direction, requis in contraintes.items():
        if requis is True:
            # Cette direction DOIT avoir une connexion
            if direction not in piece.directions:
                return False
        elif requis is False:
            # Cette direction NE DOIT PAS avoir de connexion
            if direction in piece.directions:
                return False
    
    return True

def joueur_tire_pieces(gestionnaire_pieces, dest_pos, grid_pieces, grid_rows, grid_cols, direction):
    """Tire 3 pièces compatibles avec la direction et le voisinage.
    
    Args:
        gestionnaire_pieces (GestionnairePieces): Gestionnaire de pièces
        dest_pos (tuple): Position de destination
        grid_pieces (dict): Pièces déjà placées
        grid_rows (int): Nombre de lignes
        grid_cols (int): Nombre de colonnes
        direction (str): Direction du mouvement
        
    Returns:
        list: Liste des 3 pièces compatibles (orientées automatiquement)
    """
    # Vérifier les contraintes de voisinage
    contraintes = verifier_voisinage(dest_pos, grid_pieces, grid_rows, grid_cols)
    
    # Obtenir toutes les pièces disponibles
    pieces_disponibles = gestionnaire_pieces.get_pieces_disponibles()
    
    if len(pieces_disponibles) == 0:
        return []
    
    # Filtrer et orienter les pièces valides
    pieces_valides = []
    for piece in pieces_disponibles:
        piece_copie = piece.copier()
        piece_copie.changer_orientation(direction)
        
        if piece_respecte_contraintes(piece_copie, contraintes):
            pieces_valides.append(piece_copie)
    
    if len(pieces_valides) == 0:
        return []
    
    # Séparer les pièces par nombre d'ouvertures pour favoriser la diversité
    pieces_2_ouvertures = [p for p in pieces_valides if len(p.directions) == 2]
    pieces_3_ouvertures = [p for p in pieces_valides if len(p.directions) == 3]
    pieces_4_ouvertures = [p for p in pieces_valides if len(p.directions) == 4]
    pieces_1_ouverture = [p for p in pieces_valides if len(p.directions) == 1]
    
    # Tirer 3 pièces en favorisant la variété
    pieces_tirees = []
    noms_tires = set()
    
    # Pool avec pondération : favoriser les pièces avec plus d'ouvertures
    pool_pondere = []
    pool_pondere.extend(pieces_4_ouvertures * 3)  # 3x plus de chance
    pool_pondere.extend(pieces_3_ouvertures * 2)  # 2x plus de chance
    pool_pondere.extend(pieces_2_ouvertures * 1)  # Chance normale
    pool_pondere.extend(pieces_1_ouverture * 1)   # Chance normale
    
    if not pool_pondere:
        pool_pondere = pieces_valides
    
    tentatives = 0
    max_tentatives = 50
    
    while len(pieces_tirees) < 3 and tentatives < max_tentatives:
        tentatives += 1
        piece_choisie = random.choice(pool_pondere)
        
        if piece_choisie.nom not in noms_tires:
            pieces_tirees.append(piece_choisie)
            noms_tires.add(piece_choisie.nom)
    
    # Si on n'a pas assez de pièces différentes, compléter avec ce qu'on a
    while len(pieces_tirees) < 3 and pieces_valides:
        piece_supplementaire = random.choice(pieces_valides)
        pieces_tirees.append(piece_supplementaire.copier())
        if len(pieces_tirees) >= 3:
            break
    
    return pieces_tirees[:3]

def direction_vers_orientation(direction):
    """Convertit une direction de mouvement en orientation cardinale requise.
    
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
    """Distribue aléatoirement des objets dans les pièces selon leurs règles.
    
    Certaines pièces ont des objets garantis:
    - Den: Toujours une gemme
    - Closet: Toujours deux objets aléatoires
    
    Pour les autres pièces:
    - 40% de chance d'avoir un objet (60% avec patte de lapin)
    - Probabilité doublée pour objets métalliques avec détecteur
    
    Args:
        pieces_disponibles (list): Les pièces où placer les objets
        objets_disponibles (list): Les objets pouvant être placés
        joueur (Joueur): Pour vérifier les bonus d'objets
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
                
                # Ajouter la copie directement (préserve l'attribut unique)
                piece.ajouter_objet(objet)
                piece.a_objet = True


def appliquer_effets_pieces_garantis(piece, joueur):
    """Applique les effets garantis d'une pièce au joueur.
    L'effet s'applique à chaque fois que la pièce est placée, même si elle a déjà été visitée.
    
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