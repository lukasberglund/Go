#to do:
#add scoring
#add sound effect for placing stone
#make temp_stones translucent
#add handicaps

import pygame, sys, math
from pygame import gfxdraw
from display import *
from copy import deepcopy
from board import Board
""" main class for the go game
right now it only does local PvP
use run function to start
keeps going until window is closed
"""


class Game():
    def run(self):
        pygame.init()
        self.board = Board()
        self.display = Display(75, 250, (223, 176, 97), (248, 248, 255))
        self.color = 'black'
        self.board_history = [self.board.copy()]
        self.last_move_was_pass = False

        while True:
            self.display.draw(self.board)
            self.display.flip()
            move = self.get_player_move()
            self.execute_move(move)

    def get_player_move(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.highlight_hovered_stones()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coord = self.get_coord_in_mouse_range()
                    if coord and self.is_empty(coord):
                        return coord
                elif self.is_key_being_pressed(event, 'u'):
                    return 'undo'
                elif self.is_key_being_pressed(event, ' '):
                    return 'pass'

    def highlight_hovered_stones(self):
        self.display.temp_stone = 0
        coord = self.get_coord_in_mouse_range()
        if coord and self.is_empty(coord):
            self.display.temp_stone = (coord)
            self.display.temp_color = self.color
        self.display.draw(self.board)
        self.display.flip()

    def execute_move(self, move):
        if move == 'undo':
            self.undo_move()
            self.last_move_was_pass = False
        elif move == 'pass':
            if self.last_move_was_pass:
                self.score_game()
            self.pass_move()
            self.last_move_was_pass = True
        else:
            if self.place_stone(move):
                if self.violates_KO(self.board):
                    self.board = self.board_history[-1].copy()
                else:
                    self.color = other_color(self.color)
                    self.board_history.append(self.board.copy())
            self.last_move_was_pass = False

    def manage_click(self):
        coord = self.get_coord_in_mouse_range()
        if coord and self.is_empty(coord):
            if self.place_stone(coord):
                if self.violates_KO(self.board):
                    self.board = self.board_history[-1].copy()
                else:
                    self.color = other_color(self.color)
                    self.board_history.append(self.board.copy())

    def get_coord_in_mouse_range(self):
        for x in range(9):
            for y in range(9):
                if self.display.mouse_in_range((x, y)):
                    return (x, y)
        return 0

    def is_empty(self, coord):
        return self.board.get_state(coord) == "empty"

    def place_stone(self, coord):
        """places stone and goes through rules,
		returns true iff a stone was actually placed"""

        self.board.set_state(coord, self.color)
        self.update_groups(coord)

        self.take_enemy_pieces(coord)
        if self.is_surrounded(self.get_group(coord)):
            self.board.set_state(coord, 'empty')
            return False
        else:
            return True

    def update_groups(self, coord):
        adjacent_groups = self.get_adjacent_groups(coord, self.color)
        new_group = [coord]
        for group in adjacent_groups:
            new_group += group
            self.board.groups.remove(group)
        self.board.groups.append(new_group)

    def get_adjacent_groups(self, coord, color):
        adjacent_groups = []
        for neighboor in get_neighboors(coord):
            if self.board.get_state(neighboor) == color:
                group = self.get_group(neighboor)
                if group and not group in adjacent_groups:
                    adjacent_groups.append(group)
        return adjacent_groups

    def get_group(self, coord):
        for group in self.board.groups:
            if coord in group:
                return group
        return 0

    def take_enemy_pieces(self, coord):
        adjacent_enemy_groups = self.get_adjacent_groups(
            coord, other_color(self.color))
        for group in adjacent_enemy_groups:
            if self.is_surrounded(group):
                self.add_points(self.color, len(group))
                self.remove_group(group)

    def is_surrounded(self, group):
        for coord in group:
            for neighboor in get_neighboors(coord):
                if self.board.get_state(neighboor) == 'empty':
                    return False
        return True

    def add_points(self, color, n):
        self.board.points[color] += n

    def remove_group(self, group):
        for coord in group:
            self.board.set_state(coord, 'empty')
        self.board.groups.remove(group)

    def violates_KO(self, board):
        return len(self.board_history) > 1 and board == self.board_history[-2]

    def is_key_being_pressed(self, event, key):
        val = ord(key)
        return event.type == pygame.KEYDOWN and pygame.key.get_pressed()[val]

    def undo_move(self):
        if len(self.board_history) > 1:
            self.board = self.board_history[-2].copy()
            self.board_history = self.board_history[:-1]
            self.color = other_color(self.color)

    def pass_move(self):
        self.board_history.append(self.board)
        self.board = self.board.copy()
        self.color = other_color(self.color)
        self.last_move_was_pass = True

    def score_game(self):
        pass


def get_neighboors(coord):
    x, y = coord
    possible_neighboors = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
    return [c for c in possible_neighboors if is_on_board(c)]


def is_on_board(coord):
    return min(coord) >= 0 and max(coord) <= 8


def other_color(color):
    if color[0] == 'b':  #from which it follows the color must be black
        return 'white'
    else:
        return 'black'


def display_test():
    pygame.init()
    board = Board()
    display = Display(75, (223, 176, 97))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        display.draw(board)
        pygame.display.flip()


def list_print(l):
    for x in l:
        print(x)


game = Game()
game.run()
