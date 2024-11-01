import pygame
from const import *
import os
import time
import threading

# Hằng số để điều chỉnh kích thước của các ảnh
wall_scale = A/25*1.5
switch_scale = A/25*0.9  # Thay đổi giá trị này để điều chỉnh kích thước ảnh
stone_scale = A/25*1.25
ares_scale = A/25*0.9
# Load images from Img folder
ARES_IMG = pygame.image.load(os.path.join('Img', 'ares.png'))
STONE_IMG = pygame.image.load(os.path.join('Img', 'stone.png'))
SWITCH_IMG = pygame.image.load(os.path.join('Img', 'switch.png'))
WALL_IMG = pygame.image.load(os.path.join('Img', 'wall.png'))

# Thay đổi kích thước hình ảnh
ARES_IMG = pygame.transform.scale(ARES_IMG, (int(ARES_IMG.get_width() * ares_scale), int(ARES_IMG.get_height() * ares_scale)))
STONE_IMG = pygame.transform.scale(STONE_IMG, (int(STONE_IMG.get_width() * stone_scale), int(STONE_IMG.get_height() * stone_scale)))
SWITCH_IMG = pygame.transform.scale(SWITCH_IMG, (int(SWITCH_IMG.get_width() * switch_scale), int(SWITCH_IMG.get_height() * switch_scale)))
WALL_IMG = pygame.transform.scale(WALL_IMG, (int(WALL_IMG.get_width() * wall_scale), int(WALL_IMG.get_height() * wall_scale)))


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
        self.color = color
        self.id = id
        self.content = content  # Để giữ nội dung cụ thể (Ares, đá, v.v.)
        self.weight = weight  # Trọng số của viên đá, mặc định là None

    def draw(self, sc: pygame.Surface) -> None:
        pygame.draw.rect(sc, self.color, self.rect)
        # Vẽ nội dung trong node
        if self.content == 'Ares':
            img_rect = ARES_IMG.get_rect(center=self.rect.center)
            sc.blit(ARES_IMG, img_rect.topleft)
        elif self.content == 'Stone':
            img_rect = STONE_IMG.get_rect(center=self.rect.center)
            sc.blit(STONE_IMG, img_rect.topleft)
            # Hiển thị trọng số trên viên đá
            if self.weight is not None:
                font = pygame.font.Font(None, 24)
                text = font.render(str(self.weight), True, WHITE)
                text_rect = text.get_rect(center=self.rect.center)
                sc.blit(text, text_rect)
        elif self.content == 'Switch':
            img_rect = SWITCH_IMG.get_rect(center=self.rect.center)
            sc.blit(SWITCH_IMG, img_rect.topleft)
        elif self.content == 'Wall':
            img_rect = WALL_IMG.get_rect(center=self.rect.center)
            sc.blit(WALL_IMG, img_rect.topleft)
        elif self.content == "Stone on switch":
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
            self.color = PINK
            pygame.draw.rect(sc, self.color, self.rect)
            img_rect = SWITCH_IMG.get_rect(center=self.rect.center)
            sc.blit(SWITCH_IMG, img_rect.topleft)
            img_rect = ARES_IMG.get_rect(center=self.rect.center)
            sc.blit(ARES_IMG, img_rect.topleft)
        else:
            pygame.draw.rect(sc, self.color, self.rect)  # Không gian trống

        # Vẽ overlay lưới
        pygame.draw.rect(sc, GREY, self.rect, 1)

class SearchSpace:
    def __init__(self, weights, maze_data, cols, rows) -> None:
        self.grid_cells: list[Node] = []
        self.wall: list[Node] = []
        self.weights = weights
        self.start = None
        self.goal = None
        self.cols = cols
        self.rows = rows

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
        """Update the maze state for each move of Ares."""
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
                        current_pos.color = LIGHT_GRAY
                    else:
                        current_pos.content = None

                    current_pos.color = BLUE  # Set BLUE color for the cell Ares leaves
                    next_node.content = 'Ares on switch'
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

                    current_pos.color = BLUE  # Set BLUE color for the cell Ares leaves
                    next_node.content = 'Ares'

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

                current_pos.color = BLUE  # Set BLUE for the cell Ares leaves
            # Update Ares' new position and re-draw the maze

            self.start = next_node  # Update Ares' starting position
            self.draw(screen)  # Redraw the maze after movement
    
# New functions for button drawing and info display
def draw_info(screen, step_count, start_time, costs):
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.Font(None, 26)
    step_text = font.render(f'Steps: {step_count}', True, pygame.Color('white'))
    weight_text = font.render(f'Weight: {costs}', True, pygame.Color('white'))
    time_text = font.render(f'Time: {start_time:.2f}ms = {start_time/1000:.2f}s', True, pygame.Color('white'))
    screen.blit(step_text, (10, HEIGHT - 30))
    screen.blit(weight_text, (10, HEIGHT - 50))
    screen.blit(time_text, (10, HEIGHT - 70))

