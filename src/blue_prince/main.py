import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window


# Dimensions optimisées pour des carrés parfaits et fenêtre verticale
GRID_ROWS, GRID_COLS = 9, 5    # grille 9 x 5 (9 lignes, 5 colonnes)
CELL_SIZE = 100                 # Taille d'une case (carrés de 100x100 pixels - parfait pour images)
INFO_WIDTH = 250                # Zone d'infos = 250px (plus compacte)

# Initialisation de la fenêtre via fenetre.init_window
WIN, GAME_WIDTH, INFO_WIDTH, WIDTH, HEIGHT = init_window(GRID_ROWS, GRID_COLS, CELL_SIZE, INFO_WIDTH)

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

# Position du joueur - démarrage au centre bas
pos_actuelle = [2, 8]  # [colonne, ligne] - milieu de la ligne du bas (colonne 2/5, ligne 8/9)

# draw_window déplacée dans fenetre.py (fenetre_draw_window)

def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)

        # Passer la position et la taille de la grille à la fonction de contrôle
        controles.mouvement(pos_actuelle, GRID_ROWS, GRID_COLS)
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, pos_actuelle, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, INFO_WIDTH, WIDTH, HEIGHT,
                            colors, font)

if __name__ == "__main__":
    main()
