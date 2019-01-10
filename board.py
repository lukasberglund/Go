from copy import deepcopy


class Board():
    def __init__(self):
        self.grid = [empties(9) for _ in range(9)]
        self.points = {'black': 0, 'white': 0}
        self.temp_stone = 0
        self.groups = []

    def get_state(self, coord):
        x, y = coord
        return self.grid[y][x]

    def set_state(self, coord, state):
        x, y = coord
        self.grid[y][x] = state

    def copy(self):
        copy = Board()
        copy.grid = deepcopy(self.grid)
        copy.groups = deepcopy(self.groups)
        copy.points = self.points.copy()
        return copy

    def __eq__(self, other):
        return self.grid == other.grid


def empties(x):
    return ['empty' for _z in range(x)]
