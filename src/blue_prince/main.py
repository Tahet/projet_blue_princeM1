import pygame
import sys
import controles as controles
from fenetre import init_window, draw_window as fenetre_draw_window , adapter_resolution, charger_images_objets
from joueur import Joueur
from pieces import Piece, charger_pieces_blue_prince, placer_objets_aleatoires, appliquer_effets_pieces_garantis, retirer_objets_uniques_de_toutes_pieces, joueur_tire_pieces
from objets import gemme, pomme, banane, gateau, sandwich, repas, detecteur_metaux, patte_lapin, kit_crochetage, cle, de
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
    # Initialisation
    charger_images_objets()
    
    clock = pygame.time.Clock()
    joueur = Joueur()
    preview_direction = None
    pieces_tirees = []
    piece_selectionnee_index = None
    en_attente_selection = False
    # Variables système de portes
    en_attente_validation_porte = False
    niveau_verrou_porte = 0
    porte_validee = False
    jeu_termine = False

    # Setup du jeu
    toutes_les_pieces = charger_pieces_blue_prince(cell_w, cell_h, Piece)
    gestionnaire_pieces = GestionnairePieces(toutes_les_pieces)
    objets_disponibles = [cle, de, gemme, pomme, banane, gateau, sandwich, repas, detecteur_metaux, patte_lapin, kit_crochetage]
    grid_pieces = {}
    
    # Placement pièces spéciales
    entrance_hall = next((p for p in toutes_les_pieces if p.nom == "Entrance Hall"), None)
    if entrance_hall:
        entrance_hall.visitee = True
        grid_pieces[(2, 8)] = entrance_hall
        gestionnaire_pieces.initialiser_verrous_piece(entrance_hall, 8)

    antechamber = next((p for p in toutes_les_pieces if p.nom == "Antechamber"), None)
    if antechamber:
        antechamber.visitee = False
        grid_pieces[(2, 0)] = antechamber
        gestionnaire_pieces.initialiser_verrous_piece(antechamber, 0)

    # Variables de suivi
    objets_trouves_par_piece = {}
    piece_actuelle_affichage = None
    position_precedente = tuple(joueur.position)
    
    while True:
        clock.tick(30)
        
        # Vérifications victoire/défaite
        if not jeu_termine and verifier_victoire(joueur, grid_pieces):
            afficher_victoire(WIN, WIDTH, HEIGHT)
            afficher_texte_quitter(WIN, WIDTH, HEIGHT)
            jeu_termine = True
        
        if not jeu_termine and verifier_defaite(joueur):
            afficher_defaite(WIN, WIDTH, HEIGHT)
            afficher_texte_quitter(WIN, WIDTH, HEIGHT)
            jeu_termine = True
        
        if jeu_termine:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    continue
            continue

        # Gestion des contrôles
        (preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, 
         grid_pieces, en_attente_validation_porte, niveau_verrou_porte, porte_validee) = controles.mouvement(
            joueur, preview_direction, GRID_ROWS, GRID_COLS, 
            gestionnaire_pieces, pieces_tirees, en_attente_selection, 
            piece_selectionnee_index, grid_pieces, objets_disponibles,
            en_attente_validation_porte, niveau_verrou_porte
        )

        # Traitement validation porte
        if porte_validee and preview_direction is not None:
            # Calcul destination
            temp_pos = list(joueur.position)
            dest_pos = None
            
            if preview_direction == "haut":
                dest_pos = (temp_pos[0], temp_pos[1] - 1)
            elif preview_direction == "bas":
                dest_pos = (temp_pos[0], temp_pos[1] + 1)
            elif preview_direction == "gauche":
                dest_pos = (temp_pos[0] - 1, temp_pos[1])
            elif preview_direction == "droite":
                dest_pos = (temp_pos[0] + 1, temp_pos[1])
            
            # Ouverture porte actuelle
            piece_actuelle = grid_pieces.get(tuple(joueur.position))
            if piece_actuelle:
                direction_sortie_map = {
                    "haut": "N",
                    "bas": "S",
                    "gauche": "W",
                    "droite": "E"
                }
                direction_sortie = direction_sortie_map.get(preview_direction)
                if direction_sortie and hasattr(piece_actuelle, 'portes_ouvertes'):
                    piece_actuelle.portes_ouvertes[direction_sortie] = True
            
            # Vérification ouverture destination
            if dest_pos and dest_pos in grid_pieces:
                piece_destination = grid_pieces[dest_pos]
                direction_entree_requise = {
                    "haut": "S",
                    "bas": "N",
                    "gauche": "E",
                    "droite": "W"
                }
                direction_requise = direction_entree_requise.get(preview_direction)
                
                # Si la pièce destination n'a pas d'ouverture correspondante, annuler
                if direction_requise and direction_requise not in piece_destination.directions:
                    print("Porte déverrouillée mais mur derrière !")
                    preview_direction = None
                    porte_validee = False
                    continue
            
            # Tirage 3 pièces si case vide
            if dest_pos and dest_pos not in grid_pieces:
                pieces_tirees = joueur_tire_pieces(gestionnaire_pieces, dest_pos, grid_pieces, GRID_ROWS, GRID_COLS, preview_direction, joueur)
                
                if len(pieces_tirees) > 0:
                    en_attente_selection = True
                    piece_selectionnee_index = 0
                else:
                    print("Aucune pièce disponible !")
                    preview_direction = None
            # Déplacement si pièce existante
            elif dest_pos and dest_pos in grid_pieces:
                if joueur.deplacer(preview_direction):
                    joueur.utiliser_pas()
                    piece_destination = grid_pieces[dest_pos]
                    
                    # Marquage Antechamber pour victoire
                    if piece_destination.nom == "Antechamber":
                        piece_destination.visitee = True
                    
                    direction_entree_map = {
                        "haut": "S",
                        "bas": "N",
                        "gauche": "E",
                        "droite": "W"
                    }
                    direction_entree = direction_entree_map.get(preview_direction)
                    if direction_entree and hasattr(piece_destination, 'portes_ouvertes'):
                        if direction_entree in piece_destination.portes_ouvertes:
                            piece_destination.portes_ouvertes[direction_entree] = True
                    
                    preview_direction = None

        pos_tuple = tuple(joueur.position)
        
        # Détection changement de pièce
        if pos_tuple != position_precedente:
            position_precedente = pos_tuple
            
            # Collecte objets nouvelle pièce
            if pos_tuple in grid_pieces:
                piece_actuelle = grid_pieces[pos_tuple]
                
                # Première visite seulement
                if pos_tuple not in objets_trouves_par_piece:
                    objets_trouves_noms = []
                    
                    # Effets garantis pièce
                    message_effet = appliquer_effets_pieces_garantis(piece_actuelle, joueur)
                    if message_effet:
                        objets_trouves_noms.append(message_effet)
                    
                    # Collecte objets
                    for objet in piece_actuelle.objets:
                        if not objet.is_collected:
                            # Vérification objets uniques
                            if objet.unique:
                                deja_possede = False
                                if objet.nom == 'detecteur de metaux' and joueur.chance_metaux == 2:
                                    deja_possede = True
                                elif objet.nom == 'patte de lapin' and joueur.chance_objets == 2:
                                    deja_possede = True
                                elif objet.nom == 'kit de crochetage' and joueur.kit_crochetage == 1:
                                    deja_possede = True
                                
                                if deja_possede:
                                    objet.is_collected = True
                                    continue
                            
                            nom_affiche = objet.appliquer_effet(joueur)
                            if nom_affiche:
                                objets_trouves_noms.append(nom_affiche)
                                if objet.unique:
                                    retirer_objets_uniques_de_toutes_pieces(grid_pieces, objet.nom)
                    
                    # Message collecte
                    if objets_trouves_noms:
                        objets_trouves_par_piece[pos_tuple] = f"Vous avez trouvé : {', '.join(objets_trouves_noms)}"
                        piece_actuelle_affichage = pos_tuple
                    else:
                        objets_trouves_par_piece[pos_tuple] = True
                        piece_actuelle_affichage = None
                else:
                    piece_actuelle_affichage = None
        
        # Affichage message collecte
        texte_objets_trouves = None
        if piece_actuelle_affichage == pos_tuple and pos_tuple in objets_trouves_par_piece:
            if isinstance(objets_trouves_par_piece[pos_tuple], str):
                texte_objets_trouves = objets_trouves_par_piece[pos_tuple]

        # Message validation porte
        message_porte = None
        if en_attente_validation_porte:
            if niveau_verrou_porte == 0:
                message_porte = "Porte Ouverte\n\nEspace pour passer"
            elif niveau_verrou_porte == 1:
                if joueur.kit_crochetage == 1:
                    message_porte = "Porte Verrouillée\n\nKit de Crochetage\n(Espace)"
                else:
                    message_porte = f"Porte Verrouillée\n\n1 clé requise\n({joueur.cles} clé(s))\n\nEspace: ouvrir | Échap: annuler"
            elif niveau_verrou_porte == 2:
                message_porte = f"Porte Double Verrou\n\n1 clé requise\n(Kit inutile)\n({joueur.cles} clé(s))\n\nEspace: ouvrir | Échap: annuler"

        # Affichage
        colors = {'WHITE': WHITE, 'BLACK': BLACK, 'GREY': GREY, 'BLUE': BLUE}
        fenetre_draw_window(WIN, joueur, grid_pieces, preview_direction, GRID_ROWS, GRID_COLS, cell_w, cell_h,
                            GAME_WIDTH, SIDEBAR_WIDTH, WIDTH, HEIGHT,
                            colors, font, pieces_tirees, en_attente_selection, piece_selectionnee_index, 
                            texte_objets_trouves, message_porte)

if __name__ == "__main__":
    main()