import pygame
import random
import sys
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Levels configuration
levels = [3, 4, 5, 6, 7]  # Grid sizes for levels 3x3, 4x4, etc.
current_level = 0

# Load images for each level
image_folder = 'images'
level_images = [
    [os.path.join(image_folder, f'level1_image{i}.jpg') for i in range(1, 6)],
    [os.path.join(image_folder, f'level2_image{i}.jpg') for i in range(1, 6)],
    [os.path.join(image_folder, f'level3_image{i}.jpg') for i in range(1, 6)],
    [os.path.join(image_folder, f'level4_image{i}.jpg') for i in range(1, 6)],
    [os.path.join(image_folder, f'level5_image{i}.jpg') for i in range(1, 6)],
]
loaded_images = [[pygame.image.load(img) for img in level] for level in level_images]

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle Game")

# Font
font = pygame.font.Font(None, 36)

# Draw the image selection menu
def draw_menu(images):
    screen.fill(WHITE)
    text = font.render("Choose an image to start the level:", True, BLACK)
    screen.blit(text, (20, 20))
    
    for i, img in enumerate(images):
        scaled_img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        rect = pygame.Rect(20 + i * (TILE_SIZE + 10), 70, TILE_SIZE, TILE_SIZE)
        screen.blit(scaled_img, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)  # Draw border

    pygame.display.flip()

# Handle menu events
def handle_menu_events(images):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(images)):
                    rect = pygame.Rect(20 + i * (TILE_SIZE + 10), 70, TILE_SIZE, TILE_SIZE)
                    if rect.collidepoint(x, y):
                        return images[i]

# Create a list of tile positions
def create_tiles(grid_size):
    tiles = [(x, y) for y in range(grid_size) for x in range(grid_size)]
    empty_pos = tiles[-1]
    tiles = tiles[:-1]
    random.shuffle(tiles)
    return tiles, empty_pos

# Create the grid
def create_grid(tiles, grid_size):
    grid = [tiles[i * grid_size:(i + 1) * grid_size] for i in range(grid_size - 1)]
    grid.append(tiles[(grid_size - 1) * grid_size:] + [None])
    return grid

# Get the position of the empty space
def get_empty_pos(grid):
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if tile is None:
                return (x, y)

# Draw the grid and tiles
def draw_grid(image, grid, grid_size):
    tile_size = TILE_SIZE * (3 / grid_size)  # Adjust tile size for different grid sizes
    for y in range(grid_size):
        for x in range(grid_size):
            tile = grid[y][x]
            if tile:
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                screen.blit(image, rect, (tile[0] * tile_size, tile[1] * tile_size, tile_size, tile_size))
            else:
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, BLACK, rect)

# Draw reference image
def draw_reference_image(image, grid_size):
    tile_size = TILE_SIZE * (3 / grid_size)
    scaled_reference = pygame.transform.scale(image, (int(tile_size), int(tile_size)))
    screen.blit(scaled_reference, (WIDTH - int(tile_size) - 20, 20))

# Move a tile
def move_tile(x, y, grid, empty_pos):
    empty_x, empty_y = empty_pos
    if (x == empty_x and abs(y - empty_y) == 1) or (y == empty_y and abs(x - empty_x) == 1):
        grid[empty_y][empty_x], grid[y][x] = grid[y][x], grid[empty_y][empty_x]
        empty_pos = (x, y)
    return empty_pos

# Check if the puzzle is solved
def is_solved(grid, grid_size):
    solution = [(x, y) for y in range(grid_size) for x in range(grid_size)]
    solution[-1] = None
    flat_grid = [tile for row in grid for tile in row]
    return flat_grid == solution

# Display confetti
def display_confetti():
    colors = [RED, GREEN, BLUE, YELLOW]
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        color = random.choice(colors)
        pygame.draw.circle(screen, color, (x, y), 5)
    pygame.display.flip()
    time.sleep(2)  # Show confetti for 2 seconds

# Main game loop
def game_loop(image, grid_size):
    tiles, empty_pos = create_tiles(grid_size)
    grid = create_grid(tiles, grid_size)
    empty_pos = get_empty_pos(grid)
    dragging = False
    drag_tile = None
    tile_size = int(TILE_SIZE * (3 / grid_size))  # Convert tile_size to integer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    x //= tile_size
                    y //= tile_size
                    if x < grid_size and y < grid_size and grid[y][x]:
                        dragging = True
                        drag_tile = (x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    x, y = event.pos
                    x //= tile_size
                    y //= tile_size
                    if x < grid_size and y < grid_size:
                        empty_pos = move_tile(drag_tile[0], drag_tile[1], grid, empty_pos)
                    drag_tile = None

        screen.fill(WHITE)
        draw_grid(image, grid, grid_size)
        draw_reference_image(image, grid_size)

        if dragging and drag_tile:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            tile_x, tile_y = drag_tile
            screen.blit(image, (mouse_x - tile_size // 2, mouse_y - tile_size // 2),
                        (tile_x * tile_size, tile_y * tile_size, tile_size, tile_size))

        pygame.display.flip()

        if is_solved(grid, grid_size):
            display_confetti()
            return

def show_level_images(level_images):
    screen.fill(WHITE)
    text = font.render("Level Images", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))
    
    for level_index, images in enumerate(level_images):
        for img_index, img in enumerate(images):
            scaled_img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            rect = pygame.Rect(20 + img_index * (TILE_SIZE + 10), 70 + level_index * (TILE_SIZE + 10), TILE_SIZE, TILE_SIZE)
            screen.blit(scaled_img, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
    
    pygame.display.flip()
    time.sleep(2)

if __name__ == "__main__":
    while current_level < len(levels):
        show_level_images(loaded_images)
        
        # Select image for the current level
        chosen_image = None
        while not chosen_image:
            draw_menu(loaded_images[current_level])
            chosen_image = handle_menu_events(loaded_images[current_level])
        
        print(f"Level {current_level + 1} selected image: {chosen_image}")
        grid_size = levels[current_level]
        scaled_image = pygame.transform.scale(chosen_image, (grid_size * TILE_SIZE, grid_size * TILE_SIZE))
        game_loop(scaled_image, grid_size)
        
        current_level += 1
        text = font.render(f"Level {current_level} Completed!", True, BLACK)
        screen.fill(WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(2)
    
    text = font.render("Congratulations! All levels completed!", True, BLACK)
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()
