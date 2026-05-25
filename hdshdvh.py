import pygame
import random
import sys

# 1. SETTINGS
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
TOTAL_CELLS = COLS * ROWS
TARGET_FOOD_COUNT = 20  # We want 20 cubes at all times

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold=True)

# Colors
BG_COLOR = (10, 10, 20)
SNAKE_COLOR = (0, 255, 150)
FOOD_COLOR = (255, 50, 80)

def create_path():
    """Generates the perfect 'Lawnmower' cycle."""
    path = []
    for x in range(COLS): path.append((x * CELL_SIZE, 0))
    for y in range(1, ROWS):
        if y % 2 == 1:
            for x in range(COLS - 1, 0, -1): path.append((x * CELL_SIZE, y * CELL_SIZE))
        else:
            for x in range(1, COLS): path.append((x * CELL_SIZE, y * CELL_SIZE))
    for y in range(ROWS - 1, 0, -1): path.append((0, y * CELL_SIZE))
    
    mapping = {path[i]: path[(i + 1) % len(path)] for i in range(len(path))}
    return mapping

# Initialize Game
NAVIGATOR = create_path()
snake_body = [(0, 0)]
snake_pos = (0, 0)
foods = [] # This will hold our 20 cubes
won = False

def refill_foods():
    """Ensures there are exactly 20 foods on the screen if space allows."""
    # 1. Find all empty spots
    all_spots = set((x * CELL_SIZE, y * CELL_SIZE) for x in range(COLS) for y in range(ROWS))
    occupied = set(snake_body) | set(foods)
    empty_spots = list(all_spots - occupied)
    
    # 2. Add food until we hit 20 or run out of room
    while len(foods) < TARGET_FOOD_COUNT and empty_spots:
        new_f = random.choice(empty_spots)
        foods.append(new_f)
        empty_spots.remove(new_f)

# Initial spawn of 20 cubes
refill_foods()

# 2. MAIN LOOP
while True:
    screen.fill(BG_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not won:
        # Move along the pre-set path
        snake_pos = NAVIGATOR[snake_pos]
        snake_body.insert(0, snake_pos)
        
        # Check if we hit ANY of the 20 foods
        if snake_pos in foods:
            foods.remove(snake_pos)
            refill_foods() # Immediately try to put a new one back
            # Snake grows because we don't pop()
        else:
            if len(snake_body) > 1:
                snake_body.pop()
        
        if len(snake_body) >= TOTAL_CELLS:
            won = True

    # --- DRAW ---
    for f in foods:
        pygame.draw.rect(screen, FOOD_COLOR, (f[0], f[1], CELL_SIZE-2, CELL_SIZE-2))
    
    for i, seg in enumerate(snake_body):
        # Head is bright white, body is green
        color = (255, 255, 255) if i == 0 else SNAKE_COLOR
        pygame.draw.rect(screen, color, (seg[0], seg[1], CELL_SIZE-1, CELL_SIZE-1))

    # UI
    fill_text = font.render(f"SNAKE FILL: {len(snake_body)} / {TOTAL_CELLS}", True, (255, 255, 255))
    screen.blit(fill_text, (10, 10))
    
    if won:
        win_text = font.render("PERFECT 600 REACHED!", True, (0, 255, 0))
        screen.blit(win_text, (WIDTH//2-100, HEIGHT//2))

    pygame.display.flip()
    clock.tick(1)