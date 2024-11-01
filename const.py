# const.py

# Kích thước và khoảng cách giữa các ô trong mê cung
BOUND = 15
A = 40  # Kích thước của mỗi ô
A1 = 1  # Khoảng cách giữa các ô


# Khởi tạo các biến với giá trị mặc định
# Hàm cập nhật các giá trị COLS và ROWS
def set_dimensions(cols, rows):
    global COLS, ROWS, WIDTH, HEIGHT
    COLS = cols
    ROWS = rows
    WIDTH =  2 * BOUND + (COLS - 1) * A1 + A*(COLS) + 150
    HEIGHT = 2 * BOUND + (ROWS - 1) * A1 + A*ROWS +100
    return WIDTH, HEIGHT


# Màu sắc
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
# Màu sắc bổ sung
DARK_GRAY = (50, 50, 50)    # Màu xám tối, có thể dùng cho nền hoặc viền
CYAN = (0, 255, 255)         # Màu xanh lam sáng, có thể dùng cho các điểm nhấn
MAGENTA = (255, 0, 255)      # Màu tím sáng, có thể dùng cho các yếu tố tương tác
LIGHT_BLUE = (173, 216, 230) # Màu xanh nhạt, có thể dùng cho nền
BROWN = (165, 42, 42)        # Màu nâu, có thể dùng cho đất hoặc gỗ
GOLD = (255, 215, 0)         # Màu vàng kim, có thể dùng cho điểm thưởng
PINK = (255, 192, 203)       # Màu hồng, có thể dùng cho các yếu tố nữ tính hoặc vui tươi

# Màu sắc xám
LIGHT_GRAY = (200, 200, 200)  # Màu xám sáng, thường dùng cho nền hoặc các phần tử không nổi bật
GREY = (100, 100, 100)        # Màu xám trung bình, có thể dùng cho không gian trống
DARK_GRAY = (50, 50, 50)      # Màu xám tối, phù hợp cho nền tối hoặc viền
CHARCOAL = (40, 40, 40)       # Màu xám than, tối hơn xám tối, thích hợp cho các yếu tố thiết kế mạnh mẽ
SILVER = (192, 192, 192)      # Màu bạc, thường dùng cho điểm nhấn hoặc các yếu tố sang trọng
DOVE_GRAY = (169, 169, 169)   # Màu xám bồ câu, một tông màu xám nhẹ hơn, thích hợp cho nền
ASH_GRAY = (178, 190, 181)    # Màu xám tro, có chút tông xanh nhẹ, dùng cho các yếu tố tự nhiên