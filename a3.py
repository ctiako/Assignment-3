# CS305 Park University
# Assignment #3 Starter Code
# STRIPS Planning
# By Cyrille Tekam Tiako
# 27 Aug 2024

import time  # Import the time module

# Mock implementations for missing imports
class Strips:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects

class STRIPS_domain:
    def __init__(self, features, actions):
        self.features = features
        self.actions = actions

class Planning_problem:
    def __init__(self, domain, initial_state, goal_state):
        self.domain = domain
        self.initial_state = initial_state
        self.goal_state = goal_state

class Forward_STRIPS:
    def __init__(self, problem, heuristic=None):
        self.problem = problem
        self.heuristic = heuristic

class SearcherMPP:
    def __init__(self, strips_problem):
        self.strips_problem = strips_problem

    def search(self):
        # This function should return the solution path
        # For now, return a mock solution to avoid errors
        return MockSolution()

class MockSolution:
    def __init__(self):
        self.arc = None
        self.initial = None

#######################
# Helper Functions:
#
# The functions below were created to help you complete the
# planning tasks. You will need to complete the implementation
# of other functions below.

def path_to_actions(path):
    """Converts an AIPython planning search path to a list of actions."""
    if path.arc:
        yield path.arc.action
        yield from path_to_actions(path.initial)

def gen_tiles(size):
    """Generates the names for tiles in the slide-puzzle search
       space in the format tileX where X is the number on the
       tile. 'blank' is also generated for the absent tile."""
    for i in range(1, size * size):
        yield 'tile' + str(i)
    yield 'blank'

def gen_spaces(size):
    """Generates names of the spaces on the slide puzzle. These
       names represent 2-d coordinates on the square puzzle and
       have the format spaceX-Y where X is the row and Y is the
       column."""
    for row in range(1, size + 1):
        for col in range(1, size + 1):
            yield 'space' + str(row) + '-' + str(col)

def gen_puzzle_feature_dict(size):
    """Generates the feature dictionary needed by STRIPS_domain."""
    spaces = set(gen_spaces(size))
    return {t: spaces for t in gen_tiles(size)}

def str_to_8puzzle_state(s):
    """Converts a 3x3 string into an 8-puzzle search state.
       Whitespace is trimmed off of each line and X stands in
       for the blank space (no number tile)."""
    row = 0
    state = dict()
    for line in s.strip().split("\n"):
        row += 1
        col = 0
        line = line.strip()
        for c in line:
            col += 1
            state['blank' if c == 'X' else 'tile' + c] = \
                'space' + str(row) + '-' + str(col)
    return state

def gen_puzzle_actions(size):
    """Generates all possible actions for the slide puzzle."""
    # right moves
    for tile in range(1, size * size):
        for row in range(1, size + 1):
            for col in range(1, size):
                yield Strips('move-' + str(tile) + '-right',
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col),
                              'blank': 'space' + str(row) + '-' + str(col + 1)},
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col + 1),
                              'blank': 'space' + str(row) + '-' + str(col)})
    # left moves
    for tile in range(1, size * size):
        for row in range(1, size + 1):
            for col in range(2, size + 1):
                yield Strips('move-' + str(tile) + '-left',
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col),
                              'blank': 'space' + str(row) + '-' + str(col - 1)},
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col - 1),
                              'blank': 'space' + str(row) + '-' + str(col)})

    # down moves
    for tile in range(1, size * size):
        for row in range(1, size):
            for col in range(1, size + 1):
                yield Strips('move-' + str(tile) + '-down',
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col),
                              'blank': 'space' + str(row + 1) + '-' + str(col)},
                             {'tile' + str(tile): 'space' + str(row + 1) + '-' + str(col),
                              'blank': 'space' + str(row) + '-' + str(col)})

    # up moves
    for tile in range(1, size * size):
        for row in range(2, size + 1):
            for col in range(1, size + 1):
                yield Strips('move-' + str(tile) + '-up',
                             {'tile' + str(tile): 'space' + str(row) + '-' + str(col),
                              'blank': 'space' + str(row - 1) + '-' + str(col)},
                             {'tile' + str(tile): 'space' + str(row - 1) + '-' + str(col),
                              'blank': 'space' + str(row) + '-' + str(col)})

def gen_puzzle_domain(size):
    """Creates the STRIPS_domain for the given slide-puzzle size."""
    return STRIPS_domain(gen_puzzle_feature_dict(size), list(gen_puzzle_actions(size)))

def puzzle_heuristic(state, goal):
    """Heuristic for the 8-puzzle problem: counts misplaced tiles."""
    misplaced = 0
    for tile in state:
        if state[tile] != goal[tile]:
            misplaced += 1
    return misplaced

def main():
    pend = """123
              456
              78X"""
    
    print("\n\nSolving puzzle 1...\n")
    p1start = """123
                 X56
                 478"""
    
    prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p1start),
                            str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 1 solution:', list(path_to_actions(res)))
    
    p2start = """437
                 568
                 21X"""
    
    print("\n\nSolving puzzle 2...\n")
    start_time = time.perf_counter()  # Record the start time
    prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p2start),
                            str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))
    end_time = time.perf_counter()  # Record the end time
    print("Time:", end_time - start_time, "seconds")
    
    print("\n\nSolving puzzle 2 with heuristic...\n")
    start_time = time.perf_counter()  # Record the start time
    prob = Planning_problem(gen_puzzle_domain(3),
                            str_to_8puzzle_state(p2start),
                            str_to_8puzzle_state(pend))
    fsprob = Forward_STRIPS(prob, puzzle_heuristic)
    searcher = SearcherMPP(fsprob)
    res = searcher.search()
    print('puzzle 2 solution:', list(path_to_actions(res)))
    end_time = time.perf_counter()  # Record the end time
    print("Time:", end_time - start_time, "seconds")
  
if __name__ == '__main__':
    main()
