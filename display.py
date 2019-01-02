import pygame, sys, math
import pygame.freetype
from pygame import gfxdraw


class Display():

	def __init__(self, block_width, panel_width, background_color, panel_color):
		self.block_width = block_width
		self.width = block_width * 9
		self.size = (self.width + panel_width, self.width)
		self.buffer_width = block_width // 2
		self.background_color = background_color
		self.stone_radius = self.block_width // 3
		self.screen = pygame.display.set_mode(self.size)

		self.panel_width = panel_width
		self.panel_color = panel_color

		self.temp_stone = 0
		self.temp_color = 0

	def draw(self, board):
		self.screen.fill(self.background_color)
		self.draw_board(board)
		self.draw_panel(board)

	def draw_board(self, board):
		self.draw_lines()
		self.draw_dots()
		self.draw_stones(board)
		if self.temp_stone:
			x, y = self.temp_stone
			self.draw_stone(x, y, self.temp_color)

	def draw_lines(self):
		for i in range(9):
			self.draw_vert_line(i)
			self.draw_hor_line(i)

	def draw_vert_line(self, i):
		black = (0,0,0)
		pygame.draw.aaline(self.screen, black,
			(self.buffer_width + self.block_width * (i), self.buffer_width),
			(self.buffer_width + self.block_width * (i),
			self.width - self.buffer_width), 3)

	def draw_hor_line(self, i):
		black = (0,0,0)
		pygame.draw.aaline(self.screen, black,
			(self.buffer_width, self.buffer_width + self.block_width * (i)),
			(self.width - self.buffer_width,
			self.buffer_width + self.block_width * (i)), 3)

	def draw_dots(self):
		black = (0,0,0)
		dot_radius = self.block_width // 5
		self.draw_dot(black, 2, 2, dot_radius)
		self.draw_dot(black, 2, 6, dot_radius)
		self.draw_dot(black, 6, 2, dot_radius)
		self.draw_dot(black, 6, 6, dot_radius)
		self.draw_dot(black, 4, 4, dot_radius)

	def draw_dot(self, color, x, y, radius):
		pygame.gfxdraw.filled_circle(self.screen,
			self.buffer_width + self.block_width * x,
			self.buffer_width + self.block_width * y,
			radius, color)
		pygame.gfxdraw.aacircle(self.screen,
			self.buffer_width + self.block_width * x,
			self.buffer_width + self.block_width * y,
			radius, color)

	def draw_stones(self, board):
		for x in range(9):
			for y in range(9):
				state = board.get_state((x,y))
				if not state == 'empty':
					self.draw_stone(x, y, state)

	def draw_stone(self, x, y, color):
		if color == 'black':
			rgb = [0,0,0]
		elif color == 'white':
			rgb = [240,240,240]
		self.draw_dot(rgb, x, y, self.stone_radius)

	def draw_panel(self, board):
		self.draw_panel_background()
		self.draw_dividing_line()
		self.draw_points(board)
		self.draw_undo_instruction()
		self.draw_pass_instruction()

	def draw_panel_background(self):
		pygame.draw.rect(self.screen, self.panel_color,
			(self.width, 0, self.width + self.panel_width, self.width))

	def draw_dividing_line(self):
		pygame.draw.aaline(self.screen, (0,0,0),
			(self.width, 0), (self.width, self.width), 10)
		pygame.draw.circle(self.screen, (0,0,0), (self.width + 1, 0), 1)
		pygame.draw.circle(self.screen, (0,0,0), (self.width + 1, self.width), 1)

	def draw_points(self, board):
		helvetica = pygame.freetype.Font('Fonts/Helvetica.ttc',25)
		self.draw_player_points(helvetica, board, 'black', 20)
		self.draw_player_points(helvetica, board, 'white', 55)


	def draw_player_points(self, font, board, player_color, y_coord):
		text = "%s points: %s" %(player_color, str(board.points[player_color]))
		text = text[0].upper() + text[1:]
		font.render_to(self.screen,
			(self.width + self.buffer_width// 2, y_coord),
			text, (0,0,0))

	def draw_undo_instruction(self):
		helvetica = pygame.freetype.Font('Fonts/Helvetica.ttc',25)
		text = "'u' to undo"
		helvetica.render_to(self.screen,
			(self.width + self.buffer_width// 2 + 20, self.width - 60),
			text, (0,0,0))

	def draw_pass_instruction(self):
		helvetica = pygame.freetype.Font('Fonts/Helvetica.ttc',25)
		text = "space to pass"
		helvetica.render_to(self.screen,
			(self.width + self.buffer_width// 2 + 20, self.width - 100),
			text, (0,0,0))

	def flip(self):
		pygame.display.flip()

	def mouse_in_range(self, coord):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		stone_x, stone_y = self.get_state_location(coord)
		d = math.sqrt((mouse_x - stone_x)**2 + (mouse_y - stone_y)**2)
		return d <= self.stone_radius

	def get_state_location(self, coord):
		x, y = coord
		return (self.buffer_width + self.block_width * x,
			self.buffer_width + self.block_width * y)
