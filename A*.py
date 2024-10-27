import heapq
import time
from memory_profiler import memory_usage

# Define directions for movement: (row_offset, col_offset)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

class State:
    def __init__(self, ares_pos, stones, cost, parent=None):
        self.ares_pos = ares_pos  # (row, col)
        self.stones = stones  # List of (row, col, weight) positions for stones
        self.cost = cost  # g value (actual cost from start)
        self.parent = parent  # Parent state for tracing path

    def __lt__(self, other):
        return self.cost < other.cost  # For heapq to compare states by cost

def is_valid_move(grid, row, col, stones):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != '#' and (row, col) not in [(s[0], s[1]) for s in stones]

def is_valid_push(grid, stone_pos, dir, new_stone_pos, ares_pos, stones):
    valid_position_behind = (ares_pos[0] == stone_pos[0] - dir[0] and ares_pos[1] == stone_pos[1] - dir[1])

    valid_new_position = grid[new_stone_pos[0]][new_stone_pos[1]] != '#' and (new_stone_pos[0], new_stone_pos[1]) not in [(s[0], s[1]) for s in stones]

    return valid_position_behind and valid_new_position


def check_goal(stones, switches):
    # Check if each switch contains exactly one stone and no switches are left unfilled or have more than one stone
    stones_on_switches = set(stone[:2] for stone in stones if stone[:2] in switches)
    return len(stones_on_switches) == len(switches)  # All switches should be filled uniquely

def calculate_h(ares_pos, stones, switches):
    h_value = 0
    for stone in stones:
        min_distance = min(abs(stone[0] - switch[0]) + abs(stone[1] - switch[1]) for switch in switches)
        h_value += min_distance * stone[2]
        h_value += abs(stone[0] - ares_pos[0]) + abs(stone[1] - ares_pos[1])
    return h_value

def a_star_search(grid, ares_start, stones, switches):
    open_list = []
    closed_set = set()

    # Initial state
    start_state = State(ares_start, stones, 0)
    heapq.heappush(open_list, (0, start_state))
    expanded_node = 1

    while open_list:
        current_state = heapq.heappop(open_list)[1]

        if check_goal(current_state.stones, switches):
            return expanded_node, trace_path(current_state)

        # Mark current state as visited
        closed_set.add((current_state.ares_pos, tuple(stone[:2] for stone in current_state.stones)))

        # Explore neighbors (4 directions)
        for dir in DIRECTIONS:
            new_ares_pos = (current_state.ares_pos[0] + dir[0], current_state.ares_pos[1] + dir[1])

            # Normal movement (no stone push)
            if is_valid_move(grid, new_ares_pos[0], new_ares_pos[1], current_state.stones):
                new_stones = current_state.stones.copy()
                new_state = State(new_ares_pos, new_stones, current_state.cost + 1, current_state)
                if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                    heapq.heappush(open_list, (new_state.cost + calculate_h(new_state.ares_pos, new_state.stones, switches), new_state))
                    expanded_node += 1

            # Check if pushing a stone is possible
            for i, stone_pos in enumerate(current_state.stones):
                if stone_pos[:2] == new_ares_pos:  # Ares is adjacent to a stone
                    new_stone_pos = (stone_pos[0] + dir[0], stone_pos[1] + dir[1])
                    if is_valid_push(grid, stone_pos, dir, new_stone_pos, current_state.ares_pos, current_state.stones):
                        new_stones = current_state.stones.copy()
                        new_stones[i] = (new_stone_pos[0], new_stone_pos[1], stone_pos[2])  # Keep stone's weight
                        push_cost = stone_pos[2] + 1 # Cost depends on stone weight
                        new_state = State(new_ares_pos, new_stones, current_state.cost + push_cost, current_state)
                        if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                            heapq.heappush(open_list, (new_state.cost + calculate_h(new_state.ares_pos, new_state.stones, switches), new_state))
                            expanded_node += 1
    return None

def trace_path(state):
    path = []
    while state is not None:
        path.append(state)
        state = state.parent
    path.reverse()  # Reverse to get the path from start to goal
    return path

def createMatrix(file_name):   
    matrix = [] 
    with open(file_name, 'r') as file:
        first_line = file.readline().strip()
        weights = list(map(int, first_line.split()))

        for line in file:
            line = line.replace('\n','')
            matrix.append(list(line))
        stones, ares_pos, switches, = [], [], []

    for row_index, row in enumerate(matrix):
        for col_index, element in enumerate(row):
            if element == '$' or element == '*':
                stones.append((row_index, col_index))
            if element == '@' or element == '+':
                ares_pos = (row_index, col_index)
            if element == '+' or element == '.' or element == '*':
                switches.append((row_index, col_index)) 
    return matrix, ares_pos, stones, switches, weights

def output():
    # Sample usage
    grid, ares_start, stones, switches, weights = createMatrix('/Users/nguyenngochoang/Documents/CSAI/input-10.txt')
    # Add stone weights to stone positions
    new_stones = [(stones[i][0], stones[i][1], weights[i]) for i in range(len(stones))]
    start_time = time.time()
    mem_usage, result = memory_usage((a_star_search, (grid, ares_start, new_stones, switches)), retval=True)
    end_time = time.time()

    if result is not None:
        node, path = result
        total_time = 1000 * (end_time - start_time)
        usage = max(mem_usage) - min(mem_usage)
        weight = path[-1].cost

        steps = ""
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

        print('A*')
        print(f'Steps: {len(steps)}, Weight: {weight}, Node: {node}, Time (ms): {total_time}, Memory (MB): {usage}')
        print(steps)
    else:
        print("No solution found")


if __name__ == '__main__':
    output()