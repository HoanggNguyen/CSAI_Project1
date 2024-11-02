import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 480, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ares's Adventure")

# Scaling factor for buttons
menu_button_scale = 0.5  # Adjust this value to scale the buttons


# Load and scale background image
background_image = pygame.image.load("Img/Menu/BG.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load button images
button_paths = {
    "Start New Adventure": "Img/Menu/StartNewAdventure.png",
    "Review Journey": "Img/Menu/ReviewJourney.png",
    "How to play": "Img/Menu/HowToPlay.png",
    "Quit Game": "Img/Menu/QuitGame.png"
}

# Load and scale button images based on menu_button_scale
buttons = {}
for text, path in button_paths.items():
    button_image = pygame.image.load(path)
    button_width = int(button_image.get_width() * menu_button_scale)
    button_height = int(button_image.get_height() * menu_button_scale)
    buttons[text] = pygame.transform.scale(button_image, (button_width, button_height))

# Define button vertical positions
button_positions = {
    "Start New Adventure": 300,
    "Review Journey": 380,
    "How to play": 460,
    "Quit Game": 540
}

# Load Quantico font
font_path = "./Fonts/Quantico-Bold.ttf"

title_font = pygame.font.Font(font_path, 74)

def draw_menu(screen):
    """Function to draw the main menu on the given screen."""
    # Draw the scaled background image
    screen.blit(background_image, (0, 0))

    # Draw title text with Quantico font, split into two lines, and center-aligned
    title_text1 = title_font.render("Ares's", True, (44, 61, 88))
    title_text2 = title_font.render("Adventure", True, (44, 61, 88))
    title_text1_rect = title_text1.get_rect(center=(screen_width // 2, 100))
    title_text2_rect = title_text2.get_rect(center=(screen_width // 2, 180))
    screen.blit(title_text1, title_text1_rect)
    screen.blit(title_text2, title_text2_rect)

    # Draw centered buttons
    for text, y_pos in button_positions.items():
        button_image = buttons[text]
        button_rect = button_image.get_rect(center=(screen_width // 2, y_pos))
        screen.blit(button_image, button_rect)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                mouse_pos = event.pos
                for text, y_pos in button_positions.items():
                    button_rect = buttons[text].get_rect(center=(screen_width // 2, y_pos))
                    if button_rect.collidepoint(mouse_pos):
                        print(f"{text} button clicked")
                        if text == "Quit Game":
                            pygame.quit()
                            sys.exit()
                        # Add specific functionality for each button here

        # Draw the menu
        draw_menu(screen)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
