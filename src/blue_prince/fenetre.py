import pygame
import sys
import os

# Cache global pour les images des objets
IMAGES_OBJETS = {}

def charger_images_objets():
    """Charge les images des objets depuis le dossier data."""
    global IMAGES_OBJETS
    
    # Mappage des noms d'objets aux noms de fichiers
    objets_mapping = {
        "pas": "pas.png",
        "or": "Or .webp",
        "gemme": "Gemme.png",
        "clé": "Clés.webp",
        "dé": "Dés.png",
        "kit_crochetage": "kit Crochetage.jpeg",
        "detecteur_metaux": "Détecteur Métaux.png",
        "patte_lapin": "Patte de lapin.png"
    }
    
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    for key, filename in objets_mapping.items():
        filepath = os.path.join(data_dir, filename)
        try:
            if os.path.exists(filepath):
                img = pygame.image.load(filepath)
                IMAGES_OBJETS[key] = img
            else:
                print(f"Fichier image non trouvé: {filepath}")
        except Exception as e:
            print(f"Erreur chargement image {filename}: {e}")

def adapter_resolution(pourcentage: float):
    """Récupère la résolution de l'écran et retourne une fraction spécifiée."""
    if not pygame.get_init():
        pygame.init()
        
    info = pygame.display.Info()
    max_width = int(info.current_w * pourcentage)
    max_height = int(info.current_h * pourcentage)
    
    return max_width, max_height

def init_window(grid_rows: int, grid_cols: int, cell_size: int, sidebar_width: int, caption: str = "Blue Prince"):
    """Initialise la fenêtre pygame.
    
    Args:
        grid_rows (int): Nombre de lignes de la grille
        grid_cols (int): Nombre de colonnes de la grille
        cell_size (int): Taille d'une cellule en pixels
        sidebar_width (int): Largeur de la sidebar en pixels
        caption (str): Titre de la fenêtre
        
    Returns:
        tuple: (win, game_width, sidebar_width, total_width, total_height)
    """
    if not pygame.get_init():
        pygame.init()

    game_width = grid_cols * cell_size
    total_width = game_width + sidebar_width
    total_height = grid_rows * cell_size

    win = pygame.display.set_mode((total_width, total_height))
    pygame.display.set_caption(caption)

    return win, game_width, sidebar_width, total_width, total_height

def obtenir_effet_piece(nom_piece):
    """Retourne l'effet garanti d'une pièce pour l'affichage.
    
    Args:
        nom_piece (str): Nom de la pièce
        
    Returns:
        str: Description de l'effet ou None
    """
    effets = {
        "Bedroom": "Effet: +2 pas",
        "Pantry": "Effet: +4 or",
        "Chapel": "Effet: -1 or",
        "Rumpus Room": "Effet: +8 or",
        "Nook": "Effet: +1 clé",
        "Trophy Room": "Effet: +8 gemmes",
        "Garage": "Effet: +2 clés",
        "Locksmith": "Effet: Acheter 1 clé pour 5 or",
        "Kitchen": "Effet: Acheter banane pour 3 or (+5 pas)",
        "Weight Room": "Effet: Pas divisés par 2",
        "Vault": "Effet: +40 or",
        "Den": "Effet: +1 gemme garantie",
        "Closet": "Effet: 2 objets aléatoires",
        "Storeroom": "Effet: +1 or, +1 gemme, +1 clé"
    }
    return effets.get(nom_piece, None)

