import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window , adapter_resolution
from joueur import Joueur
from pieces import Piece, charger_pieces_blue_prince, joueur_tire_pieces

# Configuration du jeu
GRID_ROWS, GRID_COLS = 9, 5
POURCENTAGE = 0.9
SIDEBAR_WIDTH = 450
_, MAX_HEIGHT = adapter_resolution(POURCENTAGE)
CELL_SIZE = MAX_HEIGHT // GRID_ROWS

WIN, GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT = init_window(
    GRID_ROWS, GRID_COLS, CELL_SIZE, SIDEBAR_WIDTH
)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (50, 100, 200)

cell_w = CELL_SIZE
cell_h = CELL_SIZE

font = pygame.font.SysFont("arial", 24)

def main():
    """Boucle principale du jeu.
    
    Initialise le joueur et les pièces, puis gère la boucle de jeu
    avec affichage et gestion des événements.
    """
    clock = pygame.time.Clock()
    joueur = Joueur()
    preview_direction = None
    pieces_tirees = []
    piece_selectionnee_index = None
    en_attente_selection = False

    toutes_les_pieces = charger_pieces_blue_prince(cell_w, cell_h, Piece)
    
    grid_pieces = {}
    
    # Placement de l'Entrance Hall (départ)
    entrance_hall = next((p for p in toutes_les_pieces if p.nom == "Entrance Hall"), None)
    if entrance_hall:
        entrance_hall.visitee = True
        grid_pieces[(2, 8)] = entrance_hall
    
    # Placement de l'Antechamber (objectif verrouillé)
    antechamber = next((p for p in toutes_les_pieces if p.nom == "Antechamber"), None)
    if antechamber:
        antechamber.visitee = False
        grid_pieces[(2, 0)] = antechamber

    while True:
        clock.tick(30)

        preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, grid_pieces = controles.mouvement(
            joueur, preview_direction, GRID_ROWS, GRID_COLS, 
            toutes_les_pieces, pieces_tirees, en_attente_selection, 
            piece_selectionnee_index, grid_pieces
        )
        
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, joueur, grid_pieces, preview_direction, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT,
                            colors, font, pieces_tirees, en_attente_selection, piece_selectionnee_index)

if __name__ == "__main__":
    main()