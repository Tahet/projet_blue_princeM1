import pygame
import sys

def mouvement(pos_actuelle, grid_rows, grid_cols):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pos_actuelle[1] > 0:
                pos_actuelle[1] -= 1
            elif event.key == pygame.K_q and pos_actuelle[0] > 0:
                pos_actuelle[0] -= 1
            elif event.key == pygame.K_s and pos_actuelle[1] < grid_rows - 1:
                pos_actuelle[1] += 1
            elif event.key == pygame.K_d and pos_actuelle[0] < grid_cols - 1:
                pos_actuelle[0] += 1