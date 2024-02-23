# Visualize the game using pygame
# The game visualization based on game state and solution
#
# Path: modules/game_visualization.py

from typing import List
import pygame
import sys
import os
import time
from pygame.locals import *
from modules.game_state import GameState
from pygame.locals import QUIT


class GameVisualization(object):
    def __init__(self, initial_state: GameState, solution: List[str]):
        self.game_state = initial_state
        self.solution = solution
        self.screen = None
        self.clock = None
        self.font = None
        self.block_size = 50
        self.margin = 5
        self.width = (self.block_size + self.margin) * \
            self.game_state.width + self.margin
        self.height = (self.block_size + self.margin) * \
            self.game_state.height + self.margin
        self.x_offset = (self.width - self.game_state.width *
                         self.block_size - self.margin) / 2
        self.y_offset = (self.height - self.game_state.height *
                         self.block_size - self.margin) / 2

        # Load assets
        self.load_assets()

    def load_assets(self):
        # Load player image with 4 directions
        self.player_up_image = pygame.image.load(
            os.path.join('assets', 'player_up.png'))
        self.player_down_image = pygame.image.load(
            os.path.join('assets', 'player_down.png'))
        self.player_left_image = pygame.image.load(
            os.path.join('assets', 'player_left.png'))
        self.player_right_image = pygame.image.load(
            os.path.join('assets', 'player_right.png'))

        self.wall_image = pygame.image.load(os.path.join('assets', 'wall.png'))
        self.box_image = pygame.image.load(os.path.join('assets', 'box.png'))
        self.box_on_target_image = pygame.image.load(os.path.join('assets', 'crate_10.png'))
        self.target_image = pygame.image.load(
            os.path.join('assets', 'target.png'))
        self.floor_image = pygame.image.load(
            os.path.join('assets', 'floor.png'))

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sokuban')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)

    def draw(self, direction='U'):
        self.screen.fill((0, 0, 0))
        for i in range(self.game_state.height):
            for j in range(self.game_state.width):
                x = self.x_offset + j * (self.block_size + self.margin)
                y = self.y_offset + i * (self.block_size + self.margin)
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                if self.game_state.is_wall((i, j)):
                    self.screen.blit(self.wall_image, rect)
                elif self.game_state.is_box((i, j)):
                    if self.game_state.is_target((i, j)):
                        self.screen.blit(self.box_on_target_image, rect)
                    else:
                        self.screen.blit(self.box_image, rect)
                elif self.game_state.is_target((i, j)):
                    self.screen.blit(self.target_image, rect)
                else:
                    self.screen.blit(self.floor_image, rect)
        player_row, player_col = self.game_state.find_player()
        x = self.x_offset + player_col * (self.block_size + self.margin)
        y = self.y_offset + player_row * (self.block_size + self.margin)
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        if direction == 'U':
            self.screen.blit(self.player_up_image, rect)
        elif direction == 'D':
            self.screen.blit(self.player_down_image, rect)
        elif direction == 'L':
            self.screen.blit(self.player_left_image, rect)
        elif direction == 'R':
            self.screen.blit(self.player_right_image, rect)
        else:
            raise Exception('Invalid direction')
        pygame.display.flip()


    def draw_solution(self):
        if self.solution is None:
            print("No solution available.")
            self.draw_no_solution_image()
            return
        for i in range(len(self.solution)):
            self.game_state = self.game_state.move(self.solution[i])
            self.draw(self.solution[i])
            time.sleep(0.05)
    def draw_no_solution_image(self):
        # Load and display a "No Solution" image
        no_solution_image = pygame.image.load(os.path.join('assets', 'no_solution.png'))
        self.screen.blit(no_solution_image, (0, 0))
        pygame.display.flip()
    def start(self):
        self.init_pygame()
        self.draw()
        self.draw_solution()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(60)
