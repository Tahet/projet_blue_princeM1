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
#fedgr
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

# Direction sélectionnée avant de bouger
direction_selectionnee = None  # None, 'up', 'left', 'down', 'right'

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
    
    # Indicateur de direction (flèche)
    if direction_selectionnee:
        center_x = pos_actuelle[0] * cell_w + cell_w // 2
        center_y = pos_actuelle[1] * cell_h + cell_h // 2
        arrow_size = 20
        
        if direction_selectionnee == 'up':
            # Flèche vers le haut
            points = [
                (center_x, center_y - arrow_size),
                (center_x - arrow_size // 2, center_y),
                (center_x + arrow_size // 2, center_y)
            ]
        elif direction_selectionnee == 'down':
            # Flèche vers le bas
            points = [
                (center_x, center_y + arrow_size),
                (center_x - arrow_size // 2, center_y),
                (center_x + arrow_size // 2, center_y)
            ]
        elif direction_selectionnee == 'left':
            # Flèche vers la gauche
            points = [
                (center_x - arrow_size, center_y),
                (center_x, center_y - arrow_size // 2),
                (center_x, center_y + arrow_size // 2)
            ]
        elif direction_selectionnee == 'right':
            # Flèche vers la droite
            points = [
                (center_x + arrow_size, center_y),
                (center_x, center_y - arrow_size // 2),
                (center_x, center_y + arrow_size // 2)
            ]
        
        pygame.draw.polygon(WIN, WHITE, points)

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
    global direction_selectionnee
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Sélectionner une direction avec Z/Q/S/D
                if event.key == pygame.K_z and pos_actuelle[1] > 0:
                    direction_selectionnee = 'up'
                elif event.key == pygame.K_q and pos_actuelle[0] > 0:
                    direction_selectionnee = 'left'
                elif event.key == pygame.K_s and pos_actuelle[1] < GRID_ROWS - 1:
                    direction_selectionnee = 'down'
                elif event.key == pygame.K_d and pos_actuelle[0] < GRID_COLS - 1:
                    direction_selectionnee = 'right'
                # Confirmer le déplacement avec Entrée
                elif event.key == pygame.K_RETURN:
                    if direction_selectionnee == 'up' and pos_actuelle[1] > 0:
                        pos_actuelle[1] -= 1
                        direction_selectionnee = None
                    elif direction_selectionnee == 'left' and pos_actuelle[0] > 0:
                        pos_actuelle[0] -= 1
                        direction_selectionnee = None
                    elif direction_selectionnee == 'down' and pos_actuelle[1] < GRID_ROWS - 1:
                        pos_actuelle[1] += 1
                        direction_selectionnee = None
                    elif direction_selectionnee == 'right' and pos_actuelle[0] < GRID_COLS - 1:
                        pos_actuelle[0] += 1
                        direction_selectionnee = None

        draw_window()

if __name__ == "__main__":
    main()