def draw_buttons(screen):
    WIDTH, HEIGHT = screen.get_size()
    BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
    BUTTON_X = WIDTH - BUTTON_WIDTH - 20  # Right margin

    # Button Y positions
    home_y = 15
    run_all_y = HEIGHT - 180
    restart_y = HEIGHT - 140
    next_step_y = HEIGHT - 100
    pause_y = HEIGHT - 60

    # Define button colors and labels
    button_info = [
        {"color": "orange", "label": "Home", "y": home_y},
        {"color": "green", "label": "Run All", "y": run_all_y},
        {"color": "pink", "label": "Restart", "y": restart_y},
        {"color": "yellow", "label": "Next Step", "y": next_step_y},
        {"color": "red", "label": "Pause", "y": pause_y}
    ]

    # Font for button labels
    font = pygame.font.Font(None, 24)  # Adjust font size as needed

    for button in button_info:
        # Draw button rectangle
        pygame.draw.rect(screen, pygame.Color(button["color"]), (BUTTON_X, button["y"], BUTTON_WIDTH, BUTTON_HEIGHT))

        # Render text and calculate position to center it on the button
        text = font.render(button["label"], True, pygame.Color('black'))
        text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, button["y"] + BUTTON_HEIGHT // 2))

        # Blit text onto the button
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(200)

# Global stop signal for the loading screen
loading_screen_running = True

