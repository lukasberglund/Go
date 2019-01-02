#just for reference in case I made something important
"""
	def place_stone(self, coord): #returns True iff a stone was placed
		self.board.set_state(coord, self.color)
		self.take_enemy_pieces(coord)
		if self.is_surrounded(self.get_shape(coord)):
			self.board.set_state(coord, 'empty')
			return False
		else:
			return True

	def take_enemy_pieces(self, stone_added):
		neighboors = self.get_neighboors(stone_added)
		for neighboor in neighboors:
			if self.is_enemy_stone(neighboor, self.color):
				shape = self.get_shape(neighboor)
				if self.is_surrounded(shape):
					self.remove_shape(shape)
"""


class Board():
    def __init__(self, block_width, background_color):
        self.block_width = block_width
        self.width = block_width * 9
        self.size = (self.width, self.width)
        self.buffer_width = block_width // 2

        self.background_color = background_color

        self.screen = pygame.display.set_mode(self.size)
        self.stone_grid = self.init_stone_grid()
        self.stones = flatten(self.stone_grid)

        self.temp_stone = 0

    def draw(self, black_stones, white_stones, color):
        self.screen.fill(self.background_color)
        self.draw_lines()
        self.draw_dots()
        self.draw_stones(black_stones, white_stones)
        if self.temp_stone:
            self.get_stone(self.temp_stone).draw(color)

    def draw_lines(self):
        for i in range(9):
            self.draw_vert_line(i)
            self.draw_hor_line(i)

    def draw_vert_line(self, i):
        black = (0, 0, 0)
        pygame.draw.aaline(
            self.screen, black,
            (self.buffer_width + self.block_width * (i), self.buffer_width),
            (self.buffer_width + self.block_width * (i),
             self.width - self.buffer_width), 3)

    def draw_hor_line(self, i):
        black = (0, 0, 0)
        pygame.draw.aaline(
            self.screen, black,
            (self.buffer_width, self.buffer_width + self.block_width * (i)),
            (self.width - self.buffer_width,
             self.buffer_width + self.block_width * (i)), 3)

    def draw_dots(self):
        black = (0, 0, 0)
        dot_radius = self.block_width // 5
        self.draw_dot(black, 2, 2, dot_radius)
        self.draw_dot(black, 2, 6, dot_radius)
        self.draw_dot(black, 6, 2, dot_radius)
        self.draw_dot(black, 6, 6, dot_radius)
        self.draw_dot(black, 4, 4, dot_radius)

    def get_stone(self, coord):
        x, y = coord
        return self.stone_grid[y][x]

    def draw_dot(self, color, x, y, radius):
        pygame.gfxdraw.filled_circle(
            self.screen, self.buffer_width + self.block_width * x,
            self.buffer_width + self.block_width * y, radius, color)
        pygame.gfxdraw.aacircle(
            self.screen, self.buffer_width + self.block_width * x,
            self.buffer_width + self.block_width * y, radius, color)

    def draw_stones(self, black_stones, white_stones):
        for coord in black_stones:
            self.get_stone(coord).draw('black')
        for coord in white_stones:
            self.get_stone(coord).draw('white')

    def init_stone_grid(self):
        radius = self.block_width // 3
        stones = []
        for x in range(9):
            line = [stone(radius, x, y, self) for y in range(9)]
            stones.append(line)
        return stones

    def get_coord_state(self, x, y):
        return self.stone_grid[y][x].state


class stone(object):
    def __init__(self, radius, x, y, board, state='empty'):
        self.radius = radius
        self.x = x
        self.y = y
        self.x_pixel = board.buffer_width + board.block_width * x
        self.y_pixel = board.buffer_width + board.block_width * y
        self.board = board
        self.state = state
        self.temp_state = 'empty'

    def mouse_in_range(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        d = math.sqrt((mouse_x - self.x_pixel)**2 +
                      (mouse_y - self.y_pixel)**2)
        return d <= self.radius

    def draw(self, color):
        if color == 'black':
            rgb = [0, 0, 0]
        elif color == 'white':
            rgb = [240, 240, 240]
        self.board.draw_dot(rgb, self.x, self.y, self.radius)
