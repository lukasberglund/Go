from copy import deepcopy

class Board():

	def __init__(self):
		self.grid = []
		for i in range(9):
			self.grid.append(zeroes(9))
		self.points = {'black': 0, 'white': 0}
		self.temp_stone = 0
		self.groups = []


	def get_state(self, coord):
		n_to_state = {0: 'empty', 1: 'black', 2: 'white'}
		x, y = coord
		return n_to_state[self.grid[y][x]]

	def set_state(self, coord, state):
		state_to_n = {'empty': 0, 'black': 1, 'white': 2}
		x, y = coord
		self.grid[y][x] = state_to_n[state]

	def copy(self):
		copy = Board()
		copy.grid = deepcopy(self.grid)
		copy.groups = deepcopy(self.groups)
		copy.points = self.points.copy()
		return copy

	def __eq__(self, other):
		return self.grid == other.grid


def zeroes(x):
	return [0 for i in range(x)]
