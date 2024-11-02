import pygame
import os
# Kích thước và khoảng cách giữa các ô trong mê cung
BOUND = 15
A = 50  # Kích thước của mỗi ô
A1 = 0  # Khoảng cách giữa các ô

# Khởi tạo các biến với giá trị mặc định
# Hàm cập nhật các giá trị COLS và ROWS
def set_dimensions(cols, rows):
    global COLS, ROWS, WIDTH, HEIGHT
    COLS = cols
    ROWS = rows
    WIDTH =  2 * BOUND + (COLS - 1) * A1 + A*(COLS) + 150
    HEIGHT = 2 * BOUND + (ROWS - 1) * A1 + A*ROWS +100
    return WIDTH, HEIGHT


# Hằng số để điều chỉnh kích thước của các ảnh
wall_scale = A/25*0.8
switch_scale = A/25*0.9  # Thay đổi giá trị này để điều chỉnh kích thước ảnh
stone_scale = A/25*1.25
ares_scale = A/25*0.9
menu_button_scale = 0.5

# Load and scale background image
background_image1 = pygame.image.load("Img/Menu/BG.png")
background_image2 = pygame.image.load("Img/Menu/BG2.jpg")
background_image = pygame.transform.scale(background_image1, (480, 720))
# Load images outside the functions
button_img = pygame.image.load('./Img/Menu/button2.png')
light_button_image2 = pygame.image.load('./Img/Menu/light-button2.png')

# Define button vertical positions
button_positions = {
    "Start New Adventure": 300,
    "Review Journey": 380,
    "How to play": 460,
    "Quit Game": 540
}



# Load images from Img folder
ARES_IMG = pygame.image.load(os.path.join('Img', 'ares.png'))
STONE_IMG = pygame.image.load(os.path.join('Img', 'stone.png'))
SWITCH_IMG = pygame.image.load(os.path.join('Img', 'switch.png'))
WALL_IMG = pygame.image.load(os.path.join('Img', 'wall.png'))
FLOOR_IMG = pygame.image.load(os.path.join('Img', 'floor.png'))

# Thay đổi kích thước hình ảnh
ARES_IMG = pygame.transform.scale(ARES_IMG, (int(ARES_IMG.get_width() * ares_scale), int(ARES_IMG.get_height() * ares_scale)))
STONE_IMG = pygame.transform.scale(STONE_IMG, (int(STONE_IMG.get_width() * stone_scale), int(STONE_IMG.get_height() * stone_scale)))
SWITCH_IMG = pygame.transform.scale(SWITCH_IMG, (int(SWITCH_IMG.get_width() * switch_scale), int(SWITCH_IMG.get_height() * switch_scale)))
WALL_IMG = pygame.transform.scale(WALL_IMG, (int(WALL_IMG.get_width() * wall_scale), int(WALL_IMG.get_height() * wall_scale)))
FLOOR_IMG = pygame.transform.scale(FLOOR_IMG, (int(FLOOR_IMG.get_width() * wall_scale), int(FLOOR_IMG.get_height() * wall_scale)))


font_path = "./Fonts/Quantico-Bold.ttf"

GREY = (100, 100, 100)      # Không gian trống (free space)
WHITE = (255, 255, 255)     # Màu nền cho các ô
YELLOW = (200, 200, 0)      # Node hiện tại (đang khám phá)
RED = (200, 0, 0)           # Node đã được khám phá
BLUE = (30, 144, 255)       # Đá
PURPLE = (138, 43, 226)     # Switch (mục tiêu)
ORANGE = (255, 165, 0)      # Điểm bắt đầu (Ares)
GREEN = (54, 179, 72)       # Đá nằm trên switch
BLACK = (0, 0, 0)           # Tường
LIGHT_GRAY = (200, 200, 200) # Màu lưới mờ để phân biệt các ô
NAVY = (0,0,128)

GOLD = (255, 215, 0)         # Màu vàng kim, có thể dùng cho điểm thưởng
PINK = (255, 192, 203)       # Màu hồng, có thể dùng cho các yếu tố nữ tính hoặc vui tươi

# Màu sắc xám
WARM_GRAY = (220, 220, 200)  # Beige pha xám nhẹ, phù hợp cho nền trung tính và hài hòa
STONE = (210, 205, 190)       # Tông màu đá tự nhiên, tối hơn Beige và có chút xám
