import argparse
import pygame
import sys
from pygame.locals import QUIT
import os
from modules.game_state import GameState
from modules.game_visualization import GameVisualization
from modules.solver import Solver
import threading
import time

def load_map(map_path):
    """Load the map from the given path"""
    with open(map_path, 'r') as f:
        game_map = [list(line.strip()) for line in f]
    return game_map

WHITE = (255, 255, 255)

def select_strategy(game_map):
    options = ['bfs', 'dfs', 'astar', 'ucs', 'greedy', 'custom']
    selected_strategy = options[0]  # Default selected strategy

    pygame.init()
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont('Arial', 20)

    instructions = [
        "Click on the dropdown to select a strategy.",
        "Use arrow up and down to choose strategy.",
        "Press Enter to select."
    ]

    # Load image assets
    wall_image = pygame.image.load(os.path.join('assets', 'wall.png'))
    box_image = pygame.image.load(os.path.join('assets', 'box.png'))
    target_image = pygame.image.load(os.path.join('assets', 'target.png'))
    player_image = pygame.image.load(os.path.join('assets', 'player_up.png'))
    floor_image = pygame.image.load(os.path.join('assets', 'floor.png'))
    box_on_target_image = pygame.image.load(os.path.join('assets', 'crate_10.png'))
    start_time = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_strategy = options[(options.index(selected_strategy) - 1) % len(options)]
                elif event.key == pygame.K_DOWN:
                    selected_strategy = options[(options.index(selected_strategy) + 1) % len(options)]
                elif event.key == pygame.K_RETURN:
                    start_time = time.time()  # Start the timer
                    return selected_strategy, start_time

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render instructions
        instruction_margin = 10
        instruction_offset_y = screen_height - instruction_margin
        for idx, instruction in enumerate(instructions):
            instruction_text = font.render(instruction, True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(bottomright=(screen_width - instruction_margin, instruction_offset_y - idx * (instruction_text.get_height() + instruction_margin)))
            screen.blit(instruction_text, instruction_rect)

        # Map rendering
        cell_size = 65  # Adjust cell size as needed
        map_offset_x = 50
        map_offset_y = 50

        for row in range(len(game_map)):
            for col in range(len(game_map[row])):
                x = map_offset_x + col * cell_size
                y = map_offset_y + row * cell_size
                if game_map[row][col] == '#':
                    screen.blit(wall_image, (x, y))
                elif game_map[row][col] == '$':
                    screen.blit(box_image, (x, y))
                elif game_map[row][col] == '.':
                    screen.blit(target_image, (x, y))
                elif game_map[row][col] == '*':
                    screen.blit( box_on_target_image , (x, y))
                else:
                    # Draw floor image first
                    screen.blit(floor_image, (x, y))
                    # Then draw other elements
                    if game_map[row][col] == '@':
                        screen.blit(player_image, (x, y))

        # Display selected strategy at the top left
        selected_strategy_text = font.render(f"Selected Strategy: {selected_strategy}", True, (255, 255, 255))
        screen.blit(selected_strategy_text, (instruction_margin, instruction_margin))

        pygame.display.flip()  # Update the display after drawing the map and text

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--map', help='The map file', default='maps/sokoban1.txt')
    args = parser.parse_args()

    game_map = load_map(args.map)
    game_state = GameState(game_map)

    selected_strategy, start_time = select_strategy(game_map)
    print("Selected strategy:", selected_strategy)

    # Print just the name of the map file
    print("Map file:", args.map)

    solver = Solver(game_state, selected_strategy)
    solver.solve()
    solution = solver.get_solution()

    game_visualization = GameVisualization(game_state, solution)

    pygame.init()
    game_visualization.start()
