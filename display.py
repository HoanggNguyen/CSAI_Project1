from maze import*
from support import output
from algos import *
import sys

# New functions for button drawing and info display
def draw_info(screen, step_count, start_time, ares_weight, ares_cost, total_step,speed=1):
    WIDTH, HEIGHT = screen.get_size()

    font = pygame.font.Font(font_path, 18)
    total_step = font.render(f'Total Steps: {total_step}', True, pygame.Color('white'))
    time_text = font.render(f'Total Time: {start_time:.2f}ms ~ {start_time/1000:.2f}s', True, pygame.Color('white'))
    current = font.render(f'== Current state == (speed {speed}x)', True, pygame.Color('white'))
    step_text = font.render(f'Steps count: {step_count}, Cost: {ares_cost}, Weight: {ares_weight}', True, pygame.Color('white'))
    screen.blit(time_text, (10, HEIGHT - 100))
    screen.blit(total_step, (10, HEIGHT - 80))
    screen.blit(current, (10, HEIGHT - 60))
    screen.blit(step_text, (10, HEIGHT - 40))

def draw_buttons(screen, paused, run_all_pressed):
    WIDTH, HEIGHT = screen.get_size()
    BUTTON_WIDTH, BUTTON_HEIGHT = 110, 30
    BUTTON_X = WIDTH - BUTTON_WIDTH - 20  # Right margin

    # Button Y positions
    home_y = 15
    back_y = home_y + BUTTON_HEIGHT + 10  # Place Back button below Home
    speed_up_y = back_y + BUTTON_HEIGHT + 10  # Place Speed up button below Back
    run_all_y = HEIGHT - 180
    restart_y = HEIGHT - 140
    next_step_y = HEIGHT - 100
    pause_y = HEIGHT - 60

    # Load the button images
    button_image = pygame.transform.scale(button_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    light_button_image = pygame.transform.scale(light_button_image2, (BUTTON_WIDTH, BUTTON_HEIGHT))  # Light version

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Define button labels and their positions
    button_info = [
        {"label": "Home", "y": home_y, "enabled": True},
        {"label": "Back", "y": back_y, "enabled": True},
        {"label": "Speed up", "y": speed_up_y, "enabled": True},
        {"label": "Run All", "y": run_all_y, "enabled": not run_all_pressed},
        {"label": "Restart", "y": restart_y, "enabled": True},
        {"label": "Next Step", "y": next_step_y, "enabled": True},
        {"label": "Continue" if paused else "Pause", "y": pause_y}
    ]

    # Font for button labels
    font = pygame.font.Font(font_path, 18)  # Adjust font size as needed

    for button in button_info:
        button_y = button["y"]
        # Determine if mouse is hovering over the button
        is_hovered = (BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and button_y <= mouse_y <= button_y + BUTTON_HEIGHT)
        
        # Select image based on hover state
        if button.get("enabled", True):
            image_to_use = light_button_image if is_hovered else button_image
            screen.blit(image_to_use, (BUTTON_X, button_y))
        else:
            image_to_use = light_button_image
            screen.blit(image_to_use, (BUTTON_X, button_y))
        
        # Render text and calculate position to center it on the button
        text = font.render(button["label"], True, pygame.Color('White'))
        text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
        
        # Blit text onto the button image
        screen.blit(text, text_rect)

# Global stop signal for the loading screen
loading_screen_running = True

def testcase_selection_screen(screen, state, background_image, button_img, light_button_image):
    WIDTH, HEIGHT = 480, 720
    BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50  # Kích thước nút
    MARGIN = 50  # Lề bên
    BUTTON_GAP = 15  # Khoảng cách giữa các nút

    # Load button images
    button_img.convert_alpha()
    light_button_image.convert_alpha()

    # Calculate button positions
    left_x = MARGIN  # Vị trí X cho cột bên trái
    right_x = WIDTH - BUTTON_WIDTH - MARGIN  # Vị trí X cho cột bên phải
    start_y = 220  # Vị trí Y bắt đầu cho nút

    # Tạo danh sách test cases bao gồm thêm INPUT 11 và INPUT 12
    test_cases = [f"INPUT 0{i}" for i in range(1, 10)] 
    test_cases.append(f"INPUT 10")
    test_cases.append(f"INPUT 11")
    test_cases.append(f"INPUT 12")

    # Vị trí của nút Back
    back_button_x = MARGIN  # 30 pixels từ bên trái
    back_button_y = HEIGHT - BUTTON_HEIGHT - MARGIN  # 30 pixels từ bên dưới
    # Vị trí của nút More
    more_button_x = WIDTH - MARGIN - BUTTON_WIDTH  # 30 pixels từ bên phải
    more_button_y = HEIGHT - BUTTON_HEIGHT - MARGIN  # 30 pixels từ bên dưới

    # Khởi tạo danh sách các nút
    buttons = []
    for i, item in enumerate(test_cases):
        y = start_y + (i % 6) * (BUTTON_HEIGHT + BUTTON_GAP)  # Tính toán vị trí Y
        x = left_x if i < 6 else right_x  # Tính toán vị trí X cho từng cột
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((rect, item))

    # Cài đặt font
    font_path = "./Fonts/Quantico-Bold.ttf"
    font_path2 = "./Fonts/Quantico-Bold.ttf"
    button_font = pygame.font.Font(font_path2, 22)  # Font cho các nút
    title_font = pygame.font.Font(font_path2, 42)  # Font tiêu đề
    sub_font = pygame.font.Font(font_path, 26)
    sub_font2 = pygame.font.Font(font_path, 16)
    selected_testcase = None
    running = True

    while running:
        # Vẽ hình nền
        screen.blit(background_image, (0, 0))

        # Tiêu đề và phụ đề màn hình
        screen_title = "New Adventure" if state == "new" else "Review Journey"
        screen_subtitle = "Pick Map Carefully!!!"
        screen_subtitle2 = "You Could Strike Gold or Stumble into Trouble!"

        # Vẽ tiêu đề và phụ đề
        title_text = sub_font.render(screen_title, True, (44, 61, 88))
        sub_text = title_font.render(screen_subtitle, True, (44, 61, 88))
        sub_text2 = sub_font2.render(screen_subtitle2, True, (44, 61, 88))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 90))
        screen.blit(sub_text2, (WIDTH // 2 - sub_text2.get_width() // 2, 160))

        # Vẽ các nút
        for rect, text in buttons:
            button_to_draw = pygame.transform.scale(light_button_image if rect.collidepoint(pygame.mouse.get_pos()) else button_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
            screen.blit(button_to_draw, rect.topleft)
            label = button_font.render(text, True, WHITE)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
        
        # Vẽ nút Back
        back_button_rect = pygame.Rect(back_button_x, back_button_y, BUTTON_WIDTH / 2, BUTTON_HEIGHT)
        scaled_back_button_img = pygame.transform.scale(light_button_image if back_button_rect.collidepoint(pygame.mouse.get_pos()) else button_img, (BUTTON_WIDTH / 2, BUTTON_HEIGHT))
        screen.blit(scaled_back_button_img, back_button_rect.topleft)
        
        label = button_font.render("Back", True, WHITE)
        label_rect = label.get_rect(center=back_button_rect.center)
        screen.blit(label, label_rect)

        # Vẽ nút More input
        more_button_rect = pygame.Rect(more_button_x, more_button_y, BUTTON_WIDTH , BUTTON_HEIGHT)
        scaled_more_button_img = pygame.transform.scale(light_button_image if more_button_rect.collidepoint(pygame.mouse.get_pos()) else button_img, (BUTTON_WIDTH , BUTTON_HEIGHT))
        screen.blit(scaled_more_button_img, more_button_rect.topleft)
        
        label2 = button_font.render("More Input", True, WHITE)
        label_rect2 = label2.get_rect(center=more_button_rect.center)
        screen.blit(label2, label_rect2)

        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Kiểm tra nhấp chuột vào nút
                for rect, item in buttons:
                    if rect.collidepoint(mouse_pos):
                        selected_testcase = item
                        running = False
                        current_screen = "algorithm"
                        break
                # Kiểm tra nhấp chuột vào nút Back
                if back_button_rect.collidepoint(mouse_pos):
                    current_screen = "menu"
                    running = False
                    break
                # Kiểm tra nhấp chuột vào nút more
                if more_button_rect.collidepoint(mouse_pos):
                    current_screen = "test_case2"
                    running = False
                    break

    return selected_testcase, current_screen, True


def testcase_selection_screen2(screen, state, background_image, button_img, light_button_image):
    WIDTH, HEIGHT = 480, 720

    BUTTON_WIDTH, BUTTON_HEIGHT = 140, 50  # Adjusted size of the buttons
    MARGIN = 30  # Margin on each side
    BUTTON_GAP = 30  # Minimum gap between buttons
    
    #screen = pygame.display.set_mode((480, 720))
    # Load button images
    button_img.convert_alpha()
    light_button_image.convert_alpha()
    
    # Calculate button positions based on margins and gaps
    start_y = 250  # Starting Y position for main buttons

    buttons = [
        {"label": "INPUT 13", "y": start_y},
        {"label": "INPUT 14", "y": start_y + BUTTON_HEIGHT + BUTTON_GAP},
        {"label": "INPUT 15", "y": start_y + 2 * (BUTTON_HEIGHT + BUTTON_GAP)},
        {"label": "INPUT 16", "y": start_y + 3 * (BUTTON_HEIGHT + BUTTON_GAP)},
    ]

    # Centering buttons
    for button in buttons:
        button["x"] = (WIDTH - BUTTON_WIDTH) // 2  # Center X position for buttons

    # Back button position
    back_button_x = MARGIN  # 30 pixels from the left
    back_button_y = HEIGHT - BUTTON_HEIGHT - MARGIN   # 30 pixels from the bottom

    
    selected_testcase = None
    running = True
    next_screen = "algorithm"
    # Cài đặt font
    font_path = "./Fonts/Quantico-Bold.ttf"
    font_path2 = "./Fonts/Quantico-Bold.ttf"
    button_font = pygame.font.Font(font_path2, 22)  # Font cho các nút
    title_font = pygame.font.Font(font_path2, 42)  # Font tiêu đề
    sub_font = pygame.font.Font(font_path, 26)
    sub_font2 = pygame.font.Font(font_path, 16)
    selected_testcase = None
    running = True

    while running:
        # Vẽ hình nền
        screen.blit(background_image, (0, 0))

        # Tiêu đề và phụ đề màn hình
        screen_title = "New Adventure" if state == "new" else "Review Journey"
        screen_subtitle = "Pick Map Carefully!!!"
        screen_subtitle2 = "You Could Strike Gold or Stumble into Trouble!"

        # Vẽ tiêu đề và phụ đề
        title_text = sub_font.render(screen_title, True, (44, 61, 88))
        sub_text = title_font.render(screen_subtitle, True, (44, 61, 88))
        sub_text2 = sub_font2.render(screen_subtitle2, True, (44, 61, 88))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 90))
        screen.blit(sub_text2, (WIDTH // 2 - sub_text2.get_width() // 2, 160))

        # Draw main buttons
        for button in buttons:
            rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)

            if rect.collidepoint(pygame.mouse.get_pos()):
                button_to_draw = pygame.transform.scale(light_button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

            else:
                button_to_draw = pygame.transform.scale(button_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

            screen.blit(button_to_draw, rect.topleft)

            text = button_font.render(button["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw Back button
        back_button_rect = pygame.Rect(back_button_x, back_button_y, BUTTON_WIDTH/2, BUTTON_HEIGHT)
        
        # Scale the back button image to fit the new width
        scaled_back_button_img = pygame.transform.scale(button_img, (BUTTON_WIDTH/2, BUTTON_HEIGHT))

        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            scaled_back_button_img = pygame.transform.scale(light_button_image, (BUTTON_WIDTH/2, BUTTON_HEIGHT))

        screen.blit(scaled_back_button_img, back_button_rect.topleft)

        label = button_font.render("Back", True, (255, 255, 255))
        label_rect = label.get_rect(center=back_button_rect.center)
        screen.blit(label, label_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button in buttons:
                    if (button["x"] <= mouse_x <= button["x"] + BUTTON_WIDTH and
                            button["y"] <= mouse_y <= button["y"] + BUTTON_HEIGHT):
                        selected_testcase = button["label"]
                        running = False
                        break
                if (back_button_rect.x <= mouse_x <= back_button_rect.x + back_button_rect.width and
                        back_button_rect.y <= mouse_y <= back_button_rect.y + back_button_rect.height):
                    next_screen = "test_case"
                    running = False
                    break

    return selected_testcase, next_screen, True


def algorithm_selection_screen(screen, state, background_image, button_img, light_button_image):
    WIDTH, HEIGHT = 480, 720

    BUTTON_WIDTH, BUTTON_HEIGHT = 140, 50  # Adjusted size of the buttons
    MARGIN = 30  # Margin on each side
    BUTTON_GAP = 30  # Minimum gap between buttons
    
    #screen = pygame.display.set_mode((480, 720))
    # Load button images
    button_img.convert_alpha()
    light_button_image.convert_alpha()
    
    # Calculate button positions based on margins and gaps
    start_y = 250  # Starting Y position for main buttons

    buttons = [
        {"label": "BFS", "algo": "BFS", "y": start_y},
        {"label": "DFS", "algo": "DFS", "y": start_y + BUTTON_HEIGHT + BUTTON_GAP},
        {"label": "UCS", "algo": "UCS", "y": start_y + 2 * (BUTTON_HEIGHT + BUTTON_GAP)},
        {"label": "A*", "algo": "ASTAR", "y": start_y + 3 * (BUTTON_HEIGHT + BUTTON_GAP)},
    ]

    # Centering buttons
    for button in buttons:
        button["x"] = (WIDTH - BUTTON_WIDTH) // 2  # Center X position for buttons

    # Back button position
    back_button_x = MARGIN  # 30 pixels from the left
    back_button_y = HEIGHT - BUTTON_HEIGHT - MARGIN   # 30 pixels from the bottom

    font_path = "./Fonts/Quantico-Bold.ttf"
    button_font = pygame.font.Font(font_path, 22)  # Set the font size for buttons
    title_font = pygame.font.Font(font_path, 42)  # Title font size
    sub_font = pygame.font.Font(font_path, 26)
    sub_font2 = pygame.font.Font(font_path, 16)
    
    selected_algo = None
    running = True
    next_screen = "game"

    while running:
        screen.blit(background_image, (0, 0))
        
        if state == "new":
            screen_title = "New Adventure"
        elif state == "old":
            screen_title = "Review Journey"

        screen_subtitle = "Wise Algorithm"
        screen_subtitle2 = "It Could Lead You to Glory (or a Maze of Confusion)!"

        title_text = sub_font.render(screen_title, True, (44, 61, 88))
        sub_text = title_font.render(screen_subtitle, True, (44, 61, 88))
        sub_text2 = sub_font2.render(screen_subtitle2, True, (44, 61, 88))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, 90))
        screen.blit(sub_text2, (WIDTH // 2 - sub_text2.get_width() // 2, 160))

        # Draw main buttons
        for button in buttons:
            rect = pygame.Rect(button["x"], button["y"], BUTTON_WIDTH, BUTTON_HEIGHT)

            if rect.collidepoint(pygame.mouse.get_pos()):
                button_to_draw = pygame.transform.scale(light_button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

            else:
                button_to_draw = pygame.transform.scale(button_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

            screen.blit(button_to_draw, rect.topleft)

            text = button_font.render(button["label"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw Back button
        back_button_rect = pygame.Rect(back_button_x, back_button_y, BUTTON_WIDTH/2, BUTTON_HEIGHT)
        
        # Scale the back button image to fit the new width
        scaled_back_button_img = pygame.transform.scale(button_img, (BUTTON_WIDTH/2, BUTTON_HEIGHT))
        
        if back_button_rect.collidepoint(pygame.mouse.get_pos()):
            scaled_back_button_img = pygame.transform.scale(light_button_image, (BUTTON_WIDTH/2, BUTTON_HEIGHT))
        
        screen.blit(scaled_back_button_img, back_button_rect.topleft)
        
        label = button_font.render("Back", True, (255, 255, 255))
        label_rect = label.get_rect(center=back_button_rect.center)
        screen.blit(label, label_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button in buttons:
                    if (button["x"] <= mouse_x <= button["x"] + BUTTON_WIDTH and
                            button["y"] <= mouse_y <= button["y"] + BUTTON_HEIGHT):
                        selected_algo = button["algo"]
                        running = False
                        break
                if (back_button_rect.x <= mouse_x <= back_button_rect.x + back_button_rect.width and
                        back_button_rect.y <= mouse_y <= back_button_rect.y + back_button_rect.height):
                    next_screen = "test_case"
                    running = False
                    break

    return selected_algo, next_screen, True

def display_no_solution(screen):
    """Display 'No Solution' message in the center of the screen."""
    # Get screen dimensions
    WIDTH, HEIGHT = (480, 720)
    
    screen = pygame.display.set_mode((480, 720))
    
    background_image3 = pygame.transform.scale(background_image2, (480, 720))

    # Set font for the message
    font = pygame.font.Font(font_path, 52) # Font size for "No Solution"

    # Render the message
    no_solution_text = font.render("No Solution", True, pygame.Color('red'))

    # Calculate the position to center the text on the screen
    no_solution_rect = no_solution_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Draw the "No Solution" message on the screen
    screen.blit(no_solution_text, no_solution_rect)
    pygame.display.flip()  # Update the display

screen_width, screen_height = 480, 720

def draw_menu(screen, current_screen):
    """Function to draw the main menu on the given screen."""
    # Load fonts and setup font size for buttons
    font_path = "./Fonts/Quantico-Bold.ttf"
    title_font = pygame.font.Font(font_path, 74)
    button_font = pygame.font.Font(font_path, 26)

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw title text, center-aligned
    title_text1 = title_font.render("Ares's", True, (44, 61, 88))
    title_text2 = title_font.render("Adventure", True, (44, 61, 88))
    title_text1_rect = title_text1.get_rect(center=(screen.get_width() // 2, 100))
    title_text2_rect = title_text2.get_rect(center=(screen.get_width() // 2, 180))
    screen.blit(title_text1, title_text1_rect)
    screen.blit(title_text2, title_text2_rect)

    # Get the mouse position for hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Define padding for button width adjustment
    padding_x = 20  # Horizontal padding for button width

    # Draw each button with hover effect and adjusted size
    for text, y_pos in button_positions.items():
        # Render button text and get its width
        button_text = button_font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect()
        button_width = text_rect.width + padding_x * 2  # Calculate button width based on text

        # Resize button images based on calculated width
        resized_button_img = pygame.transform.scale(button_img, (button_width, text_rect.height + 10))
        resized_light_button_img = pygame.transform.scale(light_button_image2, (button_width, text_rect.height + 10))

        # Determine if the button is hovered
        button_image2 = resized_light_button_img if resized_button_img.get_rect(center=(screen.get_width() // 2, y_pos)).collidepoint(mouse_x, mouse_y) else resized_button_img
        
        # Draw the resized button at the specified position
        button_rect = button_image2.get_rect(center=(screen.get_width() // 2, y_pos))
        screen.blit(button_image2, button_rect)
        
        # Center the text on the button
        text_rect.center = button_rect.center
        screen.blit(button_text, text_rect)

    # Event handling for button clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for text, pos in button_positions.items():
                button_rect = resized_button_img.get_rect(center=(screen.get_width() // 2, pos))
                if button_rect.collidepoint(mouse_pos):
                    print(f"{text} button clicked")
                    current_screen = text
                    if text == "Quit Game":
                        pygame.quit()
                        sys.exit()
                    elif text == "Start New Adventure":
                        return "test_case", "new"  # Set to test case selection screen
                    elif text == "Review Journey":
                        return "test_case", "old"
                    elif text == "How to play":
                        return "howto", None  # Adjusted this line for clarity

    return current_screen, "old"


dict2 = {
    "01": [[],[],[],[]],
    "02": [[],[],[],[]],
    "03": [[],[],[],[]],
    "04": [[],[],[],[]],
    "05": [[],[],[],[]],
    "06": [[],[],[],[]],
    "07": [[],[],[],[]],
    "08": [[],[],[],[]],
    "09": [[],[],[],[]],
    "10": [[],[],[],[]],
    "11": [[],[],[],[]],
    "12": [[],[],[],[]],
    "13": [[],[],[],[]],
    "14": [[],[],[],[]],
    "15": [[],[],[],[]],
    "16": [[],[],[],[]]
}

def game_screen(sc,state, test_case, algorithm):
    clock = pygame.time.Clock()

    #Lấy test_case
    input_num = test_case[6:]
    file = "input-"+ input_num +".txt"
    folder_path = './input'
    file_path = folder_path + '/' + file

    # Đọc dữ liệu từ file input và khởi tạo maze
    all_inputs = read_all_input_files(folder_path)
    weights, maze_data, cols, rows = all_inputs.get(file, ([], [], 0, 0))

    RES = set_dimensions(cols, rows)
    sc = pygame.display.set_mode(RES)
    background_image3 = pygame.transform.scale(background_image2, RES)
    sc.blit(background_image3, (0, 0))
    pygame.display.flip()

    restart_sc = sc

    # Khởi tạo SearchSpace với weights, maze_data, COLS và ROWS
    g = SearchSpace(weights, maze_data, cols, rows)
    g.draw(sc)
    clock.tick(60)
    pygame.time.delay(200)

    if state == "new":
        step_count = 0

        if algorithm == "BFS" and len(dict2[input_num][0]) == 0:
            costs, steps, timespent, total_step = output(sc,BFS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
            costs = [0] + costs
            dict2[input_num][0] = [steps, timespent, costs, total_step]
        elif algorithm == "BFS":
            steps = dict2[input_num][0][0]
            timespent = dict2[input_num][0][1]
            costs = dict2[input_num][0][2]
            total_step = dict2[input_num][0][3]
        elif algorithm == "DFS" and len(dict2[input_num][1]) == 0:
            costs, steps, timespent, total_step = output(sc,DFS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
            costs = [0] + costs
            dict2[input_num][1] = [steps, timespent, costs, total_step]
        elif algorithm == "DFS":
            steps = dict2[input_num][1][0]
            timespent = dict2[input_num][1][1]
            costs = dict2[input_num][1][2]
            total_step = dict2[input_num][1][3]
        elif algorithm == "UCS" and len(dict2[input_num][2]) == 0:
            costs, steps, timespent, total_step = output(sc,UCS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
            costs = [0] + costs
            dict2[input_num][2] = [steps, timespent, costs, total_step]
        elif algorithm == "UCS":
            steps = dict2[input_num][2][0]
            timespent = dict2[input_num][2][1]
            costs = dict2[input_num][2][2]
            total_step = dict2[input_num][2][3]
        elif algorithm == "ASTAR" and len(dict2[input_num][3]) == 0:
            costs, steps, timespent, total_step = output(sc,ASTAR, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
            costs = [0] + costs
            dict2[input_num][3] = [steps, timespent, costs, total_step]
        elif algorithm == "ASTAR":
            steps = dict2[input_num][3][0]
            timespent = dict2[input_num][3][1]
            costs = dict2[input_num][3][2]
            total_step = dict2[input_num][3][3]
        else:
            print("Not implemented")
            pygame.quit()
            exit()
    elif state == "old":
        
        dict = load_results_from_json('./output-restored/results.json')
        # BFS
        if algorithm == "BFS":
            steps = dict[input_num][0][0]   
            timespent = dict[input_num][0][1]
            costs = dict[input_num][0][2]
            total_step = dict[input_num][0][3]
        # DFS
        elif algorithm == "DFS":
            steps = dict[input_num][1][0]
            timespent = dict[input_num][1][1]
            costs = dict[input_num][1][2]
            total_step = dict[input_num][1][3]
        #UCS
        elif algorithm == "UCS":
            steps = dict[input_num][2][0]
            timespent = dict[input_num][2][1]
            costs = dict[input_num][2][2]
            total_step = dict[input_num][2][3]
        #ASTAR
        elif algorithm == "ASTAR":
            steps = dict[input_num][3][0]
            timespent = dict[input_num][3][1]
            costs = dict[input_num][3][2]
            total_step = dict[input_num][3][3]
    if steps is None:
        display_no_solution(sc)  # Show 'No Solution' message
        pygame.time.delay(1800)
        return "algorithm", True
    
    current_step = 0
    running, paused = False, False
    run_all_pressed = False  # Thêm biến này để theo dõi trạng thái của nút Run All

    WIDTH, HEIGHT = sc.get_size()
    # Main code snippet (inside your game loop)
    speed = 1
    step_count = 0
    current_screen = None
    running_menu = False
    running_game = True

    
    while running_game:
        
        sc.blit(background_image3, (0, 0))

        # Draw buttons
        draw_buttons(sc, paused, run_all_pressed)
        draw_info(sc, step_count, timespent, g.ares_weight, g.ares_cost, total_step,speed)
        
        g.draw(sc)

        # Truyền trạng thái run_all_pressed vào hàm draw_buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
                BUTTON_X = sc.get_width() - BUTTON_WIDTH - 20  # Right margin

                back_y = 15 + BUTTON_HEIGHT + 10  # Back button Y position
                speed_up_y = back_y + BUTTON_HEIGHT + 10  # Speed Up button Y position
                
                # Check button areas
                if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH:  # Check button area based on BUTTON_X position
                    # Run All Button (green)
                    if HEIGHT - 180 <= y <= HEIGHT - 180 + BUTTON_HEIGHT and not run_all_pressed:
                        running, paused = True, False
                        run_all_pressed = True  # Mark Run All button as pressed

                    # Speed Up Button (blue)
                    if speed_up_y <= y <= speed_up_y + BUTTON_HEIGHT:
                        speed += 1  # Increase speed value when the button is clicked
                        draw_buttons(sc, paused, run_all_pressed)

                    # Restart Button (pink)
                    elif HEIGHT - 140 <= y <= HEIGHT - 140 + BUTTON_HEIGHT:
                        running = False
                        running_game = True
                        current_step = 0
                        step_count = 0
                        speed = 1
                        g = SearchSpace(weights, maze_data, cols, rows)
                        g.draw(restart_sc)  # Redraw maze after reset
                        run_all_pressed = False

                    # Next Step Button (yellow)
                    elif HEIGHT - 100 <= y <= HEIGHT - 100 + BUTTON_HEIGHT:
                        if current_step < len(steps):
                            g.update_maze_step(steps[current_step], sc)  # Update the maze step
                            pygame.display.flip()
                            clock.tick(100)
                            step_count += 1
                            current_step += 1
                            running = False  # Prevent automatic running
                        else:
                            running = False

                    # Pause/Continue Button (red)
                    elif HEIGHT - 60 <= y <= HEIGHT - 60 + BUTTON_HEIGHT:
                        paused = not paused  # Toggle paused state
                        running = not paused  # Ensure running state is consistent with paused state

                # Back to Home Button (orange)
                if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and 15 <= y <= 15 + BUTTON_HEIGHT:
                    current_screen = "menu"
                    running_game = False  # Exit the game loop
                    running_menu = True  # Set menu state
                # Back
                elif BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and 15 + BUTTON_HEIGHT + 10  <= y <= 15 + BUTTON_HEIGHT + 10  + BUTTON_HEIGHT:
                    current_screen = "algorithm"  # Set screen to return to algorithm
                    running_game = False  # Exit the game loop
                    running_menu = True  # Set menu state
                    running = False

        if running and not paused:
            if current_step < len(steps):
                g.update_maze_step(steps[current_step], sc)
                pygame.display.flip()
                step_count += 1
                current_step += 1
                pygame.time.delay(int(500 / speed))
            else:
                running = False
    sc = pygame.display.set_mode((480, 720))
    
    return current_screen, running_menu

def show_how_to_play(screen, button_img, light_button_image):
    # Load background image
    background_image = pygame.image.load('./Img/Menu/Howtoplay.png')
    screen.blit(background_image, (0, 0))  # Display the background image

    # Set button parameters
    BUTTON_WIDTH = 200  # Define the button width
    BUTTON_HEIGHT = 50  # Define the button height
    back_button_x = (screen.get_width() - (BUTTON_WIDTH / 2)) // 2  # Center the button
    back_button_y = screen.get_height() - BUTTON_HEIGHT - 20  # Position it near the bottom

    

    # Draw Back button
    back_button_rect = pygame.Rect(back_button_x, back_button_y, BUTTON_WIDTH / 2, BUTTON_HEIGHT)

    # Event handling loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button_rect.collidepoint(event.pos):
                    return "menu", None  # Return to menu screen

        # Update button image based on hover state
        scaled_back_button_img = pygame.transform.scale(
            light_button_image if back_button_rect.collidepoint(pygame.mouse.get_pos()) else button_img,
            (BUTTON_WIDTH / 2, BUTTON_HEIGHT)
        )
        screen.blit(scaled_back_button_img, back_button_rect.topleft)

        # Render the label
        button_font = pygame.font.Font(None, 36)  # Set your font and size
        label = button_font.render("Back", True, (255, 255, 255))  # WHITE color
        label_rect = label.get_rect(center=back_button_rect.center)
        screen.blit(label, label_rect)

        pygame.display.flip()  # Update the display
