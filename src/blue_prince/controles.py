import pygame
import sys

def mouvement(joueur, preview_direction, grid_rows, grid_cols):
    """
    Gère les entrées clavier pour la prévisualisation et la confirmation des mouvements.
    - ZQSD définit une direction de prévisualisation.
    - Entrée confirme le mouvement dans cette direction.
    - Echap annule la prévisualisation.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Définir la direction de prévisualisation avec ZQSD
            if event.key == pygame.K_z:
                preview_direction = "haut"
            elif event.key == pygame.K_q:
                preview_direction = "gauche"
            elif event.key == pygame.K_s:
                preview_direction = "bas"
            elif event.key == pygame.K_d:
                preview_direction = "droite"
            
            # Confirmer le mouvement avec Entrée
            elif event.key == pygame.K_RETURN and preview_direction is not None:
                # Tenter de déplacer le joueur dans la direction prévisualisée
                if joueur.deplacer(preview_direction):
                    # Si le mouvement réussit (géré dans la classe Joueur), consommer un pas
                    joueur.utiliser_pas()
                # Après la tentative, annuler la prévisualisation
                preview_direction = None

            # Annuler la prévisualisation avec Echap
            elif event.key == pygame.K_ESCAPE:
                preview_direction = None

    return preview_direction