def draw_loading_screen(screen, start_time):
    global loading_screen_running
    WIDTH, HEIGHT = screen.get_size()
    font_large = pygame.font.Font(None, 48)  # Font size for "Finding path..."
    font_small = pygame.font.Font(None, 24)  # Smaller font size for "Waiting time"

    # Rectangle dimensions and position for partial screen cover
    rect_width, rect_height = 300, 150
    rect_x = (WIDTH - rect_width)
    rect_y = (HEIGHT - rect_height)

    while loading_screen_running:
        # Draw the rectangle in the center
        pygame.draw.rect(screen, pygame.Color('black'), (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(screen, pygame.Color('white'), (rect_x, rect_y, rect_width, rect_height), 2)  # Border

        # Calculate elapsed time in seconds
        wait_time = int(time.time() - start_time)

        # Render text
        finding_path_text = font_large.render("Finding path...", True, pygame.Color('white'))
        waiting_time_text = font_small.render(f"Waiting time: {wait_time}s", True, pygame.Color('white'))

        # Position text in the rectangle
        finding_path_rect = finding_path_text.get_rect(center=(WIDTH - rect_width/2, HEIGHT - rect_height/2 -20))
        waiting_time_rect = waiting_time_text.get_rect(center=(WIDTH - rect_width/2, HEIGHT - rect_height/2+20))

        # Draw text onto the screen
        screen.blit(finding_path_text, finding_path_rect)
        screen.blit(waiting_time_text, waiting_time_rect)

        pygame.display.flip()

        # Update once per second
        pygame.time.delay(1000)

        # Handle any exit events (optional, can remove if not needed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def start_loading_screen(screen):
    # Start a new thread for the loading screen
    global loading_screen_running
    loading_screen_running = True
    start_time = time.time()
    loading_thread = threading.Thread(target=draw_loading_screen, args=(screen, start_time))
    loading_thread.start()
    return loading_thread

def stop_loading_screen(loading_thread):
    # Signal to stop and wait for the thread to finish
    global loading_screen_running
    loading_screen_running = False
    loading_thread.join()

def testcase_selection_screen(screen):
    WIDTH, HEIGHT = screen.get_size()

    BUTTON_WIDTH, BUTTON_HEIGHT = 250, 70
    ZOOM_FACTOR = 0.1
    left_x = WIDTH * 0.25 - BUTTON_WIDTH // 2
    right_x = WIDTH * 0.75 - BUTTON_WIDTH // 2
    start_y = 120
    GAP = int(200 * ZOOM_FACTOR)

    test_cases = [f"INPUT 0{i}" for i in range(1, 10)]
    test_cases.append(f"INPUT 10")

    buttons = []
    for i, item in enumerate(test_cases):
        x = left_x if i < 5 else right_x
        y = start_y + (i % 5) * (BUTTON_HEIGHT + GAP)
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((rect, item))

    font = pygame.font.Font(None, 40)
    
    selected_testcase = None
    running = True
    while running:
        screen.fill(pygame.Color('lightgray'))
        screen_title = "Select a Test Case"
        title_text = font.render(screen_title, True, NAVY)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        for rect, text in buttons:
            color = LIGHT_BLUE if rect.collidepoint(pygame.mouse.get_pos()) else pygame.Color('dodgerblue')
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, pygame.Color('black'), rect, 2) # ve vien
            label = font.render(text, True, WHITE)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse click is on any button
                for rect, item in buttons:
                    if rect.collidepoint(mouse_pos):
                        selected_testcase = item
                        running = False
                        curent_screen = "algorithm"
                        break
    return selected_testcase, curent_screen, True

def algorithm_selection_screen(screen):
    WIDTH, HEIGHT = screen.get_size()

    # Define button properties
    BUTTON_WIDTH, BUTTON_HEIGHT = 150, 70
    MARGIN = 20
    grid_x_start = (WIDTH - (BUTTON_WIDTH * 2 + MARGIN)) // 2
    grid_y_start = (HEIGHT - (BUTTON_HEIGHT * 2 + MARGIN)) // 2

    # Define button labels and associated algorithms
    buttons = [
        {"label": "BFS", "algo": "BFS", "x": grid_x_start, "y": grid_y_start},
        {"label": "DFS", "algo": "DFS", "x": grid_x_start + BUTTON_WIDTH + MARGIN, "y": grid_y_start},
        {"label": "UCS", "algo": "UCS", "x": grid_x_start, "y": grid_y_start + BUTTON_HEIGHT + MARGIN},
        {"label": "A*", "algo": "ASTAR", "x": grid_x_start + BUTTON_WIDTH + MARGIN, "y": grid_y_start + BUTTON_HEIGHT + MARGIN},
    ]

    # Font for button labels
    font = pygame.font.Font(None, 40)

    selected_algo = None
    running = True
    next_screen = "game"

    while running:
        # Fill the screen with a background color
        screen.fill(pygame.Color('lightgray'))

        screen_title = "Select a Search Algorithm"
        title_text = font.render(screen_title, True, NAVY)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        for button in buttons:
            # Draw each button rectangle
            rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)
            
            color = LIGHT_BLUE if rect.collidepoint(pygame.mouse.get_pos()) else pygame.Color('dodgerblue')
            pygame.draw.rect(screen, color, 
                             (button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(screen, pygame.Color('black'), 
                             (button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT), 2)  # Border

            # Render and center the label text on each button
            text = font.render(button["label"], True, pygame.Color('white'))
            text_rect = text.get_rect(center=(button["x"] + BUTTON_WIDTH // 2, button["y"] + BUTTON_HEIGHT // 2))
            screen.blit(text, text_rect)

        #Back to home
        back_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 30, BUTTON_WIDTH + 10, BUTTON_HEIGHT)
        color = LIGHT_BLUE if back_button_rect.collidepoint(pygame.mouse.get_pos()) else pygame.Color('dodgerblue')
        pygame.draw.rect(screen, color, back_button_rect)
        pygame.draw.rect(screen, pygame.Color('black'), back_button_rect,2)
        font_of_back_to_home = pygame.font.Font(None, 33)
        label = font_of_back_to_home.render("Back to home", True, pygame.Color('white'))
        label_rect = label.get_rect(center=back_button_rect.center)
        screen.blit(label, label_rect)

        pygame.display.flip()  # Update display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if mouse click is on any button
                for button in buttons:
                    if (button["x"] <= mouse_x <= button["x"] + BUTTON_WIDTH and
                        button["y"] <= mouse_y <= button["y"] + BUTTON_HEIGHT):
                        selected_algo = button["algo"]
                        running = False  # Exit the loop once an algorithm is selected
                        break
                if (back_button_rect.x <= mouse_x <= back_button_rect.x + back_button_rect.width and
                    back_button_rect.y <= mouse_y <= back_button_rect.y + back_button_rect.height):
                    next_screen = "test_case"
                    running = False
                    break

    return selected_algo, next_screen, True # Return the selected algorithm

def display_no_solution(screen):
    """Display 'No Solution' message in the center of the screen."""
    # Get screen dimensions
    WIDTH, HEIGHT = screen.get_size()

    # Set font for the message
    font = pygame.font.Font(None, 60)  # Font size for "No Solution"

    # Render the message
    no_solution_text = font.render("No Solution", True, pygame.Color('red'))

    # Calculate the position to center the text on the screen
    no_solution_rect = no_solution_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Fill the screen with a background color (optional for contrast)
    screen.fill(pygame.Color('black'))

    # Draw the "No Solution" message on the screen
    screen.blit(no_solution_text, no_solution_rect)
    pygame.display.flip()  # Update the display