import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window , adapter_resolution
from joueur import Joueur
from pieces import Piece, charger_pieces_blue_prince, placer_objets_aleatoires, appliquer_effets_pieces_garantis, retirer_objets_uniques_de_toutes_pieces
from objets import gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage, cle, de
from victoire import verifier_victoire, afficher_victoire, verifier_defaite, afficher_defaite, afficher_texte_quitter
from rarete import GestionnairePieces

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
    clock = pygame.time.Clock()
    joueur = Joueur()
    preview_direction = None
    pieces_tirees = []
    piece_selectionnee_index = None
    en_attente_selection = False
    jeu_termine = False

    # Charger toutes les pièces
    toutes_les_pieces = charger_pieces_blue_prince(cell_w, cell_h, Piece)
    
    # Créer le gestionnaire de pièces avec système de deck limité
    gestionnaire_pieces = GestionnairePieces(toutes_les_pieces)
    
    # Liste des objets disponibles
    objets_disponibles = [cle, de, gemme, pomme, banane, detecteur_metaux, patte_lapin, kit_crochetage]
    
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

    # Ensemble pour suivre les pièces déjà visitées et ayant eu leurs effets appliqués
    pieces_effets_appliques = set()
    
    # Dictionnaire pour stocker les objets trouvés par pièce (pour l'affichage)
    objets_trouves_par_piece = {}
    
    # Position précédente pour détecter les changements de pièce
    position_precedente = tuple(joueur.position)
    
    while True:
        clock.tick(30)
        
        # Vérification de la victoire
        if not jeu_termine and verifier_victoire(joueur, grid_pieces):
            afficher_victoire(WIN, WIDTH, HEIGHT)
            afficher_texte_quitter(WIN, WIDTH, HEIGHT)
            jeu_termine = True
        
        # Vérification de la défaite
        if not jeu_termine and verifier_defaite(joueur):
            afficher_defaite(WIN, WIDTH, HEIGHT)
            afficher_texte_quitter(WIN, WIDTH, HEIGHT)
            jeu_termine = True
        
        # Si le jeu est terminé, gérer uniquement la fermeture
        if jeu_termine:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            continue

        # Gérer les mouvements et interactions avec la grille
        preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, grid_pieces = controles.mouvement(
            joueur, preview_direction, GRID_ROWS, GRID_COLS, 
            gestionnaire_pieces, pieces_tirees, en_attente_selection, 
            piece_selectionnee_index, grid_pieces, objets_disponibles
        )

        pos_tuple = tuple(joueur.position)
        
        # Détecter si le joueur a changé de pièce
        if pos_tuple != position_precedente:
            position_precedente = pos_tuple
            
            # Vérifier si le joueur est dans une pièce
            if pos_tuple in grid_pieces:
                piece_actuelle = grid_pieces[pos_tuple]
                
                # Collecter les objets dans la pièce (une seule fois par pièce)
                if pos_tuple not in objets_trouves_par_piece:
                    messages_trouves = []
                    objets_trouves_noms = []
                    
                    # Appliquer les effets garantis de la pièce (première visite seulement pour l'affichage)
                    message_effet = appliquer_effets_pieces_garantis(piece_actuelle, joueur)
                    if message_effet:
                        objets_trouves_noms.append(message_effet)
                    
                    # Collecter les objets
                    for objet in piece_actuelle.objets:
                        if not objet.is_collected:
                            # Vérifier d'abord si l'objet unique est déjà possédé
                            if objet.unique:
                                deja_possede = False
                                if objet.nom == 'detecteur de metaux' and joueur.chance_metaux == 2:
                                    deja_possede = True
                                elif objet.nom == 'patte de lapin' and joueur.chance_objets == 2:
                                    deja_possede = True
                                elif objet.nom == 'kit de crochetage' and joueur.kit_crochetage == 1:
                                    deja_possede = True
                                
                                if deja_possede:
                                    objet.is_collected = True  # Marquer comme collecté pour ne plus le voir
                                    continue  # Passer à l'objet suivant
                            
                            nom_affiche = objet.appliquer_effet(joueur)
                            if nom_affiche:
                                objets_trouves_noms.append(nom_affiche)
                                
                                # Si c'est un objet unique, le retirer de toutes les autres pièces
                                if objet.unique:
                                    retirer_objets_uniques_de_toutes_pieces(grid_pieces, objet.nom)
                    
                    # Créer un seul message avec tous les objets trouvés
                    if objets_trouves_noms:
                        message_final = f"Vous avez trouvé : {', '.join(objets_trouves_noms)}"
                        messages_trouves.append(message_final)
                        objets_trouves_par_piece[pos_tuple] = messages_trouves
                else:
                    # Si on revient dans une pièce déjà visitée, appliquer quand même les effets garantis (mais pas d'affichage)
                    appliquer_effets_pieces_garantis(piece_actuelle, joueur)

        # Préparer le texte des objets trouvés pour l'affichage
        texte_objets_trouves = None
        if pos_tuple in objets_trouves_par_piece:
            messages = objets_trouves_par_piece[pos_tuple]
            texte_objets_trouves = "\n".join(messages)

        # Dessiner la fenêtre du jeu avec l'état actuel
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, joueur, grid_pieces, preview_direction, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT,
                            colors, font, pieces_tirees, en_attente_selection, piece_selectionnee_index, texte_objets_trouves)

if __name__ == "__main__":
    main()