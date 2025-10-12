import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window
from joueur import Joueur
from pieces import Piece, charger_pieces_blue_prince

# Dimensions optimisées pour des carrés parfaits et fenêtre verticale
GRID_ROWS, GRID_COLS = 9, 5    # grille 9 x 5 (9 lignes, 5 colonnes)
CELL_SIZE = 100                 # Taille d'une case (carrés de 100x100 pixels - parfait pour images)
SIDEBAR_WIDTH = 300             # Barre latérale unique pour infos et menu

# Initialisation de la fenêtre via fenetre.init_window
WIN, GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT = init_window(
    GRID_ROWS, GRID_COLS, CELL_SIZE, SIDEBAR_WIDTH
)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (50, 100, 200)

# Taille d'une case (carrés parfaits)
cell_w = CELL_SIZE
cell_h = CELL_SIZE

# Police
font = pygame.font.SysFont("arial", 24)


# draw_window déplacée dans fenetre.py (fenetre_draw_window)

def main():
    clock = pygame.time.Clock()
    joueur = Joueur()
    preview_direction = None  # Stocke la direction de prévisualisation ("haut", "bas", etc.)

    # Charger toutes les pièces du jeu
    toutes_les_pieces = charger_pieces_blue_prince(cell_w, cell_h, Piece)
    
    # Créer une grille qui mappe les coordonnées aux pièces
    # Pour l'instant, on ne place que le hall d'entrée
    grid_pieces = {}
    entrance_hall = next((p for p in toutes_les_pieces if p.nom == "Entrance Hall"), None)
    if entrance_hall:
        grid_pieces[(2, 8)] = entrance_hall

    while True:
        clock.tick(30)

        # La fonction de contrôle met à jour la direction de prévisualisation
        preview_direction = controles.mouvement(joueur, preview_direction, GRID_ROWS, GRID_COLS)
        
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, joueur, grid_pieces, preview_direction, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT,
                            colors, font)

if __name__ == "__main__":
    main()
