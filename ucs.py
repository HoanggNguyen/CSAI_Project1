import time
import tracemalloc

directions = {
    'u': (-1,0),
    'd': (1,0),
    'l': (0,-1),
    'r': (0,1)
}

def createMatrix(file_name):   
    matrix = [] 
    with open(file_name, 'r') as file:
        first_line = file.readline().strip()
        weights = list(map(int, first_line.split()))

        for line in file:
            line = line.replace('\n','')
            matrix.append(list(line))
    return matrix, weights

def get_inf_in_grid(grid, weights):
    ares_position = None
    stones = []
    switches = []
    indx_weight = 0

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char == '@':
                ares_position = (r, c)
            elif char == '+':
                ares_position = (r, c)
                switches.append((r, c))
            elif char == '$':
                stones.append((r,c,weights[indx_weight]))
                indx_weight += 1
            elif char == '*':
                stones.append((r,c,weights[indx_weight]))
                indx_weight += 1
                switches.append((r, c))
            elif char == '.':
                switches.append((r, c))
    return ares_position, stones, switches
    
def can_move(pos, grid):
    dx, dy = pos
    return 0 <= dx < len(grid) and 0 <= dy < len(grid[0]) and grid[dx][dy] != '#'

def ucs_search(grid, start_pos, stones, switches):
    #Khởi tạo hàng đợi ưu tiên
    PQ = []
    PQ.append((0, start_pos, tuple(stones), []))

    #Tập các trạng thái đã đi qua
    visited = set()

    #Đếm số node
    node_count = 1

    while len(PQ):
        cost, ares_pos, stones, path = PQ.pop(0)
        stones = list(stones)
        if all(stone[:2] in switches for stone in stones):
            return cost, path, node_count

        state = (ares_pos, tuple(stones))
        visited.add(state)
    
        for move, (dx, dy) in directions.items():
            (dx_ares, dy_ares) = ares_pos
            new_ares_pos = (dx_ares + dx, dy_ares + dy)
            ares_push_stone = new_ares_pos in [stone[:2] for stone in stones]
            #Kiểm tra ares có di chuyển được không, có trùng vị trí với đá không
            if can_move(new_ares_pos, grid) and not ares_push_stone:
                #Trạng thái mới sau khi ares di chuyển
                new_state = (new_ares_pos, tuple(stones))

                #Thêm hướng di chuyển vào trong đường đi
                new_path = path + [move]

                #kiểm tra trạng thái mới có bị trùng lặp không
                if new_state not in visited:
                    check = True
                    node_count += 1
                    for cost_in_tup, ares_in_tup, stones_in_tup, path_in_tup in PQ:
                        #Kiểm tra xem trong tập PQ có chứa 2 giá trị giống nhau không
                        if new_ares_pos == ares_in_tup and stones_in_tup == tuple(stones):
                            #Nếu có, ưu tiên chi phí thấp hơn
                            if cost + 1 < cost_in_tup:
                                PQ.remove((cost_in_tup,ares_in_tup, stones_in_tup, path_in_tup))
                                PQ.append((cost + 1, ares_in_tup, stones_in_tup, new_path))
                            check = False
                            break
                    if check:
                        PQ.append((cost + 1, new_ares_pos, tuple(stones), new_path))
            #Nếu bước di chuyển của ares trùng với đá
            elif ares_push_stone:
                #Tìm vị trí mới của đá sau khi được đẩy
                for i in range(len(stones)):
                        if stones[i][:2] == new_ares_pos:
                            indx = i
                weight = stones[indx][2]
                (dx,dy) = directions[move]
                new_stone_pos = (stones[indx][0] + dx, stones[indx][1] + dy)

                #Kiểm tra đá có gặp vật cản không
                if can_move(new_stone_pos, grid) and new_stone_pos not in [stone[:2] for stone in stones]:
                    # Đẩy đá
                    new_stones = stones.copy()
                    new_stones[indx] = (stones[indx][0] + dx, stones[indx][1] + dy, weight)

                    #Trạng thái mới khi ares đẩy đá
                    new_state = (new_ares_pos, tuple(new_stones))

                    #Thêm hướng di chuyển vào trong đường đi
                    new_path = path + [move.upper()]

                    #kiểm tra trạng thái mới có bị trùng lặp không
                    if new_state not in visited:
                        check = True
                        node_count += 1
                        for cost_in_tup, ares_in_tup, stones_in_tup, path_in_tup in PQ:
                            #Kiểm tra xem trong tập PQ có chứa 2 giá trị giống nhau không
                            if new_ares_pos == ares_in_tup and stones_in_tup == tuple(new_stones):
                                #Nếu có, ưu tiên chi phí thấp hơn
                                if cost + weight + 1 < cost_in_tup:
                                    PQ.remove((cost_in_tup, ares_in_tup, stones_in_tup, path_in_tup))
                                    PQ.append((cost + weight + 1, ares_in_tup, stones_in_tup, new_path))
                                check = False
                                break
                        if check:
                            PQ.append((cost+weight+1, new_ares_pos, tuple(new_stones), new_path))
        PQ.sort()                    

    return 0, [], node_count

def game():
    #Lấy grid và weights từ file txt
    grid, weights = createMatrix("input.txt")

    #Điểm bắt đầu của ares, stones, switches
    start_pos, stones, switches = get_inf_in_grid(grid,weights)

    #Đặt mốc thời gian, và bộ nhớ
    start_time = time.time()
    tracemalloc.start()

    #Sử dụng thuật toán ucs để tìm đường đi, chi phí, và đếm số node được tạo ra bởi thuật toán
    cost, path, node_count = ucs_search(grid, start_pos, stones, switches)

    #Dừng thời gian và lấy thông tin bộ nhớ
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    #Quy đổi ra thời gian ra ms và bộ nhớ ra MB
    time_taken = (end_time - start_time) * 1000
    memory_usage = peak / (1024 * 1024)
    
    #In ra thông tin đã thực hiện bằng ucs
    print("UCS")
    print(f'Steps: {len(path)}, Weight: {cost}, Node: {node_count}, Time (ms): {time_taken:.2f}, Memory (MB): {memory_usage:.2f}')
    string_path = ""
    for step in path:
        string_path = string_path + str(step)
    print(string_path)

if __name__ == "__main__":
    game()
