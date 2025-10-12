import pygame
import sys
import os
def init_window(grid_rows: int, grid_cols: int, cell_size: int, sidebar_width: int, caption: str = "Blue Prince"):
	"""Initialise la fenêtre de jeu et retourne le surface + tailles calculées.

	Retourne:
		(win, game_width, sidebar_width, total_width, total_height)
	Où game_width = grid_cols * cell_size, total_height = grid_rows * cell_size
	"""
	# s'assurer que pygame est initialisé
	if not pygame.get_init():
		pygame.init()

	game_width = grid_cols * cell_size
	total_width = game_width + sidebar_width
	total_height = grid_rows * cell_size

	win = pygame.display.set_mode((total_width, total_height))
	pygame.display.set_caption(caption)

	return win, game_width, sidebar_width, total_width, total_height


def draw_window(win, joueur, grid_pieces, preview_direction, grid_rows, grid_cols, cell_w, cell_h,
				game_width, sidebar_width, total_width, total_height,
				colors, font):
	"""Rend la grille, le joueur et la zone d'infos.

	colors: dict avec clés 'WHITE','BLACK','GREY','BLUE'
	"""
	WHITE = colors.get('WHITE', (255,255,255))
	BLACK = colors.get('BLACK', (0,0,0))
	GREY = colors.get('GREY', (200,200,200))
	BLUE = colors.get('BLUE', (50,100,200))

	win.fill(WHITE)

	# grille
	for row in range(grid_rows):
		for col in range(grid_cols):
			rect = pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h)
			pygame.draw.rect(win, GREY, rect, 1)

	# Afficher les pièces présentes sur la grille
	for (col, row), piece in grid_pieces.items():
		if piece.icon_img:
			win.blit(piece.icon_img, (col * cell_w, row * cell_h))

	# Dessiner la case actuelle du joueur (légèrement transparente pour voir l'icône derrière)
	pos_actuelle = joueur.position
	rect_joueur = pygame.Rect(pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h, cell_w, cell_h)
	surface_joueur = pygame.Surface((cell_w, cell_h), pygame.SRCALPHA)
	surface_joueur.fill((50, 100, 200, 100)) # Bleu semi-transparent
	win.blit(surface_joueur, rect_joueur.topleft)


	# Dessiner la barre de prévisualisation si une direction est choisie
	if preview_direction:
		bar_thickness = 8
		px, py = pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h
		
		if preview_direction == "haut":
			pygame.draw.line(win, WHITE, (px, py), (px + cell_w, py), bar_thickness)
		elif preview_direction == "bas":
			pygame.draw.line(win, WHITE, (px, py + cell_h), (px + cell_w, py + cell_h), bar_thickness)
		elif preview_direction == "gauche":
			pygame.draw.line(win, WHITE, (px, py), (px, py + cell_h), bar_thickness)
		elif preview_direction == "droite":
			pygame.draw.line(win, WHITE, (px + cell_w, py), (px + cell_w, py + cell_h), bar_thickness)


	# Zone latérale unifiée (sidebar)
	sidebar_x = game_width
	pygame.draw.rect(win, BLACK, (sidebar_x, 0, sidebar_width, total_height), 2)

	# --- Section 1: Infos joueur (Inventaire) ---
	info_y_end = 250 # Hauteur fixe pour cette section
	text = font.render("Inventaire:", True, BLACK)
	win.blit(text, (sidebar_x + 20, 20))

	info_lines = [
		f"Pas : {joueur.pas}",
		f"Or : {joueur.or_}",
		f"Gemmes : {joueur.gemmes}",
		f"Clés : {joueur.cles}",
		f"Dés : {joueur.des}"
	]
	for i, line in enumerate(info_lines):
		txt = font.render(line, True, BLACK)
		win.blit(txt, (sidebar_x + 20, 60 + i * 30))

	pos_text = font.render(f"Position: ({joueur.position[0]}, {joueur.position[1]})", True, BLACK)
	win.blit(pos_text, (sidebar_x + 20, 220))

	# --- Section 2: Aperçu de la pièce ---
	preview_size = sidebar_width - 40 # Un peu de marge
	preview_rect = pygame.Rect(sidebar_x + 20, info_y_end, preview_size, preview_size)
	pygame.draw.rect(win, GREY, preview_rect) # Fond gris
	pygame.draw.rect(win, BLACK, preview_rect, 2) # Bordure

	# Afficher l'aperçu de la pièce actuelle (basé sur la position réelle du joueur)
	piece_actuelle = grid_pieces.get(tuple(joueur.position))
	if piece_actuelle and piece_actuelle.icon_img:
		try:
			# Redimensionner l'icône pour l'aperçu
			large_icon = pygame.transform.scale(piece_actuelle.icon_img, (preview_size, preview_size))
			win.blit(large_icon, preview_rect.topleft)
		except Exception as e:
			print(f"Erreur chargement image pour l'aperçu: {e}")
	else:
		no_preview_text = font.render("Aucun aperçu", True, BLACK)
		win.blit(no_preview_text, (preview_rect.x + 10, preview_rect.y + 10))


	# --- Section 3: Menu d'actions ---
	menu_y_start = info_y_end + preview_size + 20 # Commence après l'aperçu
	menu_rect = pygame.Rect(sidebar_x, menu_y_start, sidebar_width, total_height - menu_y_start)
	# pygame.draw.rect(win, GREY, menu_rect) # Fond gris pour le menu
	pygame.draw.rect(win, BLACK, (sidebar_x, menu_y_start - 1, sidebar_width, total_height - menu_y_start + 1), 2) # Bordure noire

	menu_text = font.render("Menu Actions", True, BLACK)
	win.blit(menu_text, (menu_rect.x + 10, menu_rect.y + 10))

	pygame.display.update()