import heapq
from support import *
from collections import deque

def BFS(grid, ares_start, stones, switches):

    open_list = deque()  # Queue for BFS
    closed_set = {}  # Use a dictionary to store minimum costs per state signature
    expanded_nodes = 1

    # Initial state
    start_state = State(ares_start, stones, 0)
    open_list.append(start_state)

    while open_list:
        # Dequeue the first state
        current_state = open_list.popleft()

        # Check if the current state meets the goal condition
        if check_goal(current_state.stones, switches):
            return expanded_nodes, trace_path(current_state)

        # Generate a unique state signature (Ares position and stone positions)
        state_signature = (current_state.ares_pos, tuple(stone[:2] for stone in current_state.stones))

        # Only expand this state if it's the lowest-cost instance seen so far
        if state_signature in closed_set and closed_set[state_signature] <= current_state.cost:
            continue
        closed_set[state_signature] = current_state.cost  # Store the cost of this state

        # Explore neighbors in all four directions
        for dir in DIRECTIONS:
            new_ares_pos = (current_state.ares_pos[0] + dir[0], current_state.ares_pos[1] + dir[1])

            # Normal movement (no stone push)
            if is_valid_move(grid, new_ares_pos[0], new_ares_pos[1], current_state.stones):
                new_state = State(new_ares_pos, current_state.stones.copy(), current_state.cost + 1, current_state)
                new_signature = (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones))
                
                if new_signature not in closed_set or closed_set[new_signature] > new_state.cost:
                    open_list.append(new_state)
                    expanded_nodes += 1

            # Attempt to push stones in the current direction
            for i, stone_pos in enumerate(current_state.stones):
                if stone_pos[:2] == new_ares_pos:  # Ares is adjacent to a stone
                    new_stone_pos = (stone_pos[0] + dir[0], stone_pos[1] + dir[1])
                    if is_valid_push(grid, stone_pos, dir, new_stone_pos, current_state.ares_pos, current_state.stones):
                        new_stones = current_state.stones.copy()
                        new_stones[i] = (new_stone_pos[0], new_stone_pos[1], stone_pos[2])  # Keep stone's weight
                        push_cost = stone_pos[2] + 1  # Cost depends on stone weight
                        new_state = State(new_ares_pos, new_stones, current_state.cost + push_cost, current_state)
                        new_signature = (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones))

                        if new_signature not in closed_set or closed_set[new_signature] > new_state.cost:
                            open_list.append(new_state)
                            expanded_nodes += 1

    return None  # Return None if no solution is found


def calculate_h(ares_pos, stones, switches):

    h_value = 0
    for stone in stones:
        # Minimum distance from stone to the nearest switch
        min_distance = min(abs(stone[0] - switch[0]) + abs(stone[1] - switch[1]) for switch in switches)
        h_value += min_distance * stone[2]  # Weighted distance for stone
        # Add distance from Ares to stone
        h_value += abs(stone[0] - ares_pos[0]) + abs(stone[1] - ares_pos[1])
    return h_value

def ASTAR(grid, ares_start, stones, switches):

    open_list = []
    closed_set = set()
    expanded_nodes = 1

    # Push the initial state into the priority queue
    start_state = State(ares_start, stones, 0)
    heapq.heappush(open_list, (0, start_state))

    while open_list:
        # Pop the state with the lowest cost from the priority queue
        current_state = heapq.heappop(open_list)[1]

        # Check if current state meets the goal condition
        if check_goal(current_state.stones, switches):
            return expanded_nodes, trace_path(current_state)

        # Mark the current state as visited
        state_signature = (current_state.ares_pos, tuple(stone[:2] for stone in current_state.stones))
        closed_set.add(state_signature)

        # Explore neighbors in all four directions
        for dir in DIRECTIONS:
            new_ares_pos = (current_state.ares_pos[0] + dir[0], current_state.ares_pos[1] + dir[1])

            # Normal movement (no stone push)
            if is_valid_move(grid, new_ares_pos[0], new_ares_pos[1], current_state.stones):
                # Create a new state with updated position and cost
                new_state = State(new_ares_pos, current_state.stones.copy(), current_state.cost + 1, current_state)
                if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                    heapq.heappush(open_list, (new_state.cost + calculate_h(new_state.ares_pos, new_state.stones, switches), new_state))
                    expanded_nodes += 1

            # Attempt to push stones in the current direction
            for i, stone_pos in enumerate(current_state.stones):
                if stone_pos[:2] == new_ares_pos:  # Ares is adjacent to a stone
                    new_stone_pos = (stone_pos[0] + dir[0], stone_pos[1] + dir[1])
                    if is_valid_push(grid, stone_pos, dir, new_stone_pos, current_state.ares_pos, current_state.stones):
                        # Update the stone's position while keeping its weight
                        new_stones = current_state.stones.copy()
                        new_stones[i] = (new_stone_pos[0], new_stone_pos[1], stone_pos[2])
                        push_cost = stone_pos[2] + 1  # Cost of moving based on stone's weight
                        new_state = State(new_ares_pos, new_stones, current_state.cost + push_cost, current_state)
                        if (new_state.ares_pos, tuple(stone[:2] for stone in new_state.stones)) not in closed_set:
                            heapq.heappush(open_list, (new_state.cost + calculate_h(new_state.ares_pos, new_state.stones, switches), new_state))
                            expanded_nodes += 1

    return None  # Return None if no solution is found
