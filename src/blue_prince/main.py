import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window , adapter_resolution
from joueur import Joueur
from pieces import Piece, charger_pieces_blue_prince, joueur_tire_pieces, placer_objets_aleatoires, appliquer_effets_pieces_garantis
from objets import gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage, cle, de  # Importer les objets

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
    """Boucle principale du jeu."""
    clock = pygame.time.Clock()  # Horloge pour réguler la vitesse du jeu
    joueur = Joueur()  # Création du joueur
    preview_direction = None  # Direction de prévisualisation (pas utilisée ici)
    pieces_tirees = []  # Liste des pièces tirées
    piece_selectionnee_index = None  # Index de la pièce sélectionnée
    en_attente_selection = False  # Indicateur si une pièce est en attente de sélection

    # Charger toutes les pièces
    toutes_les_pieces = charger_pieces_blue_prince(cell_w, cell_h, Piece)
    
    # Liste des objets disponibles
    objets_disponibles = [cle, de, gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage]
    
    grid_pieces = {}  # Dictionnaire pour les pièces placées dans la grille
    
    # Placement de l'Entrance Hall (départ)
    entrance_hall = next((p for p in toutes_les_pieces if p.nom == "Entrance Hall"), None)
    if entrance_hall:
        entrance_hall.visitee = True  # Marquer la pièce comme visitée
        grid_pieces[(2, 8)] = entrance_hall  # Placement dans la grille

    # Placement de l'Antechamber (objectif verrouillé)
    antechamber = next((p for p in toutes_les_pieces if p.nom == "Antechamber"), None)
    if antechamber:
        antechamber.visitee = False  # Ne pas visiter cette pièce au départ
        grid_pieces[(2, 0)] = antechamber  # Placement dans la grille

    # Ensemble pour suivre les pièces déjà visitées et ayant eu leurs effets appliqués
    pieces_effets_appliques = set()
    
    while True:
        clock.tick(30)  # Limiter à 30 images par seconde

        # Gérer les mouvements et interactions avec la grille
        preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, grid_pieces = controles.mouvement(
            joueur, preview_direction, GRID_ROWS, GRID_COLS, 
            toutes_les_pieces, pieces_tirees, en_attente_selection, 
            piece_selectionnee_index, grid_pieces, objets_disponibles
        )

        # Vérifier si le joueur est dans une pièce et appliquer les effets
        pos_tuple = tuple(joueur.position)
        if pos_tuple in grid_pieces:
            piece_actuelle = grid_pieces[pos_tuple]
            
            # Appliquer les effets garantis de la pièce
            if pos_tuple not in pieces_effets_appliques:
                appliquer_effets_pieces_garantis(piece_actuelle, joueur)
                pieces_effets_appliques.add(pos_tuple)
            
            # Collecter les objets dans la pièce
            for objet in piece_actuelle.objets:
                if not objet.is_collected:
                    objet.appliquer_effet(joueur)

        # Dessiner la fenêtre du jeu avec l'état actuel
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, joueur, grid_pieces, preview_direction, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT,
                            colors, font, pieces_tirees, en_attente_selection, piece_selectionnee_index)



if __name__ == "__main__":
    main()
