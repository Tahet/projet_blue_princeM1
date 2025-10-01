import pygame
import sys

# Initialisation
pygame.init()

# Dimensions optimisées pour des carrés parfaits et fenêtre verticale
GRID_ROWS, GRID_COLS = 9, 5    # grille 9 x 5 (9 lignes, 5 colonnes)
CELL_SIZE = 80                  # Taille d'une case (carrés de 80x80 pixels - parfait pour images)
GAME_WIDTH = GRID_COLS * CELL_SIZE  # Zone de jeu = 5 * 80 = 400px
INFO_WIDTH = 250                # Zone d'infos = 250px (plus compacte)
WIDTH = GAME_WIDTH + INFO_WIDTH # Largeur totale = 400 + 250 = 650px
HEIGHT = GRID_ROWS * CELL_SIZE  # Hauteur = 9 * 80 = 720px

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blue Prince")

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

def draw_window():
    WIN.fill(WHITE)

    # === Grille du manoir ===
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h)
            pygame.draw.rect(WIN, GREY, rect, 1)

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

def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and pos_actuelle[1] > 0:
                    pos_actuelle[1] -= 1
                elif event.key == pygame.K_q and pos_actuelle[0] > 0:
                    pos_actuelle[0] -= 1
                elif event.key == pygame.K_s and pos_actuelle[1] < GRID_ROWS - 1:
                    pos_actuelle[1] += 1
                elif event.key == pygame.K_d and pos_actuelle[0] < GRID_COLS - 1:
                    pos_actuelle[0] += 1

        draw_window()

if __name__ == "__main__":
    main()
