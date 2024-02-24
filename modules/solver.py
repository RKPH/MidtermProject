from collections import deque
import time
from copy import deepcopy
import heapq
from functools import wraps

def print_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print("Expanded state:", result)
        print("Number of state generated:", args[0].generated_states)
        print("Number of expanded nodes:", args[0].expanded_states)
        print("Number of moves to reach target:", len(result) if result else None)
        print("Runtime:", round(end_time - start_time, 4), "seconds")

        return result

    return wrapper


class Solver(object):
    def __init__(self, initial_state, strategy):
        self.initial_state = initial_state
        self.strategy = strategy
        self.solution = None
        self.time = None
        self.expanded_states = 0  # Initialize expanded_states attribute
        self.generated_states = 0  # Initialize generated_states attribute

    def solve(self):
        start_time = time.time()
        if self.strategy == 'bfs':
            self.solution = self.bfs()
        elif self.strategy == 'dfs':
            self.solution = self.dfs()
        elif self.strategy == 'astar':
            self.solution = self.astar()
        elif self.strategy == 'ucs':
            self.solution = self.ucs()
        elif self.strategy == 'greedy':
            self.solution = self.greedy()
        elif self.strategy == 'custom':
            self.solution = self.custom()
        else:
            raise Exception('Invalid strategy')
        self.time = time.time() - start_time

    @print_stats
    def bfs(self):
        visited_states = set()
        queue = deque([(self.initial_state, [])])

        while queue:
            current_state, path = queue.popleft()
            self.expanded_states += 1

            if self.is_goal_state(current_state):
                return path

            visited_states.add(current_state.hash())  # Add current state's hash to visited

            for action in self.get_legal_actions(current_state):
                next_state = self.get_next_state(current_state, action)

                # Check if the next state has been visited or is in the queue
                next_state_hash = next_state.hash()
                if next_state_hash not in visited_states:
                    queue.append((next_state, path + [action]))
                    visited_states.add(next_state_hash)  # Add next state's hash to visited

                    # Increment generated states only if the state is not visited
                    self.generated_states += 1

        return None


    def is_goal_state(self, state):
        return state.check_solved()

    def get_legal_actions(self, state):
        posPlayer = state.find_player()
        posBox = state.find_boxes()
        all_actions = [[-1, 0, 'U'], [1, 0, 'D'], [0, -1, 'L'], [0, 1, 'R']]
        legal_actions = []

        for action in all_actions:
            new_pos_player = (posPlayer[0] + action[0], posPlayer[1] + action[1])
            new_pos_box = (new_pos_player[0] + action[0], new_pos_player[1] + action[1])

            if (
                state.is_empty(new_pos_player)
                or (state.is_box(new_pos_player) and state.is_empty(new_pos_box))
            ):
                legal_actions.append(action[2])

        return legal_actions

    def get_next_state(self, state, action):
        """Generate the next state based on the action taken."""
        return state.move(action)

    @print_stats
    def dfs(self):
        stack = [(self.initial_state, [])]
        visited_states = set()

        while stack:
            current_state, path = stack.pop()
            self.expanded_states += 1

            if current_state.check_solved():
                return path

            visited_states.add(current_state.hash())

            for action in self.get_legal_actions(current_state):
                next_state = self.get_next_state(current_state, action)

                next_state_hash = next_state.hash()
                if next_state_hash not in visited_states:
                    stack.append((next_state, path + [action]))
                    visited_states.add(next_state_hash)
                    self.generated_states += 1

        return None


    @print_stats
    def astar(self):
        open_list = [(self.initial_state.get_total_cost(), self.initial_state, [])]
        closed_set = set()  # Maintain a set of visited states

        while open_list:
            _, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                return path

            current_state_hash = hash(current_state)
            if current_state_hash in closed_set:
                continue  # Skip if state has already been visited

            closed_set.add(current_state_hash)  # Mark state as visited

            for direction in ['U', 'D', 'L', 'R']:
                next_state = current_state.move(direction)
                next_state_hash = hash(next_state)

                if next_state_hash not in closed_set:
                    new_cost = next_state.get_total_cost()
                    heapq.heappush(open_list, (new_cost, next_state, path + [direction]))
                    self.generated_states += 1

            self.expanded_states += 1

        return None

    @print_stats
    def ucs(self):
        open_list = [(self.initial_state.get_current_cost(), self.initial_state, [])]
        heapq.heapify(open_list)
        visited_states = set()  # Track visited states

        while open_list:
            current_cost, current_state, path = heapq.heappop(open_list)

            current_state_hash = hash(current_state)

            if current_state_hash in visited_states:
                continue  # Skip if state has been visited with a lower cost

            visited_states.add(current_state_hash)

            if current_state.check_solved():
                return path

            for direction in ['U', 'D', 'L', 'R']:
                next_state = current_state.move(direction)
                next_cost = next_state.get_current_cost() + len(path)  # Calculate total cost

                if hash(next_state) not in visited_states:
                    heapq.heappush(open_list, (next_cost, next_state, path + [direction]))
                    self.generated_states += 1

            self.expanded_states += 1

        return None


    @print_stats
    def greedy(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        closed_set = set()

        while open_list:
            _, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                return path

            current_state_hash = hash(current_state)
            closed_set.add(current_state_hash)

            for direction in ['U', 'D', 'L', 'R']:
                next_state = current_state.move(direction)
                next_state_hash = hash(next_state)

                if next_state_hash not in closed_set:
                    heuristic_value = next_state.get_heuristic()
                    heapq.heappush(open_list, (heuristic_value, next_state, path + [direction]))

            self.expanded_states += 1
            self.generated_states += 1

        return None
    @print_stats
    
    @print_stats
    def custom(self):
        open_list = [(self.initial_state.get_heuristic(), self.initial_state, [])]
        closed_set = set()  # Maintain a set of visited states

        while open_list:
            _, current_state, path = heapq.heappop(open_list)

            if current_state.check_solved():
                return path

            current_state_hash = hash(current_state)
            if current_state_hash in closed_set:
                continue  # Skip if state has already been visited

            closed_set.add(current_state_hash)  # Mark state as visited

            for direction in ['U', 'D', 'L', 'R']:
                next_state = current_state.move(direction)
                next_state_hash = hash(next_state)

                if next_state_hash not in closed_set:
                    heuristic_value = next_state.get_heuristic()
                    heapq.heappush(open_list, (heuristic_value, next_state, path + [direction]))

            self.expanded_states += 1
            self.generated_states += 1

        return None


        


    def get_solution(self):
        return self.solution


