from display import *
from algos import *
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(100, 50)
    pygame.init()  # Set up the screen
    pygame.font.init()
    pygame.event.get()

    screen_width, screen_height = 480, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ares's Adventure - Group 10")

    current_screen = "menu"
    running = True
    
    while running:
        if current_screen == "menu":
            current_screen, state = draw_menu(screen, current_screen)
        elif current_screen == "howto":
            current_screen, state = show_how_to_play(screen, button_img, light_button_image2)  # Ensure show_how_to_play returns correctly
        elif current_screen == "test_case":
            test_case, current_screen, running = testcase_selection_screen(screen, state, background_image, button_img, light_button_image2)
        elif current_screen == "test_case2":
            test_case, current_screen, running = testcase_selection_screen2(screen, state, background_image, button_img, light_button_image2)
        elif current_screen == "algorithm":
            algo, current_screen, running = algorithm_selection_screen(screen, state, background_image, button_img, light_button_image2)
        elif current_screen == "game":
            current_screen, running = game_screen(screen, state, test_case, algo)
        elif current_screen == "quit":
            running = False

        pygame.display.flip()

    pygame.quit()

    pygame.quit()
if __name__ == '__main__':
    main()