def draw_rounded_rect(surface, color, rect, border_radius=10, width=0):
    """Dessine un rectangle avec coins arrondis.
    
    Args:
        surface: Surface pygame
        color: Couleur RGB
        rect: Rectangle pygame.Rect
        border_radius: Rayon des coins arrondis
        width: Épaisseur (0 pour remplissage)
    """
    if border_radius == 0:
        pygame.draw.rect(surface, color, rect, width)
        return
    
    # Limiter le rayon aux dimensions du rectangle
    border_radius = min(border_radius, rect.width // 2, rect.height // 2)
    
    # Créer une surface avec transparence
    rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    
    if width == 0:  # Remplissage
        pygame.draw.rect(rect_surface, color, (0, 0, rect.width, rect.height), border_radius=border_radius)
    else:  # Bordure
        pygame.draw.rect(rect_surface, color, (0, 0, rect.width, rect.height), width, border_radius=border_radius)
    
    surface.blit(rect_surface, rect.topleft)

def draw_window(win, joueur, grid_pieces, preview_direction, grid_rows, grid_cols, cell_w, cell_h,
                game_width, sidebar_width, total_width, total_height,
                colors, font, pieces_tirees=None, en_attente_selection=False, piece_selectionnee_index=None, 
                texte_objets_trouves=None, message_porte=None):
    """Affiche tous les éléments du jeu.
    """
    WHITE = colors.get('WHITE', (255,255,255))
    BLACK = colors.get('BLACK', (0,0,0))
    GREY = colors.get('GREY', (200,200,200))
    BLUE = colors.get('BLUE', (50,100,200))
    DARK_BLUE = (30, 80, 150)
    win.fill(WHITE)

    # Grille de jeu (inchangée)
    for row in range(grid_rows):
        for col in range(grid_cols):
            rect = pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h)
            pygame.draw.rect(win, GREY, rect, 1)

    # Pièces sur la grille (inchangée)
    for (col, row), piece in grid_pieces.items():
        if piece.icon_img:
            win.blit(piece.icon_img, (col * cell_w, row * cell_h))

    # Position actuelle du joueur (inchangée)
    pos_actuelle = joueur.position
    rect_joueur = pygame.Rect(pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h, cell_w, cell_h)
    surface_joueur = pygame.Surface((cell_w, cell_h), pygame.SRCALPHA)
    surface_joueur.fill((50, 100, 200, 100))
    win.blit(surface_joueur, rect_joueur.topleft)

    # Indicateur de direction (barre blanche) (inchangée)
    if preview_direction:
        bar_thickness = 8
        px, py = pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h
        
        if preview_direction == "haut":
            pygame.draw.line(win, WHITE, (px, py), (px + cell_w, py), bar_thickness)
        elif preview_direction == "bas":
            pygame.draw.line(win, WHITE, (px, py + cell_h), (px + cell_w, py + cell_h), bar_thickness)
        elif preview_direction == "gauche":
            pygame.draw.line(win, WHITE, (px, py), (px, py + cell_h), bar_thickness)
        elif preview_direction == "droite":
            pygame.draw.line(win, WHITE, (px + cell_w, py), (px + cell_w, py + cell_h), bar_thickness)

    # Sidebar (inchangée)
    sidebar_x = game_width
    pygame.draw.rect(win, BLACK, (sidebar_x, 0, sidebar_width, total_height), 2)

    # Constantes pour la nouvelle mise en page
    info_y_end = 275  # Réduit pour moins d'espace blanc
    TEXT_PADDING = 15
    TEXT_ZONE_WIDTH = 240

    # ========== SECTION INVENTAIRE ==========
    # Fond dégradé pour la sidebar (section inventaire)
    sidebar_bg = pygame.Surface((sidebar_width, info_y_end))
    sidebar_bg.fill((240, 248, 255))  # Alice blue - couleur très légère
    win.blit(sidebar_bg, (sidebar_x, 0))
    
    # Ligne de démarcation en bas de l'inventaire
    pygame.draw.line(win, DARK_BLUE, (sidebar_x + 2, info_y_end - 1), (sidebar_x + sidebar_width - 2, info_y_end - 1), 2)

    # Section inventaire (Lignes de texte avec images)
    debut_texte = sidebar_x + TEXT_PADDING
    
    # Titre de l'inventaire avec un petit fond coloré
    inv_title_bg = pygame.Rect(debut_texte - 5, 8, 220, 35)
    pygame.draw.rect(win, (200, 220, 255), inv_title_bg, border_radius=8)
    pygame.draw.rect(win, DARK_BLUE, inv_title_bg, 2, border_radius=8)
    
    inv_title_font = pygame.font.SysFont("arial", 20, bold=True)
    text = inv_title_font.render("Inventaire", True, DARK_BLUE)
    win.blit(text, (debut_texte, 12))

    # Utiliser une police plus petite pour l'inventaire
    info_font = pygame.font.SysFont("arial", 14)
    
    # Taille des petites images d'objets
    icon_size = 22
    
    # Données d'inventaire avec les clés pour accéder aux images
    info_items = [
        ("Pas", joueur.pas, "pas"),
        ("Or", joueur.or_, "or"),
        ("Gemmes", joueur.gemmes, "gemme"),
        ("Clés", joueur.cles, "clé"),
        ("Dés", joueur.des, "dé"),
        ("Kit Crochetage", "Oui" if joueur.kit_crochetage > 0 else "Non", "kit_crochetage"),
        ("Detecteur Metaux", "Oui" if joueur.chance_metaux > 1 else "Non", "detecteur_metaux"),
        ("Patte de Lapin", "Oui" if joueur.chance_objets > 1 else "Non", "patte_lapin")
    ]
    
    for i, (label, value, img_key) in enumerate(info_items):
        y_pos = 52 + i * 25
        x_text = debut_texte + icon_size + 8
        
        # Afficher l'image si disponible
        if img_key in IMAGES_OBJETS:
            try:
                img = IMAGES_OBJETS[img_key]
                resized_img = pygame.transform.scale(img, (icon_size, icon_size))
                win.blit(resized_img, (debut_texte, y_pos - 2))
            except Exception as e:
                print(f"Erreur affichage image {img_key}: {e}")
        
        # Afficher le texte
        txt = info_font.render(f"{label} : {value}", True, (40, 40, 80))
        win.blit(txt, (x_text, y_pos))

    pos_font = pygame.font.SysFont("arial", 12, italic=True)
    pos_text = pos_font.render(f"Position: ({joueur.position[0]}, {joueur.position[1]})", True, (100, 100, 120))
    win.blit(pos_text, (debut_texte, 252))

    # Section aperçu de la pièce actuelle (à côté de l'inventaire)
    preview_x = debut_texte + TEXT_ZONE_WIDTH
    preview_y = 15
    
    MAX_IMAGE_HEIGHT = info_y_end - preview_y - 5
    remaining_width = sidebar_width - (TEXT_PADDING + TEXT_ZONE_WIDTH + TEXT_PADDING) 
    
    preview_size = min(MAX_IMAGE_HEIGHT, remaining_width)
    preview_size = max(0, preview_size)

    preview_rect = pygame.Rect(preview_x, preview_y, preview_size, preview_size)
    pygame.draw.rect(win, GREY, preview_rect)
    pygame.draw.rect(win, BLACK, preview_rect, 2)

    piece_actuelle = grid_pieces.get(tuple(joueur.position))
    if piece_actuelle and piece_actuelle.icon_img:
        if preview_size > 0:
            try:
                large_icon = pygame.transform.scale(piece_actuelle.icon_img, (preview_size, preview_size))
                win.blit(large_icon, preview_rect.topleft)
            except Exception as e:
                print(f"Erreur chargement image pour l'aperçu: {e}")
    else:
        no_preview_text = font.render("Aucun aperçu", True, BLACK)
        win.blit(no_preview_text, (preview_rect.x + 10, preview_rect.y + 10))

    # Affichage des objets trouvés dans la pièce actuelle
    if texte_objets_trouves:
        objets_font = pygame.font.SysFont("arial", 14)
        
        objets_y = preview_rect.bottom + 5
        objets_x = preview_rect.x
        
        max_width = preview_size
        toutes_les_lignes = []
        
        messages = texte_objets_trouves.split('\n')
        
        for message in messages:
            mots = message.split()
            ligne_actuelle = ""
            
            for mot in mots:
                test_ligne = ligne_actuelle + " " + mot if ligne_actuelle else mot
                test_surface = objets_font.render(test_ligne, True, BLACK)
                if test_surface.get_width() <= max_width:
                    ligne_actuelle = test_ligne
                else:
                    if ligne_actuelle:
                        toutes_les_lignes.append(ligne_actuelle)
                    ligne_actuelle = mot
            
            if ligne_actuelle:
                toutes_les_lignes.append(ligne_actuelle)
        
        for i, ligne in enumerate(toutes_les_lignes):
            texte_surface = objets_font.render(ligne, True, BLACK)
            win.blit(texte_surface, (objets_x, objets_y + i * 18))

    # Section menu/sélection
    menu_y_start = info_y_end
    menu_rect = pygame.Rect(sidebar_x, menu_y_start, sidebar_width, total_height - menu_y_start)
    
    # Fond bleu clair pour la zone de menu (sans trait de séparation)
    menu_bg_color = (220, 235, 255)  # Bleu très clair
    pygame.draw.rect(win, menu_bg_color, menu_rect)
    
    # Bordure colorée uniquement sur les côtés (pas de séparation avec l'inventaire)
    pygame.draw.line(win, DARK_BLUE, (sidebar_x, menu_y_start), (sidebar_x + sidebar_width, menu_y_start), 0)  # Pas de ligne du haut
    pygame.draw.line(win, DARK_BLUE, (sidebar_x, menu_y_start), (sidebar_x, total_height), 3)  # Gauche
    pygame.draw.line(win, DARK_BLUE, (sidebar_x + sidebar_width, menu_y_start), (sidebar_x + sidebar_width, total_height), 3)  # Droite
    pygame.draw.line(win, DARK_BLUE, (sidebar_x, total_height - 1), (sidebar_x + sidebar_width, total_height - 1), 3)  # Bas

    if message_porte:
        # Fond semi-transparent sur toute la zone de menu
        overlay = pygame.Surface((sidebar_width, total_height - menu_y_start))
        overlay.set_alpha(230)
        overlay.fill((240, 240, 240))
        win.blit(overlay, (sidebar_x, menu_y_start))
        
        # Afficher le message de la porte
        porte_font = pygame.font.SysFont("arial", 18)
        lignes = message_porte.split('\n')
        
        y_offset = menu_rect.y + 20
        for ligne in lignes:
            if ligne.strip():  # Ignorer les lignes vides
                texte = porte_font.render(ligne, True, BLACK)
                # Centrer le texte
                x_offset = sidebar_x + (sidebar_width - texte.get_width()) // 2
                win.blit(texte, (x_offset, y_offset))
                y_offset += 30

    elif en_attente_selection and pieces_tirees:
        # Affichage des 3 pièces disponibles
        titre_font = pygame.font.SysFont("arial", 22, bold=True)
        titre = titre_font.render("Choisissez une pièce:", True, DARK_BLUE)
        win.blit(titre, (menu_rect.x + 10, menu_rect.y + 10))
        
        small_font = pygame.font.SysFont("arial", 14)
        if joueur.des > 0:
            instruction = small_font.render(f"Z/S: Navigation | F: Relancer ({joueur.des} dé)", True, (60, 60, 60))
        else:
            instruction = small_font.render("Z/S: Navigation | Espace: Valider", True, (60, 60, 60))
        win.blit(instruction, (menu_rect.x + 10, menu_rect.y + 35))
        
        piece_font = pygame.font.SysFont("arial", 18, bold=True)
        effet_font = pygame.font.SysFont("arial", 13)
        piece_y = menu_rect.y + 60
        piece_size = 60
        
        LIGHT_GRAY = (240, 240, 245)
        HIGHLIGHT_BLUE = (180, 210, 255)
        CARD_BORDER = (100, 140, 200)
        
        for i, piece in enumerate(pieces_tirees):
            piece_x = menu_rect.x + 10
            
            # Calculer la hauteur de la carte en fonction de l'effet
            effet_piece = obtenir_effet_piece(piece.nom)
            hauteur_carte = piece_size + 60 if effet_piece else piece_size + 40
            
            piece_rect = pygame.Rect(piece_x, piece_y, sidebar_width - 20, hauteur_carte)
            
            # Fond de la carte
            if i == piece_selectionnee_index:
                pygame.draw.rect(win, HIGHLIGHT_BLUE, piece_rect)  # Bleu highlighted
                border_color = DARK_BLUE
                border_width = 3
            else:
                pygame.draw.rect(win, LIGHT_GRAY, piece_rect)
                border_color = CARD_BORDER
                border_width = 2
            
            # Bordure de la carte
            pygame.draw.rect(win, border_color, piece_rect, border_width)
            
            if piece.icon_img:
                try:
                    mini_icon = pygame.transform.scale(piece.icon_img, (piece_size, piece_size))
                    win.blit(mini_icon, (piece_x + 5, piece_y + 5))
                except Exception as e:
                    print(f"Erreur affichage miniature: {e}")
            
            num_text = piece_font.render(f"{i+1}.", True, DARK_BLUE)
            win.blit(num_text, (piece_x + piece_size + 15, piece_y + 5))
            
            nom_text = piece_font.render(piece.nom, True, BLACK)
            win.blit(nom_text, (piece_x + piece_size + 15, piece_y + 25))
            
            cout = getattr(piece, 'cout_gemmes', 0)
            cout_color = DARK_BLUE if joueur.gemmes >= cout else (200, 50, 50)
            cout_text = pygame.font.SysFont("arial", 14).render(f"Coût: {cout} gemmes", True, cout_color)
            win.blit(cout_text, (piece_x + piece_size + 15, piece_y + 45))
            
            if effet_piece:
                effet_text = effet_font.render(effet_piece, True, (0, 120, 0))
                win.blit(effet_text, (piece_x + piece_size + 15, piece_y + 70))
            
            piece_y += hauteur_carte + 10
    else:
        # Menu normal
        menu_title_font = pygame.font.SysFont("arial", 20, bold=True)
        menu_text = menu_title_font.render("Menu Actions", True, DARK_BLUE)
        win.blit(menu_text, (menu_rect.x + 10, menu_rect.y + 10))
        
        instruction_font = pygame.font.SysFont("arial", 15)
        instruction = instruction_font.render("ZQSD: Choisir direction", True, (60, 60, 60))
        win.blit(instruction, (menu_rect.x + 10, menu_rect.y + 45))
        
        instruction2 = instruction_font.render("Espace: Confirmer", True, (60, 60, 60))
        win.blit(instruction2, (menu_rect.x + 10, menu_rect.y + 70))

    pygame.display.update()