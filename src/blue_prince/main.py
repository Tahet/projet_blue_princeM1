import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window


# Dimensions optimisées pour des carrés parfaits et fenêtre verticale
GRID_ROWS, GRID_COLS = 9, 5    # grille 9 x 5 (9 lignes, 5 colonnes)
CELL_SIZE = 100                 # Taille d'une case (carrés de 100x100 pixels - parfait pour images)
INFO_WIDTH = 250                # Zone d'infos = 250px (plus compacte)

<<<<<<< HEAD
# Initialisation de la fenêtre via fenetre.init_window
WIN, GAME_WIDTH, INFO_WIDTH, WIDTH, HEIGHT = init_window(GRID_ROWS, GRID_COLS, CELL_SIZE, INFO_WIDTH)

=======
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Prince")
#fedgr
>>>>>>> 7fefb32fdf3d3c5bc73227f7164d7eca82e6aa22
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

<<<<<<< HEAD
# draw_window déplacée dans fenetre.py (fenetre_draw_window)
=======
def draw_window():
    WIN.fill(WHITE)

    # === Grille du manoir ===
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h)
            pygame.draw.rect(WIN, GREY, rect, 1)
#ghhs
    # Case du joueur
    rect_courant = pygame.Rect(pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h, cell_w, cell_h)
    pygame.draw.rect(WIN, BLUE, rect_courant)

    # === Zone d'infos ===
    pygame.draw.rect(WIN, BLACK, (GAME_WIDTH, 0, INFO_WIDTH, HEIGHT), 2)

    # Texte inventaire
    text = font.render("Inventaire:", True, BLACK)
    WIN.blit(text, (GAME_WIDTH + 20, 20))

    info_lines = [
        "Pas : 70",
        "Or : 0", 
        "Gemmes : 2",
        "Clés : 0",
        "Dés : 0"
    ]
    for i, line in enumerate(info_lines):
        txt = font.render(line, True, BLACK)
        WIN.blit(txt, (GAME_WIDTH + 20, 60 + i * 30))


    pygame.display.update()
>>>>>>> 7fefb32fdf3d3c5bc73227f7164d7eca82e6aa22

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
