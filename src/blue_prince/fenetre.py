import pygame
import sys


def init_window(grid_rows: int, grid_cols: int, cell_size: int, info_width: int, caption: str = "Blue Prince"):
	"""Initialise la fenêtre de jeu et retourne le surface + tailles calculées.

	Retourne:
		(win, game_width, info_width, total_width, total_height)
	Où game_width = grid_cols * cell_size, total_height = grid_rows * cell_size
	"""
	# s'assurer que pygame est initialisé
	if not pygame.get_init():
		pygame.init()

	game_width = grid_cols * cell_size
	total_width = game_width + info_width
	total_height = grid_rows * cell_size

	win = pygame.display.set_mode((total_width, total_height))
	pygame.display.set_caption(caption)

	return win, game_width, info_width, total_width, total_height


def draw_window(win, pos_actuelle, grid_rows, grid_cols, cell_w, cell_h,
				game_width, info_width, total_width, total_height,
				colors, font, info_lines=None):
	"""Rend la grille, le joueur et la zone d'infos.

	colors: dict avec clés 'WHITE','BLACK','GREY','BLUE'
	info_lines: liste de chaînes pour la zone d'infos
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

	# joueur
	rect_courant = pygame.Rect(pos_actuelle[0] * cell_w, pos_actuelle[1] * cell_h, cell_w, cell_h)
	pygame.draw.rect(win, BLUE, rect_courant)

	# zone d'infos
	pygame.draw.rect(win, BLACK, (game_width, 0, info_width, total_height), 2)

	# texte inventaire
	if info_lines is None:
		info_lines = [
			"Pas : 70",
			"Or : 0",
			"Gemmes : 2",
			"Clés : 0",
			"Dés : 0"
		]

	text = font.render("Inventaire:", True, BLACK)
	win.blit(text, (game_width + 20, 20))

	for i, line in enumerate(info_lines):
		txt = font.render(line, True, BLACK)
		win.blit(txt, (game_width + 20, 60 + i * 30))

	# position
	pos_text = font.render(f"Position: ({pos_actuelle[0]}, {pos_actuelle[1]})", True, BLACK)
	win.blit(pos_text, (game_width + 20, 220))

	pygame.display.update()