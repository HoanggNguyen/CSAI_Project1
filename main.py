import pygame
from const import *
from support import *
from maze import *
from algos import *

dict = {
    "01": [[],[],[],[]],
    "02": [[],[],[],[]],
    "03": [[],[],[],[]],
    "04": [[],[],[],[]],
    "05": [[],[],[],[]],
    "06": [[],[],[],[]],
    "07": [[],[],[],[]],
    "08": [[],[],[],[]],
    "09": [[],[],[],[]],
    "10": [[],[],[],[]]
}

def game_screen(test_case, algorithm):
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
    sc.fill(pygame.Color(LIGHT_GRAY))
    pygame.display.flip()

    restart_sc = sc
    # Khởi tạo SearchSpace với weights, maze_data, COLS và ROWS
    g = SearchSpace(weights, maze_data, cols, rows)
    g.draw(sc)
    clock.tick(60)
    pygame.time.delay(200)

    step_count = 0

    if algorithm == "BFS" and len(dict[input_num][0]) == 0:
        costs, steps, timespent = output(sc,BFS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
        costs = [0] + costs
        dict[input_num][0] = [steps, timespent, costs]
    elif algorithm == "BFS":
        steps = dict[input_num][0][0]
        timespent = dict[input_num][0][1]
        costs = dict[input_num][0][2]
    elif algorithm == "DFS" and len(dict[input_num][1]) == 0:
        costs, steps, timespent = output(sc,DFS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
        costs = [0] + costs
        dict[input_num][1] = [steps, timespent, costs]
    elif algorithm == "DFS":
        steps = dict[input_num][1][0]
        timespent = dict[input_num][1][1]
        costs = dict[input_num][1][2]
    elif algorithm == "UCS" and len(dict[input_num][2]) == 0:
        costs, steps, timespent = output(sc,UCS, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
        costs = [0] + costs
        dict[input_num][2] = [steps, timespent, costs]
    elif algorithm == "UCS":
        steps = dict[input_num][2][0]
        timespent = dict[input_num][2][1]
        costs = dict[input_num][2][2]
    elif algorithm == "ASTAR" and len(dict[input_num][3]) == 0:
        costs, steps, timespent = output(sc,ASTAR, input_path=file_path, output_path='./output/output-'+input_num+'.txt')
        costs = [0] + costs
        dict[input_num][3] = [steps, timespent, costs]
    elif algorithm == "ASTAR":
        steps = dict[input_num][3][0]
        timespent = dict[input_num][3][1]
        costs = dict[input_num][3][2]
    else:
        print("Not implemented")
        pygame.quit()
        exit()

    if steps is None:
        display_no_solution(sc)  # Show 'No Solution' message
        pygame.time.delay(1800)
        return "algorithm", True
    
    current_step = 0
    running, paused = False, False
    run_all_pressed = False  # Thêm biến này để theo dõi trạng thái của nút Run All

    WIDTH, HEIGHT = sc.get_size()
    # Main code snippet (inside your game loop)
    current_step = 0
    current_screen = None
    running_menu = False
    running_game = True

    while running_game:
        sc.fill(pygame.Color('black'))
        g.draw(sc)
        # Display info
        draw_info(sc, step_count, timespent, g.ares_weight, g.ares_cost)  # Truyền trọng số và cost của Ares vào hàm draw_info

        # Draw buttons
        draw_buttons(sc, paused, run_all_pressed)  # Truyền trạng thái run_all_pressed vào hàm draw_buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
                BUTTON_X = WIDTH - BUTTON_WIDTH - 20  # Right margin

                # Check button areas
                if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH:  # Check button area based on BUTTON_X position
                    # Run All Button (green)
                    if HEIGHT - 180 <= y <= HEIGHT - 180 + BUTTON_HEIGHT and not run_all_pressed:
                        running, paused = True, False
                        run_all_pressed = True  # Đánh dấu nút Run All đã được ấn

                    #Restart
                    elif HEIGHT - 140 <= y <= HEIGHT - 140 + BUTTON_HEIGHT:
                        running = False
                        running_game = True
                        current_step = 0
                        step_count = 0
                        g = SearchSpace(weights, maze_data, cols, rows)
                        g.draw(restart_sc)
                        run_all_pressed = False  # Reset trạng thái của nút Run All

                    # Next Step Button (yellow)
                    elif HEIGHT - 100 <= y <= HEIGHT - 100 + BUTTON_HEIGHT:
                        if current_step < len(steps):
                            g.update_maze_step(steps[current_step], sc)  # Update the maze step
                            pygame.display.flip()
                            clock.tick(100)
                            step_count += 1
                            current_step += 1
                            running = False  # Ensure running is False to prevent automatic running
                        else:
                            running = False

                    # Pause/Continue Button (red)
                    elif HEIGHT - 60 <= y <= HEIGHT - 60 + BUTTON_HEIGHT:
                        paused = not paused  # Toggle paused state
                        running = not paused  # Ensure running state is consistent with paused state

                    #Back to home (orange)
                    elif 15 <= y <= 15 + BUTTON_HEIGHT:
                        current_screen = "algorithm"
                        running = False
                        running_menu = True
                        running_game = False

        if running and not paused:
            if current_step < len(steps):
                g.update_maze_step(steps[current_step], sc)
                pygame.display.flip()
                step_count += 1
                current_step += 1
                pygame.time.delay(200)
            else:
                running = False
    
    return current_screen, running_menu

def main():
    pygame.init()
    pygame.display.set_caption("Ares's Adventure")     
    current_screen = "test_case"

    running = True
    
    while(running):
        sc = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        sc.fill(pygame.color.Color(ASH_GRAY))
        if current_screen == "test_case":
            test_case, current_screen, running = testcase_selection_screen(sc)
        elif current_screen == "algorithm":
            algo, current_screen, running = algorithm_selection_screen(sc)
        elif current_screen == "game":
            current_screen, running = game_screen(test_case, algo)
            
if __name__ == '__main__':
    main()