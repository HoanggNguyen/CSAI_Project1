import pygame
import time
from const import *
from support import *
from maze import *
from algos import *

def main():

    input_num = '01'
    file = 'input-' + input_num + '.txt'
    folder_path = './input'
    file_path = folder_path + '/' + file
    your_name = 'Le Tran Minh Khue - 21120279'
    algo = 'BFS'
    # Đọc dữ liệu từ file input và khởi tạo maze
    all_inputs = read_all_input_files(folder_path)
    weights, maze_data, cols, rows = all_inputs.get(file, ([], [], 0, 0))
    RES = set_dimensions(cols, rows)

    pygame.init()
    pygame.display.set_caption(f'{your_name} - {algo}')
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    sc.fill(pygame.color.Color(ASH_GRAY))
    algo = algorithm_selection_screen(sc)
    sc.fill(pygame.Color(LIGHT_GRAY))
    pygame.display.flip()
    # Khởi tạo SearchSpace với weights, maze_data, COLS và ROWS
    g = SearchSpace(weights, maze_data, cols, rows)
    g.draw(sc)
    clock.tick(60)
    pygame.time.delay(200)

    step_count = 0

    if algo == "BFS":
        steps, timespent = output(sc,BFS, input_path=file_path, output_path='./output/output-bfs-'+input_num+'.txt')
    elif algo == "DFS":
        #steps, timespent = output(sc,DFS, input_path=file_path, output_path='./output/output-dfs-'+input_num+'.txt')
        print("Not Implemented")
        pygame.quit()
        exit()
    elif algo == "UCS":
        #steps, timespent = output(sc,DFS, input_path=file_path, output_path='./output/output-ucs-'+input_num+'.txt')
        print("Not Implemented")
        pygame.quit()
        exit()
    elif algo == "ASTAR":
        steps, timespent = output(sc,ASTAR, input_path=file_path, output_path='./output/output-astar-'+input_num+'.txt')
    else:
        print("Not implemented")
        pygame.quit()
        exit()

    if steps is None:
        display_no_solution(sc)  # Show 'No Solution' message
        pygame.time.delay(3000)
        pygame.quit()
        exit()
        return
    
    current_step = 0
    running, paused = False, False

    WIDTH, HEIGHT = sc.get_size()
    # Main code snippet (inside your game loop)
    speed = 1
    current_step = 0
<<<<<<< Updated upstream
    while True:
        sc.fill(pygame.Color('black'))
        g.draw(sc)

        # Display info
=======
    current_screen = None
    running_menu = False
    running_game = True
    sc.fill(pygame.Color('black'))
    
    g.draw(sc)

    # Display info
    draw_info(sc, step_count, timespent)
    
    # Draw buttons
    draw_buttons(sc)
    
    while running_game:
        speed = handle_buttons(sc, speed)
>>>>>>> Stashed changes
        draw_info(sc, step_count, timespent)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                BUTTON_WIDTH, BUTTON_HEIGHT = 100, 30
                BUTTON_X = WIDTH - BUTTON_WIDTH - 20  # Right margin
                

                # Check button areas
                if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH:  # Check button area based on BUTTON_X position
                    # Run All Button (green)
                    if HEIGHT - 140 <= y <= HEIGHT - 140 + BUTTON_HEIGHT:
                        running, paused = True, False

                    # Next Step Button (yellow)
                    elif HEIGHT - 100 <= y <= HEIGHT - 100 + BUTTON_HEIGHT:
                        if current_step < len(steps):
                            g.update_maze_step(steps[current_step], sc)  # Update the maze step
                            pygame.display.flip()
                            clock.tick(100)
                            step_count += 1
                            current_step += 1
                            running, paused = False, True
                        else:
                            running = False

                    # Pause Button (red)
                    elif HEIGHT - 60 <= y <= HEIGHT - 60 + BUTTON_HEIGHT:
                        paused = True

<<<<<<< Updated upstream
=======
                    #Back to home (orange)
                    elif 15 <= y <= 15 + BUTTON_HEIGHT:
                        current_screen = "algorithm"
                        running = False
                        running_menu = True
                        running_game = False
            
                g.draw(sc)
>>>>>>> Stashed changes

                # Display info
                #draw_info(sc, step_count, timespent)
                draw_buttons(sc)
        if running and not paused:
            if current_step < len(steps):
                g.update_maze_step(steps[current_step], sc)
                pygame.display.flip()
                step_count += 1
                current_step += 1
                pygame.time.delay(int(500 / speed))
                
                if event.type == pygame.QUIT:  # Check for close button press
                    running = False
            else:
                running = False
<<<<<<< Updated upstream
=======
    
    return current_screen, running_menu
def main():
    pygame.init()
    pygame.event.get()
    pygame.display.set_caption("Ares's Adventure")     
    current_screen = "test_case"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for close button press
                running = False

        sc = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        sc.fill(pygame.color.Color(ASH_GRAY))

        if current_screen == "test_case":
            test_case, current_screen, running = testcase_selection_screen(sc)
        elif current_screen == "algorithm":
            algo, current_screen, running = algorithm_selection_screen(sc)
        elif current_screen == "game":
            current_screen, running = game_screen(test_case, algo)
            

    
>>>>>>> Stashed changes

if __name__ == '__main__':
    main()
