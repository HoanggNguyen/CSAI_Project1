import os
import time
from memory_profiler import memory_usage
from maze import *

# Define possible movement directions: (row_offset, col_offset)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

class State:
    def __init__(self, ares_pos, stones, cost, parent=None):
        """
        Initialize a state in the puzzle.
        :param ares_pos: Current position of Ares as (row, col).
        :param stones: List of tuples (row, col, weight) for stone positions and weights.
        :param cost: The accumulated cost from the start (g-value).
        :param parent: The parent state for path tracing.
        """
        self.ares_pos = ares_pos
        self.stones = stones
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        # Comparison based on cost for priority queue handling
        return self.cost < other.cost

def is_valid_move(grid, row, col, stones):
    """
    Check if moving to (row, col) is valid.
    :param grid: The game grid layout.
    :param row: Row index for the target position.
    :param col: Column index for the target position.
    :param stones: List of current stone positions.
    :return: True if the move is within bounds, not blocked, and not occupied by stones.
    """
    return (
        0 <= row < len(grid) and
        0 <= col < len(grid[0]) and
        grid[row][col] != '#' and
        (row, col) not in [(s[0], s[1]) for s in stones]
    )

def is_valid_push(grid, stone_pos, dir, new_stone_pos, ares_pos, stones):
    """
    Check if Ares can push a stone in a specified direction.
    :param grid: The game grid layout.
    :param stone_pos: Current position of the stone to push.
    :param dir: Direction of the push as (row_offset, col_offset).
    :param new_stone_pos: Target position for the pushed stone.
    :param ares_pos: Current position of Ares.
    :param stones: List of current stone positions.
    :return: True if Ares can legally push the stone.
    """
    # Ensure Ares is directly behind the stone in the opposite direction of the push
    valid_position_behind = (ares_pos[0] == stone_pos[0] - dir[0] and ares_pos[1] == stone_pos[1] - dir[1])

    # Ensure new stone position is not blocked
    valid_new_position = (
        0 <= new_stone_pos[0] < len(grid) and
        0 <= new_stone_pos[1] < len(grid[0]) and
        grid[new_stone_pos[0]][new_stone_pos[1]] != '#' and 
        (new_stone_pos[0], new_stone_pos[1]) not in [(s[0], s[1]) for s in stones]
    )

    return valid_position_behind and valid_new_position

def check_goal(stones, switches):
    """
    Check if all switches are occupied by stones.
    :param stones: List of current stone positions.
    :param switches: List of target switch positions.
    :return: True if each switch is filled by exactly one stone.
    """
    stones_on_switches = set(stone[:2] for stone in stones if stone[:2] in switches)

    return len(stones_on_switches) == len(switches)  # All switches should be occupied without overlap

def trace_path(state):
    """
    Trace the path from the initial state to the goal state.
    :param state: The goal state to trace from.
    :return: List of states from start to goal.
    """
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

def output(sc,algo, input_path, output_path):
    # Đọc dữ liệu từ file đầu vào và khởi tạo trạng thái
    grid, ares_start, stones, switches, weights = createMatrix(input_path)
    # Thêm trọng số cho vị trí đá
    new_stones = [(stones[i][0], stones[i][1], weights[i]) for i in range(len(stones))]

    # Usage in the main function
    start_time = time.time()
    loading_thread = start_loading_screen(sc)  # Start loading screen in a separate thread

    # Execute your algorithm
    mem_usage, result = memory_usage((algo, (grid, ares_start, new_stones, switches)), retval=True)

    # Stop the loading screen when the algorithm finishes
    stop_loading_screen(loading_thread)
    end_time = time.time()

    with open(output_path, 'a') as file:
        if result is not None:
            node, path = result
            total_time = 1000 * (end_time - start_time)  # Thời gian chạy (ms)
            usage = max(mem_usage) - min(mem_usage)      # Dung lượng bộ nhớ đã sử dụng (MB)
            weight = path[-1].cost                       # Trọng số cuối cùng
            steps = ""
            costs = []

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

                costs.append(path[i].cost)
            # Ghi ra tệp
            file.write(f"{algo.__name__}\n")
            file.write(f"Steps: {len(steps)}, Weight: {weight -  len(steps)}, Node: {node}, Time (ms): {total_time:.2f}, Memory (MB): {usage:.2f}\n")
            file.write(steps + "\n")
        else:
            print(algo.__name__)
            print("No solution found")
            file.write(f"{algo.__name__}\n")
            file.write("No solution found\n")
            return [], None, None
        
    return costs, steps, total_time