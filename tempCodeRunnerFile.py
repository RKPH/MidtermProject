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

def select_strategy():
    options = ['bfs', 'dfs', 'astar', 'ucs', 'greedy', 'custom']
    selected_strategy = options[0]  # Default selected strategy

    pygame.init()
    screen_width = 1400
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont('Arial', 20)

    instructions = [
        "Use arrow left and right to select a map.",
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

    map_paths = ["maps/sokoban1.txt", "maps/sokoban2.txt" , "maps/sokoban3.txt", "maps/sokoban4.txt" , "maps/sokoban_extra1.txt" , "maps/sokoban_extra2.txt"]  # List of available map paths
    map_index = 0  # Index of the currently selected map
    game_map = load_map(map_paths[map_index])  # Initialize game_map

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
                elif event.key == pygame.K_LEFT:
                    map_index = (map_index - 1) % len(map_paths)
                    game_map = load_map(map_paths[map_index])
                elif event.key == pygame.K_RIGHT:
                    map_index = (map_index + 1) % len(map_paths)
                    game_map = load_map(map_paths[map_index])
                elif event.key == pygame.K_RETURN:
                    start_time = time.time()  # Start the timer
                    return selected_strategy, game_map, start_time

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render instructions
        instruction_margin = 10
        instruction_offset_x = screen_width - instruction_margin
        instruction_offset_y = screen_height // 2 - (len(instructions) * font.get_height()) // 2
        for idx, instruction in enumerate(instructions):
            instruction_text = font.render(instruction, True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(topright=(instruction_offset_x, instruction_offset_y + idx * (instruction_text.get_height() + instruction_margin)))
            screen.blit(instruction_text, instruction_rect)

        # Map rendering
        cell_size = 65  # Adjust cell size as needed
        if map_paths[map_index] == "maps/sokoban_extra1.txt":
            cell_size = 48  # Reduce cell size for "sokoban_extra1" map
        map_width = len(game_map[0]) * cell_size
        map_height = len(game_map) * cell_size
        map_offset_x = (screen_width - map_width) // 2
        map_offset_y = (screen_height - map_height) // 2

        for row in range(len(game_map)):
            for col in range(len(game_map[row])):
                x = map_offset_x + col * cell_size
                y = map_offset_y + row * cell_size
                if game_map[row][col] == '#':
                    # Resize wall image to 48x48 if the map is "sokoban_extra1"
                    if map_paths[map_index] == "maps/sokoban_extra1.txt":
                        resized_wall_image = pygame.transform.scale(wall_image, (48, 48))
                        screen.blit(resized_wall_image, (x, y))
                    else:
                        screen.blit(wall_image, (x, y))
                elif game_map[row][col] == '$':
                    # Resize box image to 48x48 if the map is "sokoban_extra1"
                    if map_paths[map_index] == "maps/sokoban_extra1.txt":
                        resized_box_image = pygame.transform.scale(box_image, (48, 48))
                        screen.blit(resized_box_image, (x, y))
                    else:
                        screen.blit(box_image, (x, y))
                elif game_map[row][col] == '.':
                    # Resize target image to 48x48 if the map is "sokoban_extra1"
                    if map_paths[map_index] == "maps/sokoban_extra1.txt":
                        resized_target_image = pygame.transform.scale(target_image, (48, 48))
                        screen.blit(resized_target_image, (x, y))
                    else:
                        screen.blit(target_image, (x, y))
                elif game_map[row][col] == '*':
                    # Resize box on target image to 48x48 if the map is "sokoban_extra1"
                    if map_paths[map_index] == "maps/sokoban_extra1.txt":
                        resized_box_on_target_image = pygame.transform.scale(box_on_target_image, (48, 48))
                        screen.blit(resized_box_on_target_image , (x, y))
                    else:
                        screen.blit(box_on_target_image , (x, y))
                else:
                    # Resize floor image to 48x48 if the map is "sokoban_extra1"
                    if map_paths[map_index] == "maps/sokoban_extra1.txt":
                        resized_floor_image = pygame.transform.scale(floor_image, (48, 48))
                        screen.blit(resized_floor_image, (x, y))
                    else:
                        screen.blit(floor_image, (x, y))
                    # Then draw other elements
                    if game_map[row][col] == '@':
                        # Resize player image to 48x48 if the map is "sokoban_extra1"
                        if map_paths[map_index] == "maps/sokoban_extra1.txt":
                            resized_player_image = pygame.transform.scale(player_image, (48, 48))
                            screen.blit(resized_player_image, (x, y))
                        else:
                            screen.blit(player_image, (x, y))

        # Display selected strategy and map at the top left
        selected_strategy_text = font.render(f"Selected Strategy: {selected_strategy}", True, (255, 255, 255))
        screen.blit(selected_strategy_text, (instruction_margin, instruction_margin))
        map_name_text = font.render(f"Selected Map: {os.path.basename(map_paths[map_index])}", True, (255, 255, 255))
        screen.blit(map_name_text, (instruction_margin, instruction_margin + selected_strategy_text.get_height() + instruction_margin))

        pygame.display.flip()  # Update the display after drawing the map and text

if __name__ == '__main__':
    selected_strategy, game_map, start_time = select_strategy()
    print("Selected strategy:", selected_strategy)

    game_state = GameState(game_map)

    solver = Solver(game_state, selected_strategy)
    solver.solve()
    solution = solver.get_solution()

    game_visualization = GameVisualization(game_state, solution)

    pygame.init()
    game_visualization.start()
