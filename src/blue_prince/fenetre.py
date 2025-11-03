import pygame
import sys
import os

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

def draw_window(win, joueur, grid_pieces, preview_direction, grid_rows, grid_cols, cell_w, cell_h,
                game_width, sidebar_width, total_width, total_height,
                colors, font, pieces_tirees=None, en_attente_selection=False, piece_selectionnee_index=None):
    """Affiche tous les éléments du jeu.
    """
    WHITE = colors.get('WHITE', (255,255,255))
    BLACK = colors.get('BLACK', (0,0,0))
    GREY = colors.get('GREY', (200,200,200))
    BLUE = colors.get('BLUE', (50,100,200))

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
    info_y_end = 250
    TEXT_PADDING = 20 # Marge à gauche et droite
    TEXT_ZONE_WIDTH = 180 # Largeur fixe pour le texte d'inventaire

    # Section inventaire (Lignes de texte)
    debut_texte = sidebar_x + TEXT_PADDING
    
    text = font.render("Inventaire:", True, BLACK)
    win.blit(text, (debut_texte, 20)) # Position 20, 20 inchangée

    info_lines = [
        f"Pas : {joueur.pas}",
        f"Or : {joueur.or_}",
        f"Gemmes : {joueur.gemmes}",
        f"Clés : {joueur.cles}",
        f"Dés : {joueur.des}"
    ]
    for i, line in enumerate(info_lines):
        txt = font.render(line, True, BLACK)
        win.blit(txt, (debut_texte, 60 + i * 30)) # Utilise debut_texte

    pos_text = font.render(f"Position: ({joueur.position[0]}, {joueur.position[1]})", True, BLACK)
    win.blit(pos_text, (debut_texte, 220)) # Utilise debut_texte

    # Section aperçu de la pièce actuelle (Déplacée et redimensionnée)
    
    # Nouvelle position X (après le texte de l'inventaire)
    preview_x = debut_texte + TEXT_ZONE_WIDTH
    preview_y = 20 # Commence en haut, aligné avec "Inventaire:"
    
    # Calcul de la taille de l'aperçu (carré)
    # Hauteur maximale de l'image (alignée sur info_y_end = 250)
    MAX_IMAGE_HEIGHT = info_y_end - preview_y - TEXT_PADDING # 250 - 20 - 20 = 210
    
    # Largeur restante dans la sidebar: sidebar_width - (Marge gauche + Largeur texte + Marge droite)
    remaining_width = sidebar_width - (TEXT_PADDING + TEXT_ZONE_WIDTH + TEXT_PADDING) 
    
    # La taille de l'aperçu sera le minimum entre la hauteur max et la largeur restante
    preview_size = min(MAX_IMAGE_HEIGHT, remaining_width)
    preview_size = max(0, preview_size) # Assure une taille positive

    # Création du rectangle de l'aperçu avec les nouvelles coordonnées et taille
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

    # Section menu/sélection
    # Le menu commence après la fin de la zone d'inventaire/image (info_y_end)
    menu_y_start = info_y_end + TEXT_PADDING # 250 + 20
    menu_rect = pygame.Rect(sidebar_x, menu_y_start, sidebar_width, total_height - menu_y_start)
    
    # Dessin du cadre du menu
    pygame.draw.rect(win, BLACK, (sidebar_x, menu_y_start - 1, sidebar_width, total_height - menu_y_start + 1), 2)

    if en_attente_selection and pieces_tirees:
        # Affichage des 3 pièces disponibles (inchangé)
        titre = font.render("Choisissez une piece:", True, BLACK)
        win.blit(titre, (menu_rect.x + 10, menu_rect.y + 10))
        
        # Instructions en haut (inchangées)
        small_font = pygame.font.SysFont("arial", 16)
        if joueur.des > 0:
            instruction = small_font.render(f"Z/S: Navigation | F: Relancer ({joueur.des} de)", True, BLACK)
        else:
            instruction = small_font.render("Z/S: Navigation | Espace: Valider", True, BLACK)
        win.blit(instruction, (menu_rect.x + 10, menu_rect.y + 35))
        
        piece_font = pygame.font.SysFont("arial", 18)
        piece_y = menu_rect.y + 60
        piece_size = 60
        
        for i, piece in enumerate(pieces_tirees):
            piece_x = menu_rect.x + 10
            piece_rect = pygame.Rect(piece_x, piece_y, sidebar_width - 20, piece_size + 40)
            
            if i == piece_selectionnee_index:
                pygame.draw.rect(win, (200, 220, 255), piece_rect)
            
            pygame.draw.rect(win, BLACK, piece_rect, 2)
            
            if piece.icon_img:
                try:
                    mini_icon = pygame.transform.scale(piece.icon_img, (piece_size, piece_size))
                    win.blit(mini_icon, (piece_x + 5, piece_y + 5))
                except Exception as e:
                    print(f"Erreur affichage miniature: {e}")
            
            num_text = piece_font.render(f"{i+1}.", True, BLACK)
            win.blit(num_text, (piece_x + piece_size + 15, piece_y + 5))
            
            nom_text = piece_font.render(piece.nom, True, BLACK)
            win.blit(nom_text, (piece_x + piece_size + 15, piece_y + 25))
            
            cout = getattr(piece, 'cout_gemmes', 0)
            cout_color = BLACK if joueur.gemmes >= cout else (255, 0, 0)
            cout_text = piece_font.render(f"Cout: {cout} gemmes", True, cout_color)
            win.blit(cout_text, (piece_x + piece_size + 15, piece_y + 45))
            
            piece_y += piece_size + 50
    else:
        # Menu normal (inchangé)
        menu_text = font.render("Menu Actions", True, BLACK)
        win.blit(menu_text, (menu_rect.x + 10, menu_rect.y + 10))
        
        instruction = pygame.font.SysFont("arial", 16).render("ZQSD: Choisir direction", True, BLACK)
        win.blit(instruction, (menu_rect.x + 10, menu_rect.y + 40))
        
        instruction2 = pygame.font.SysFont("arial", 16).render("Espace: Confirmer", True, BLACK)
        win.blit(instruction2, (menu_rect.x + 10, menu_rect.y + 60))

    pygame.display.update()