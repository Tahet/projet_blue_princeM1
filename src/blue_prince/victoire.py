import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def verifier_victoire(joueur, grid_pieces):
    """Vérifie si le joueur a atteint l'Antechamber."""
    piece_actuelle = grid_pieces.get(tuple(joueur.position))
    if piece_actuelle and piece_actuelle.nom == "Antechamber" and piece_actuelle.visitee:
        return True
    return False

def afficher_victoire(win, width, height):
    """Affiche une image de victoire à l'écran."""
    image_victoire = pygame.image.load("src/blue_prince/data/Victory.webp").convert_alpha()
    image_victoire = pygame.transform.scale(image_victoire, (width, height))
    win.blit(image_victoire, (0, 0))
    pygame.display.update()

def verifier_defaite(joueur):
    """Vérifie si le joueur a perdu (plus de pas)."""
    return joueur.pas <= 0

def afficher_defaite(win, width, height):
    """Affiche une image de défaite à l'écran."""
    image_defaite = pygame.image.load("src/blue_prince/data/defeat.png").convert_alpha()
    image_defaite = pygame.transform.scale(image_defaite, (width, height))
    win.blit(image_defaite, (0, 0))
    pygame.display.update()

def afficher_texte_quitter(win, width, height):
    """Affiche le texte 'Appuyez sur ESPACE pour quitter' au centre de l'écran."""
    font_texte = pygame.font.SysFont("garamond", 36, bold=True)
    texte = font_texte.render("Appuyez sur ESPACE pour quitter le jeu", True, WHITE)
    texte_rect = texte.get_rect(center=(width // 2, height - 100))
    
    # Ajouter un fond semi-transparent pour mieux voir le texte
    fond_rect = texte_rect.inflate(40, 20)
    surface_fond = pygame.Surface((fond_rect.width, fond_rect.height))
    surface_fond.set_alpha(200)
    surface_fond.fill(BLACK)
    
    win.blit(surface_fond, fond_rect)
    win.blit(texte, texte_rect)
    pygame.display.update()