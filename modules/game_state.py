"""
Sokuban game state class
The state of the game consists the map which is a 2D array of characters. There are 6 types of characters:
- ' ': empty space
- '#': wall
- '$': box
- '.': target
- '@': player
- '+': player on target
- '*': box on target
The game state class keeps track of the map.
The game state also keeps track of the player and box positions, and whether the game is solved or not.
The game state class has the following methods:
- find_player(): find the player in the map and return its position
- find_boxes(): find all the boxes in the map and return their positions
- find_targets(): find all the targets in the map and return their positions  
- generate_next_state(direction): generate the next game state by moving the player to the given direction
- check_solved(): check if the game is solved
"""

from copy import deepcopy

class GameState:
    def __init__(self, map, current_cost=0):  
        self.map = map
        self.current_cost = current_cost 
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.player = self.find_player()
        self.boxes = self.find_boxes()
        self.targets = self.find_targets()
        self.is_solved = self.check_solved()
        self.solution_path = [] 
    def hash(self):
        """Generate a hash value for the game state."""
        map_hash = hash(tuple(map(tuple, self.map)))  # Hash the map configuration
        player_hash = hash(self.player)  # Hash the player position
        return hash((map_hash, player_hash))  # Combine both hash values    
    def __lt__(self, other):
        return self.get_current_cost() < other.get_current_cost()

    def __hash__(self):
        return hash(tuple(map(tuple, self.map)))

    def __eq__(self, other):
        return (
            isinstance(other, GameState) and
            self.map == other.map and
            self.current_cost == other.current_cost
            # Add other relevant attributes for equality comparison
        )
    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to find the player, boxes, and targets in the map
    # The positions are tuples (row, column)
    # ------------------------------------------------------------------------------------------------------------------

    def find_player(self):
        """Find the player in the map and return its position"""
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in ['@', '+']:
                    return row, col
        # If player is not found, return a default position or handle the error as appropriate
        return None


    def find_boxes(self):
        """Find all the boxes in the map and return their positions"""
        boxes = []
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in ['$', '*']:
                    boxes.append((row, col))
        return boxes

    def find_targets(self):
        """Find all the targets in the map and return their positions"""
        targets = []
        for row in range(self.height):
            for col in range(self.width):
                if self.map[row][col] in ['.', '*']:
                    targets.append((row, col))
        return targets

    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to check if a position is a wall, box, target, or empty space
    # The position is a tuple (row, column)
    # ------------------------------------------------------------------------------------------------------------------
    
    def is_wall(self, position):
        """Check if the given position is a wall"""
        row, col = position
        return self.map[row][col] == '#'

    def is_box(self, position):
        """Check if the given position is a box"""
        row, col = position
        return self.map[row][col] in ['$', '*']

    def is_target(self, position):
        """Check if the given position is a target"""
        row, col = position
        return self.map[row][col] in ['.', '*']
    

    def is_empty(self, position):
        """Check if a position is empty or a target."""
        row, col = position
        return self.map[row][col] in [' ', '.']
    
    def is_box_on_target(self, position):
        row, col = position
        return self.map[row][col] in [ '*']
    
    # ------------------------------------------------------------------------------------------------------------------
    # The following methods get heuristics for the game state (for informed search strategies)
    # ------------------------------------------------------------------------------------------------------------------
    


    def get_heuristic(self):
        """Get the heuristic for the game state"""
        heuristic = 0
        for box in self.boxes:
            min_distance = float('inf')
            for target in self.targets:
                distance = abs(box[0] - target[0]) + abs(box[1] - target[1])
                min_distance = min(min_distance, distance)
            heuristic += min_distance
        return heuristic



    def get_total_cost(self):
        """Get the cost for the game state"""
        return self.current_cost + self.get_heuristic()


    def get_current_cost(self):
        """Get the current cost for the game state"""
        return self.current_cost
    
    # ------------------------------------------------------------------------------------------------------------------
    # The following methods are used to generate the next game state and check if the game is solved
    # ------------------------------------------------------------------------------------------------------------------

    
    
    def move(state, direction):
        """Generate the next game state by moving the player in the given direction."""
        row, col = state.player
        new_row, new_col = row, col

        if direction == 'U':
            new_row -= 1
        elif direction == 'D':
            new_row += 1
        elif direction == 'L':
            new_col -= 1
        elif direction == 'R':
            new_col += 1

        new_state = GameState([row[:] for row in state.map], state.current_cost)  
        new_state.height = state.height
        new_state.width = state.width
        new_state.player = (new_row, new_col)
        new_state.boxes = state.boxes[:]
        new_state.targets = state.targets[:]
        new_state.is_solved = state.is_solved
        new_state.solution_path = state.solution_path[:]
        
        if new_state.is_empty((new_row, new_col)):
            # If the new position is empty, move the player
            new_state.map[row][col] = '.' if (row, col) in new_state.targets else ' '
            new_state.map[new_row][new_col] = '@' if new_state.map[new_row][new_col] == ' ' else '+'
            new_state.current_cost += 1

        elif new_state.is_box((new_row, new_col)):
            new_box_row, new_box_col = new_row, new_col

            if direction == 'U':
                new_box_row -= 1
            elif direction == 'D':
                new_box_row += 1
            elif direction == 'L':
                new_box_col -= 1
            elif direction == 'R':
                new_box_col += 1

            if new_state.is_empty((new_box_row, new_box_col)):
                # If the new position for the box is empty, push the box
                new_state.map[row][col] = '.' if (row, col) in new_state.targets else ' '
                new_state.map[new_row][new_col] = '@' if new_state.map[new_row][new_col] == ' ' else '+'
                new_state.map[new_box_row][new_box_col] = '$' if new_state.map[new_box_row][new_box_col] == ' ' else '*'
                new_state.player = (new_row, new_col)
                new_state.boxes.remove((new_row, new_col))
                new_state.boxes.append((new_box_row, new_box_col))
                new_state.current_cost += 1

        return new_state
    
    
    def check_solved(self):
        """Check if the game is solved"""
        return all(box in self.targets for box in self.boxes)