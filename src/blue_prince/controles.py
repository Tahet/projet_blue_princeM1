import pygame
import sys
from pieces import joueur_tire_pieces, placer_piece_si_possible

def mouvement(joueur, preview_direction, grid_rows, grid_cols, 
              toutes_les_pieces, pieces_tirees, en_attente_selection, 
              piece_selectionnee_index, grid_pieces):
    """Gère les entrées clavier pour le mouvement et la sélection de pièces.
    
    Deux modes de fonctionnement :
    - Mode normal : ZQSD pour choisir une direction, Espace pour confirmer
    - Mode sélection : Z/S pour naviguer, F pour relancer (si dé disponible), Espace pour valider
    
    Args:
        joueur (Joueur): Instance du joueur
        preview_direction (str): Direction actuellement prévisualisée
        grid_rows (int): Nombre de lignes de la grille
        grid_cols (int): Nombre de colonnes de la grille
        toutes_les_pieces (list): Liste de toutes les pièces du jeu
        pieces_tirees (list): Liste des 3 pièces tirées
        en_attente_selection (bool): True si en mode sélection
        piece_selectionnee_index (int): Index de la pièce sélectionnée (0-2)
        grid_pieces (dict): Dictionnaire (col, row) -> Piece
        
    Returns:
        tuple: (preview_direction, en_attente_selection, pieces_tirees, 
                piece_selectionnee_index, grid_pieces)
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Mode sélection de pièce
            if en_attente_selection:
                # Sélection avec Z (haut) et S (bas)
                if event.key == pygame.K_z and piece_selectionnee_index > 0:
                    piece_selectionnee_index -= 1
                elif event.key == pygame.K_s and piece_selectionnee_index < len(pieces_tirees) - 1:
                    piece_selectionnee_index += 1
                
                # Relancer le tirage avec F si le joueur a un dé
                elif event.key == pygame.K_f and joueur.des > 0:
                    joueur.des -= 1
                    
                    # Nouveau tirage
                    pieces_tirees = joueur_tire_pieces(toutes_les_pieces)
                    
                    for piece in pieces_tirees:
                        piece.changer_orientation(preview_direction)
                    
                    piece_selectionnee_index = 0
                    for i, piece in enumerate(pieces_tirees, 1):
                        cout = getattr(piece, 'cout_gemmes', 0)
                
                # Validation avec Espace
                elif event.key == pygame.K_SPACE and piece_selectionnee_index is not None:
                    piece_choisie = pieces_tirees[piece_selectionnee_index]
                    
                    if placer_piece_si_possible(piece_choisie, joueur, preview_direction):
                        if joueur.deplacer(preview_direction):
                            joueur.utiliser_pas()
                            nouvelle_pos = tuple(joueur.position)
                            piece_choisie.visitee = True
                            grid_pieces[nouvelle_pos] = piece_choisie
                            
                            en_attente_selection = False
                            pieces_tirees = []
                            piece_selectionnee_index = None
                            preview_direction = None
                    else:
                        print(f"Impossible de placer la pièce '{piece_choisie.nom}' - Choisissez une autre pièce")
                
                # Annulation avec Echap
                elif event.key == pygame.K_ESCAPE:
                    en_attente_selection = False
                    pieces_tirees = []
                    piece_selectionnee_index = None
                    preview_direction = None
            
            # Mode normal (prévisualisation)
            else:
                # Choix de direction avec ZQSD
                if event.key == pygame.K_z:
                    preview_direction = "haut"
                elif event.key == pygame.K_q:
                    preview_direction = "gauche"
                elif event.key == pygame.K_s:
                    preview_direction = "bas"
                elif event.key == pygame.K_d:
                    preview_direction = "droite"
                
                # Confirmation avec Espace
                elif event.key == pygame.K_SPACE and preview_direction is not None:
                    # Calcul de la destination
                    temp_pos = list(joueur.position)
                    mouvement_possible = False
                    dest_pos = None
                    
                    if preview_direction == "haut" and temp_pos[1] > 0:
                        dest_pos = (temp_pos[0], temp_pos[1] - 1)
                        mouvement_possible = True
                    elif preview_direction == "bas" and temp_pos[1] < grid_rows - 1:
                        dest_pos = (temp_pos[0], temp_pos[1] + 1)
                        mouvement_possible = True
                    elif preview_direction == "gauche" and temp_pos[0] > 0:
                        dest_pos = (temp_pos[0] - 1, temp_pos[1])
                        mouvement_possible = True
                    elif preview_direction == "droite" and temp_pos[0] < grid_cols - 1:
                        dest_pos = (temp_pos[0] + 1, temp_pos[1])
                        mouvement_possible = True
                    
                    if mouvement_possible and dest_pos:
                        # Vérifier la connexion dans la pièce actuelle
                        piece_actuelle = grid_pieces.get(tuple(joueur.position))
                        if piece_actuelle:
                            direction_sortie = {
                                "haut": "N",
                                "bas": "S",
                                "gauche": "W",
                                "droite": "E"
                            }
                            orientation_requise = direction_sortie.get(preview_direction)
                            
                            if orientation_requise not in piece_actuelle.directions:
                                preview_direction = None
                                continue
                        
                        # Vérifier si la destination existe déjà
                        if dest_pos in grid_pieces:
                            piece_destination = grid_pieces[dest_pos]
                            
                            # Gestion de l'Antechamber verrouillée
                            if piece_destination.nom == "Antechamber" and not piece_destination.visitee:
                                if joueur.cles > 0:
                                    joueur.cles -= 1
                                    piece_destination.visitee = True
                                    if joueur.deplacer(preview_direction):
                                        preview_direction = None
                                else:
                                    print(f"L'Antechamber est verrouillée ! Vous avez besoin d'une clé.")
                                    preview_direction = None
                            else:
                                # Pièce déjà visitée : déplacement simple
                                if joueur.deplacer(preview_direction):
                                    preview_direction = None
                                else:
                                    print("Erreur de déplacement")
                        else:
                            # Case vide : tirage de 3 pièces
                            pieces_tirees = joueur_tire_pieces(toutes_les_pieces)
                            
                            for piece in pieces_tirees:
                                piece.changer_orientation(preview_direction)
                            
                            en_attente_selection = True
                            piece_selectionnee_index = 0
                            for i, piece in enumerate(pieces_tirees, 1):
                                cout = getattr(piece, 'cout_gemmes', 0)
                    else:
                        preview_direction = None
                
                # Annulation avec Echap
                elif event.key == pygame.K_ESCAPE:
                    preview_direction = None

    return preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, grid_pieces