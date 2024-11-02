from const import *

# Hàm đọc file input với các thông tin cần thiết
def read_input_file(file_path):
    with open(file_path, 'r') as f:
        # Đọc dòng đầu tiên chứa trọng số của các viên đá
        weights = list(map(int, f.readline().strip().split()))
        
        # Đọc các dòng tiếp theo cho maze_data, giữ lại khoảng trắng đầu dòng
        maze_data = [line.replace('\n','') for line in f if line.strip()]

    # Tính số hàng và số cột
    ROWS = len(maze_data)
    COLS = len(maze_data[0]) if ROWS > 0 else 0

    return weights, maze_data, COLS, ROWS

# Hàm đọc hàng loạt các file input từ folder và lưu vào từ điển
def read_all_input_files(folder_path):
    inputs = {}
    
    for i in range(1, 20):
        # Tạo tên file theo cấu trúc input-01.txt, input-02.txt, ...
        file_name = f"input-{i:02d}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        # Đọc dữ liệu từ file và lưu vào từ điển với key là tên file
        if os.path.exists(file_path):  # Kiểm tra xem file có tồn tại không
            inputs[file_name] = read_input_file(file_path)
    
    # Trả về từ điển chứa dữ liệu của tất cả các file input
    return inputs


class Node:
    def __init__(self, x, y, a, id, is_brick=False, color=GREY, content=None, weight=None) -> None:
        self.rect = pygame.Rect(x, y, a, a)
        self.is_brick = is_brick
        self.color = None
        self.id = id
        self.content = content  # Để giữ nội dung cụ thể (Ares, đá, v.v.)
        self.weight = weight  # Trọng số của viên đá, mặc định là None

    def draw(self, sc: pygame.Surface) -> None:
        # Vẽ nội dung trong node
        if self.content == 'Ares':
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            if self.color is not None:
                pygame.draw.rect(sc, self.color, self.rect)
            img_rect = ARES_IMG.get_rect(center=self.rect.center)
            sc.blit(ARES_IMG, img_rect.topleft)
            
        elif self.content == 'Stone':
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            img_rect = STONE_IMG.get_rect(center=self.rect.center)
            sc.blit(STONE_IMG, img_rect.topleft)
            # Hiển thị trọng số trên viên đá
            if self.weight is not None:
                font = pygame.font.Font(None, 24)
                text = font.render(str(self.weight), True, WHITE)
                text_rect = text.get_rect(center=self.rect.center)
                sc.blit(text, text_rect)
        elif self.content == 'Switch':
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            if self.color is not None:
                pygame.draw.rect(sc, self.color, self.rect)
            img_rect = SWITCH_IMG.get_rect(center=self.rect.center)
            sc.blit(SWITCH_IMG, img_rect.topleft)
        elif self.content == 'Wall':
            img_rect = WALL_IMG.get_rect(center=self.rect.center)
            sc.blit(WALL_IMG, img_rect.topleft)
        elif self.content == "Stone on switch":
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            self.color = GOLD
            pygame.draw.rect(sc, self.color, self.rect)
            img_rect = STONE_IMG.get_rect(center=self.rect.center)
            sc.blit(STONE_IMG, img_rect.topleft)
            img_rect = SWITCH_IMG.get_rect(center=self.rect.center)
            sc.blit(SWITCH_IMG, img_rect.topleft)
            # Vẫn hiển thị trọng số của viên đá trên công tắc
            if self.weight is not None:
                font = pygame.font.Font(None, 24)
                text = font.render(str(self.weight), True, WHITE)
                text_rect = text.get_rect(center=self.rect.center)
                sc.blit(text, text_rect)
        elif self.content == "Ares on switch":
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            self.color = PINK
            pygame.draw.rect(sc, self.color, self.rect)
            img_rect = SWITCH_IMG.get_rect(center=self.rect.center)
            sc.blit(SWITCH_IMG, img_rect.topleft)
            img_rect = ARES_IMG.get_rect(center=self.rect.center)
            sc.blit(ARES_IMG, img_rect.topleft)
        else:
            img_rect = FLOOR_IMG.get_rect(center=self.rect.center)
            sc.blit(FLOOR_IMG, img_rect.topleft)
            if self.color!= None:
                pygame.draw.rect(sc, self.color, self.rect)

        # Vẽ overlay lưới
        #pygame.draw.rect(sc, GREY, self.rect, 1)

