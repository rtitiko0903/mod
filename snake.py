import pygame
import random
import sys

# 1. Setup Colors and Settings
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)  # Classic solid green
YELLOW = (255, 255, 102) # Food color
WHITE  = (255, 255, 255)
RED    = (213, 50, 80)

WIDTH, HEIGHT = 600, 400
SNAKE_BLOCK = 20  # Bigger blocks make it easier to see
SNAKE_SPEED = 15  # Normal playable speed

pygame.init()
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Classic Green Snake')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def gameLoop():
    game_over = False
    game_close = False

    # Starting coordinates
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    # Random food position aligned to the grid
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0

    while not game_over:

        while game_close:
            dis.fill(BLACK)
            message("You Lost! Press C to Play Again or Q to Quit", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Boundary Check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(dis, YELLOW, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
        
        # Snake movement logic
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self-collision check
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw Snake
        for segment in snake_List:
            pygame.draw.rect(dis, GREEN, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

        pygame.display.update()

        # Eating Logic
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    gameLoop()