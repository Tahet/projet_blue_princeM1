import pygame
import sys
from pieces import joueur_tire_pieces, placer_piece_si_possible, placer_objets_aleatoires

def mouvement(joueur, preview_direction, grid_rows, grid_cols, 
              gestionnaire_pieces, pieces_tirees, en_attente_selection, 
              piece_selectionnee_index, grid_pieces, objets_disponibles,
              en_attente_validation_porte, niveau_verrou_porte):
    """Gère les entrées clavier pour le mouvement et la sélection de pièces."""
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Mode validation de porte (nouveau)
            if en_attente_validation_porte:
                if event.key == pygame.K_SPACE:
                    # Vérifier si le joueur a les ressources nécessaires
                    if niveau_verrou_porte == 0:
                        # Porte ouverte, pas besoin de ressources
                        en_attente_validation_porte = False
                        return (preview_direction, en_attente_selection, pieces_tirees, 
                                piece_selectionnee_index, grid_pieces, False, 0, True)
                    elif niveau_verrou_porte == 1:
                        # Porte verrouillée : kit OU 1 clé
                        if joueur.kit_crochetage == 1:
                            # Utiliser le kit (pas de consommation, permanent)
                            en_attente_validation_porte = False
                            return (preview_direction, en_attente_selection, pieces_tirees, 
                                    piece_selectionnee_index, grid_pieces, False, 0, True)
                        elif joueur.cles >= 1:
                            joueur.cles -= 1
                            en_attente_validation_porte = False
                            return (preview_direction, en_attente_selection, pieces_tirees, 
                                    piece_selectionnee_index, grid_pieces, False, 0, True)
                        else:
                            print("Pas assez de ressources ! (Kit ou 1 clé requis)")
                    elif niveau_verrou_porte == 2:
                        # Porte verrouillée à double tour : 2 clés obligatoires
                        if joueur.cles >= 2:
                            joueur.cles -= 2
                            en_attente_validation_porte = False
                            return (preview_direction, en_attente_selection, pieces_tirees, 
                                    piece_selectionnee_index, grid_pieces, False, 0, True)
                        else:
                            print("Pas assez de clés ! (2 clés requises)")
                
                elif event.key == pygame.K_ESCAPE:
                    # Annuler la sélection de cette porte
                    en_attente_validation_porte = False
                    preview_direction = None
                    return (preview_direction, en_attente_selection, pieces_tirees, 
                            piece_selectionnee_index, grid_pieces, False, 0, False)
            
            # Mode sélection de pièce
            elif en_attente_selection:
                # Sélection avec Z (haut) et S (bas)
                if event.key == pygame.K_z and piece_selectionnee_index > 0:
                    piece_selectionnee_index -= 1
                elif event.key == pygame.K_s and piece_selectionnee_index < len(pieces_tirees) - 1:
                    piece_selectionnee_index += 1
                
                # Relancer le tirage avec F si le joueur a un dé
                elif event.key == pygame.K_f and joueur.des > 0:
                    joueur.des -= 1
                    
                    # Calculer la position future
                    temp_pos = list(joueur.position)
                    if preview_direction == "haut":
                        dest_pos = (temp_pos[0], temp_pos[1] - 1)
                    elif preview_direction == "bas":
                        dest_pos = (temp_pos[0], temp_pos[1] + 1)
                    elif preview_direction == "gauche":
                        dest_pos = (temp_pos[0] - 1, temp_pos[1])
                    elif preview_direction == "droite":
                        dest_pos = (temp_pos[0] + 1, temp_pos[1])
                    
                    # Nouveau tirage avec filtrage et rotation automatique
                    pieces_tirees = joueur_tire_pieces(gestionnaire_pieces, dest_pos, grid_pieces, grid_rows, grid_cols, preview_direction)
                    
                    piece_selectionnee_index = 0
                
                # Validation avec Espace
                elif event.key == pygame.K_SPACE and piece_selectionnee_index is not None and len(pieces_tirees) > 0:
                    piece_choisie = pieces_tirees[piece_selectionnee_index]
                    
                    if placer_piece_si_possible(piece_choisie, joueur, preview_direction):
                        if joueur.deplacer(preview_direction):
                            joueur.utiliser_pas()
                            nouvelle_pos = tuple(joueur.position)
                            piece_choisie.visitee = True
                            grid_pieces[nouvelle_pos] = piece_choisie
                            
                            # Marquer la pièce comme utilisée dans le gestionnaire
                            gestionnaire_pieces.utiliser_piece(piece_choisie.nom)
                            
                            # NOUVEAU : Initialiser les verrous de la pièce
                            gestionnaire_pieces.initialiser_verrous_piece(piece_choisie, nouvelle_pos[1])
                            
                            # Marquer la porte par laquelle on est entré comme ouverte
                            direction_entree_map = {
                                "haut": "S",
                                "bas": "N",
                                "gauche": "E",
                                "droite": "W"
                            }
                            direction_entree = direction_entree_map.get(preview_direction)
                            if direction_entree and direction_entree in piece_choisie.portes_ouvertes:
                                piece_choisie.portes_ouvertes[direction_entree] = True
                            
                            # Placer des objets aléatoires dans la pièce nouvellement placée
                            placer_objets_aleatoires([piece_choisie], objets_disponibles, joueur)
                            
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
                                return (preview_direction, en_attente_selection, pieces_tirees, 
                                        piece_selectionnee_index, grid_pieces, False, 0, False)
                            
                            # NOUVEAU : Vérifier le verrou de cette porte
                            if hasattr(piece_actuelle, 'verrous') and orientation_requise in piece_actuelle.verrous:
                                # Si la porte n'est pas déjà ouverte
                                if not piece_actuelle.portes_ouvertes.get(orientation_requise, False):
                                    niveau_verrou = piece_actuelle.verrous[orientation_requise]
                                    if niveau_verrou is not None:
                                        # Passer en mode validation de porte
                                        en_attente_validation_porte = True
                                        return (preview_direction, en_attente_selection, pieces_tirees, 
                                                piece_selectionnee_index, grid_pieces, True, niveau_verrou, False)
                        
                        # Vérifier si la destination existe déjà
                        if dest_pos in grid_pieces:
                            piece_destination = grid_pieces[dest_pos]
                            
                            # Gestion de l'Antechamber verrouillée (ancien système, garde-le pour compatibilité)
                            if piece_destination.nom == "Antechamber" and not piece_destination.visitee:
                                if joueur.cles > 0:
                                    joueur.cles -= 1
                                    piece_destination.visitee = True
                                    if joueur.deplacer(preview_direction):
                                        joueur.utiliser_pas()
                                        preview_direction = None
                                else:
                                    print(f"L'Antechamber est verrouillée ! Vous avez besoin d'une clé.")
                                    preview_direction = None
                            else:
                                # Pièce déjà visitée : déplacement simple
                                if joueur.deplacer(preview_direction):
                                    joueur.utiliser_pas()
                                    
                                    # Marquer la porte comme ouverte dans la pièce de destination
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
                                else:
                                    print("Erreur de déplacement")
                        else:
                            # Case vide : tirage de 3 pièces avec filtrage intelligent et rotation automatique
                            pieces_tirees = joueur_tire_pieces(gestionnaire_pieces, dest_pos, grid_pieces, grid_rows, grid_cols, preview_direction)
                            
                            if len(pieces_tirees) > 0:
                                en_attente_selection = True
                                piece_selectionnee_index = 0
                            else:
                                print("Aucune pièce valide disponible !")
                                preview_direction = None
                    else:
                        preview_direction = None
                
                # Annulation avec Echap
                elif event.key == pygame.K_ESCAPE:
                    preview_direction = None

    return (preview_direction, en_attente_selection, pieces_tirees, piece_selectionnee_index, 
            grid_pieces, en_attente_validation_porte, niveau_verrou_porte, False)