class SearchSpace:
    def __init__(self, weights, maze_data, cols, rows) -> None:
        self.grid_cells: list[Node] = []
        self.wall: list[Node] = []
        self.weights = weights
        self.start = None
        self.goal = None
        self.cols = cols
        self.rows = rows
        self.ares_weight = 0  # Thêm biến này để lưu trọng số hiện tại của Ares
        self.ares_cost = 0    # Thêm biến này để lưu cost hiện tại của Ares

        self._initialize_grid(maze_data)

    def _initialize_grid(self, maze_data):
        weight_index = 0

        for i, row in enumerate(maze_data):
            for j, cell in enumerate(row):
                x, y = j * (A + A1) + BOUND, i * (A + A1) + BOUND
                node_id = i * len(row) + j
                is_brick = cell == '#'
                content = None
                weight = None  # Khởi tạo trọng số

                if cell == '#':
                    content = 'Wall'
                    node = Node(x, y, A, node_id, is_brick, content=content)
                    self.wall.append(node)
                    self.grid_cells.append(node)
                elif cell == '@':
                    content = 'Ares'
                    self.start = Node(x, y, A, node_id, is_brick, content=content)
                    self.grid_cells.append(self.start)
                elif cell == '.':
                    content = 'Switch'
                    self.goal = Node(x, y, A, node_id, is_brick, content=content)
                    self.grid_cells.append(self.goal)
                elif cell == '$':
                    content = 'Stone'
                    weight = self.weights[weight_index]  # Gán trọng số từ weights
                    weight_index += 1
                    node = Node(x, y, A, node_id, is_brick, content=content, weight=weight)
                    self.grid_cells.append(node)
                elif cell == '*':
                    content = "Stone on switch"
                    weight = self.weights[weight_index]  # Gán trọng số từ weights
                    weight_index += 1
                    node = Node(x, y, A, node_id, is_brick, content=content, weight=weight)
                    self.grid_cells.append(node)
                elif cell == '+':
                    content = "Ares on switch"
                    node = Node(x, y, A, node_id, is_brick, content=content)
                    self.start = Node(x, y, A, node_id, is_brick, content=content)
                    self.grid_cells.append(self.start)
                else:
                    self.grid_cells.append(Node(x, y, A, node_id, is_brick, content=content))

    def draw(self, sc: pygame.Surface):
        for node in self.grid_cells:
            node.draw(sc)

        pygame.display.flip()  # Chỉ cần gọi flip một lần sau khi tất cả đã được vẽ

    def get_length(self):
        return len(self.grid_cells)

    def is_goal(self):
        """Kiểm tra xem tất cả các công tắc có được kích hoạt không."""
        return all(node.content != 'Switch' for node in self.grid_cells if node.content == 'Stone')

    def update_maze_step(self, step, screen):
        current_pos = self.start  # Ares' current node
        direction = step.lower()  # Get the move direction

        # Translate the direction to coordinate changes
        dx, dy = 0, 0
        if direction == 'u':
            dy = -1
        elif direction == 'd':
            dy = 1
        elif direction == 'l':
            dx = -1
        elif direction == 'r':
            dx = 1

        # Calculate Ares' next position
        next_x = current_pos.rect.x + dx * (A + A1)
        next_y = current_pos.rect.y + dy * (A + A1)

        # Find the next node based on new position
        next_node = next((node for node in self.grid_cells if node.rect.x == next_x and node.rect.y == next_y), None)

        if next_node:
            if next_node.content == 'Stone on switch':
                stone_next_x = next_x + dx * (A + A1)
                stone_next_y = next_y + dy * (A + A1)
                stone_next_node = next((node for node in self.grid_cells if node.rect.x == stone_next_x and node.rect.y == stone_next_y), None)
                if stone_next_node and stone_next_node.content in [None, 'Switch']:  # Check if the stone can be pushed
                    # Update stone and switch state if necessary
                    if stone_next_node.content == 'Switch':
                        stone_next_node.content = 'Stone on switch'
                        stone_next_node.weight = next_node.weight
                        stone_next_node.color = GOLD  # Change color to GOLD for stone on switch
                    else:
                        stone_next_node.content = 'Stone'
                        stone_next_node.weight = next_node.weight
                    #next_node.content = 'Ares on switch'  # Remove stone from the old cell
                    next_node.weight = None

                    # Update Ares' position after pushing the stone
                    if current_pos.content == 'Ares on switch':
                        current_pos.content = 'Switch'  # Restore switch when Ares leaves
                        current_pos.color = STONE
                    else:
                        current_pos.content = None

                    current_pos.color = STONE  # Set STONE color for the cell Ares leaves
                    next_node.content = 'Ares on switch'
                    self.ares_weight += stone_next_node.weight  # Cập nhật trọng số của Ares khi đẩy đá
                    self.ares_cost += stone_next_node.weight + 1  # Cập nhật cost của Ares khi đẩy đá
            elif next_node.content == 'Stone':  # Check if pushing a stone
                # Calculate the stone's next position when pushed
                stone_next_x = next_x + dx * (A + A1)
                stone_next_y = next_y + dy * (A + A1)
                stone_next_node = next((node for node in self.grid_cells if node.rect.x == stone_next_x and node.rect.y == stone_next_y), None)

                if stone_next_node and stone_next_node.content in [None, 'Switch']:  # Check if the stone can be pushed
                    # Update stone and switch state if necessary
                    if stone_next_node.content == 'Switch':
                        stone_next_node.content = 'Stone on switch'
                        stone_next_node.weight = next_node.weight
                        stone_next_node.color = GOLD  # Change color to GOLD for stone on switch
                
                    else:
                        stone_next_node.content = 'Stone'
                        stone_next_node.weight = next_node.weight
                    #next_node.content = None  # Remove stone from the old cell
                    next_node.weight = None

                    # Update Ares' position after pushing the stone
                    if current_pos.content == 'Ares on switch':
                        current_pos.content = 'Switch'  # Restore switch when Ares leaves
                        current_pos.color = LIGHT_GRAY
                    else:
                        current_pos.content = None

                    current_pos.color = STONE  # Set STONE color for the cell Ares leaves
                    next_node.content = 'Ares'
                    self.ares_weight += stone_next_node.weight  # Cập nhật trọng số của Ares khi đẩy đá
                    self.ares_cost += stone_next_node.weight + 1  # Cập nhật cost của Ares khi đẩy đá

            elif next_node.content in [None, 'Switch']:  # Move Ares if the next node is empty or a switch
                if next_node.content == 'Switch':
                    next_node.content = 'Ares on switch'
                else:
                    next_node.content = 'Ares'

                # Restore switch status or clear old Ares position
                if current_pos.content == 'Ares on switch':
                    current_pos.content = 'Switch'  # Restore switch when Ares leaves
                else:
                    current_pos.content = None  # Clear Ares from the old cell

                current_pos.color = STONE  # Set STONE for the cell Ares leaves
                self.ares_cost += 1  # Cập nhật cost của Ares khi di chuyển
            # Update Ares' new position and re-draw the maze

            self.start = next_node  # Update Ares' starting position
            self.draw(screen)  # Redraw the maze after movement
    