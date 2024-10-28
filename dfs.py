import time
import tracemalloc

# Define directions for movement: (row_offset, col_offset)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

class State:
    def __init__(self, ares_pos, stones, cost, parent=None):
        self.ares_pos = ares_pos  # (row, col) position of Ares
        self.stones = stones  # List of (row, col, weight) positions for stones
        self.cost = cost  # g value (actual cost from start)
        self.parent = parent  # Parent state for tracing path

def create_matrix(file_name):
    matrix = []
    
    with open(file_name, 'r') as file:
        first_line = file.readline().strip()
        weights = list(map(int, first_line.split()))

        for line in file:
            line = line.replace('\n','')
            matrix.append(list(line))
        stones, ares_pos, switches, = [], [], []

    # Parse the matrix to find positions of stones, Ares, and switches
    for row_index, row in enumerate(matrix):
        for col_index, element in enumerate(row):
            if element == '$' or element == '*':
                stones.append((row_index, col_index))
            if element == '@' or element == '+':
                ares_pos = (row_index, col_index)
            if element == '+' or element == '.' or element == '*':
                switches.append((row_index, col_index))
    
    return matrix, ares_pos, stones, switches, weights

def is_valid_move(grid, row, col, stones):
    # Check if the move is within bounds, not hitting a wall, and not colliding with a stone
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != '#' and (row, col) not in [(s[0], s[1]) for s in stones]

def is_valid_push(grid, stone_pos, dir, new_stone_pos, ares_pos, stones):
    # Check if Ares is in a valid position to push the stone and if the new stone position is valid
    valid_position_behind = (ares_pos[0] == stone_pos[0] - dir[0] and ares_pos[1] == stone_pos[1] - dir[1])
    valid_new_position = grid[new_stone_pos[0]][new_stone_pos[1]] != '#' and (new_stone_pos[0], new_stone_pos[1]) not in [(s[0], s[1]) for s in stones]

    return valid_position_behind and valid_new_position

def check_goal(stones, switches):
    # Check if all stones are on switches
    stones_on_switches = set(stone[:2] for stone in stones if stone[:2] in switches)
    
    return len(stones_on_switches) == len(switches)

def trace_path(state):
    # Trace back the path from the goal state to the start state
    path = []
    
    while state is not None:
        path.append(state)
        state = state.parent
    
    path.reverse()
    
    return path

def dfs_search(grid, ares_start, stones, switches, max_depth=333):
    stack = []
    closed_set = set()
    start_state = State(ares_start, stones, 0)
    stack.append((start_state, 0))  # (state, depth)
    expanded_node = 1
    best_solution = None

    while stack:
        current_state, depth = stack.pop()

        # Check if the current state is the goal state
        if check_goal(current_state.stones, switches):
            if best_solution is None or current_state.cost < best_solution.cost:
                best_solution = current_state
            continue

        # Skip if the depth exceeds the maximum depth
        if depth > max_depth:
            continue

        closed_set.add((current_state.ares_pos, tuple(stone[:2] for stone in current_state.stones)))

        for i, stone_pos in enumerate(current_state.stones):
            for dir in DIRECTIONS:
                new_ares_pos = (current_state.ares_pos[0] + dir[0], current_state.ares_pos[1] + dir[1])

                # Check if Ares can move to the new position
                if is_valid_move(grid, new_ares_pos[0], new_ares_pos[1], current_state.stones):
                    new_stones = current_state.stones.copy()
                    new_state = State(new_ares_pos, new_stones, current_state.cost + 1, current_state)
                    
                    if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                        stack.append((new_state, depth + 1))
                        expanded_node += 1

                # Check if Ares can push the stone to the new position
                if stone_pos[:2] == new_ares_pos:
                    new_stone_pos = (stone_pos[0] + dir[0], stone_pos[1] + dir[1])
                    
                    if is_valid_push(grid, stone_pos, dir, new_stone_pos, current_state.ares_pos, current_state.stones):
                        new_stones = current_state.stones.copy()
                        new_stones[i] = (new_stone_pos[0], new_stone_pos[1], stone_pos[2])
                        push_cost = stone_pos[2] + 1
                        new_state = State(new_ares_pos, new_stones, current_state.cost + push_cost, current_state)
                        
                        if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                            stack.append((new_state, depth + 1))
                            expanded_node += 1

                            # If the stone is pushed onto a switch, break to push the next stone
                            if new_stone_pos in switches:
                                break

    if best_solution:
        return expanded_node, trace_path(best_solution)
    return None

def output():
    file_path = 'input-2.txt'
    grid, ares_start, stones, switches, weights = create_matrix(file_path)
    new_stones = [(stones[i][0], stones[i][1], weights[i]) for i in range(len(stones))]
    
    start_time = time.time()
    tracemalloc.start()

    result = dfs_search(grid, ares_start, new_stones, switches)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if result is not None:
        expanded_node, path = result
        time_taken = (end_time - start_time) * 1000
        memory_used = peak / (1024 * 1024)
        weight = path[-1].cost
        
        steps = ""

        # Generate the steps taken to reach the goal
        for i in range(1, len(path)):
            if all(stone in path[i - 1].stones for stone in path[i].stones):
                if path[i].ares_pos[1] < path[i - 1].ares_pos[1]:
                    steps += 'l'
                elif path[i].ares_pos[1] > path[i - 1].ares_pos[1]:
                    steps += 'r'
                elif path[i].ares_pos[0] < path[i - 1].ares_pos[0]:
                    steps += 'u'
                else:
                    steps += 'd'
            else:
                if path[i].ares_pos[1] < path[i - 1].ares_pos[1]:
                    steps += 'L'
                elif path[i].ares_pos[1] > path[i - 1].ares_pos[1]:
                    steps += 'R'
                elif path[i].ares_pos[0] < path[i - 1].ares_pos[0]:
                    steps += 'U'
                else:
                    steps += 'D'

        print('DFS')
        print(f'Steps: {len(steps)}, Weight: {weight}, Node: {expanded_node}, Time (ms): {time_taken}, Memory (MB): {memory_used}')
        print(steps)
    else:
        print("No solution found")

if __name__ == "__main__":
    output()
