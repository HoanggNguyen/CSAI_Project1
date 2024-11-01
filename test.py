import pygame
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Load ground image
GROUND_IMG_PATH = './Img/ground.png'  # Make sure to set the correct path
GROUND_IMG = pygame.image.load(GROUND_IMG_PATH)
cell_size = 40  # Size of each cell in the maze

# Resize ground image to cell size
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (cell_size, cell_size))

# Example maze data
maze_data = [
    "###########",
    "##        #",
    "#  $      #",
    "#     @ . #",
    "###########"
]

# Function to render the background grid of ground images
def render_background(screen, maze_width, maze_height):
    for y in range(0, maze_height * cell_size, cell_size):
        for x in range(0, maze_width * cell_size, cell_size):
            screen.blit(GROUND_IMG, (x, y))

# Function to render the maze elements on top of the background
def render_maze(screen, maze_data):
    for y, row in enumerate(maze_data):
        for x, cell in enumerate(row):
            cell_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if cell == "#":
                # Draw walls (you can replace this with wall image)
                pygame.draw.rect(screen, (50, 50, 50), cell_rect)
            elif cell == "$":
                # Draw stone (replace with stone image if needed)
                pygame.draw.circle(screen, (100, 50, 0), cell_rect.center, cell_size // 2)
            elif cell == "@":
                # Draw Ares (replace with Ares image if needed)
                pygame.draw.circle(screen, (0, 0, 255), cell_rect.center, cell_size // 2)
            elif cell == ".":
                # Draw destination (replace with destination image if needed)
                pygame.draw.circle(screen, (0, 255, 0), cell_rect.center, cell_size // 2)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen background

    # Render the background
    maze_width = len(maze_data[0])
    maze_height = len(maze_data)
    render_background(screen, maze_width, maze_height)  # Fill with ground images

    # Render the maze elements on top
    render_maze(screen, maze_data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update display

pygame.quit()
