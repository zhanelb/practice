import pygame
import random
import sys
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("snake.mp3")
pygame.mixer.music.play(-1)
eat_sound = pygame.mixer.Sound("snakebg.mp3")
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game ")
clock = pygame.time.Clock()

FPS = 10

BLACK = (0, 0, 0)
PINK = (240, 17, 117)
RED = (255, 0, 0)
GRAY = (40, 40, 40)
WHITE = (255, 255, 255)
font = pygame.font.SysFont("Arial", 24)
#snake draw
class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)
    #changing his position 
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()
    def grow(self):
        # adding new 
        self.body.append(self.body[-1])
    def change_direction(self, new_dir):
        #preventing a collision with himelf
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    def check_collision(self):
        x, y = self.body[0]
        # inner window 
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return True
        # self
        if self.body[0] in self.body[1:]:
            return True

        return False
    def eat(self, food_pos):
        return self.body[0] == food_pos
    def draw(self):
        for i, part in enumerate(self.body):
            color = PINK if i == 0 else (245, 86, 157)
            pygame.draw.rect(screen, color, (*part, CELL_SIZE, CELL_SIZE))

def random_food(snake_body):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        # food not inside the snake 
        if (x, y) not in snake_body:
            return (x, y)
snake = Snake()
food = random_food(snake.body)
food_weight = random.choice([1, 2, 3])  #random 'size'
food_timer = 0                          # how long we have it
food_lifetime = 100                    
score = 0
level = 1
foods_needed = 3 #  levels limit 

def draw_food():
    if food_weight == 1:
        color = RED
    elif food_weight == 2:
        color = (255, 165, 0)  # оранжевый
    else:
        color = (255, 255, 0)  # жёлтый

    pygame.draw.rect(screen, color, (*food, CELL_SIZE, CELL_SIZE))

def draw_stats():
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

running = True
while running:
    screen.fill(BLACK)
    food_timer += 1
    # если еда "протухла" — создаём новую
    if food_timer > food_lifetime:
        food = random_food(snake.body)
        food_weight = random.choice([1, 2, 3])
        food_timer = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((CELL_SIZE, 0))
    # move snake
    snake.move()
    # collision
    if snake.check_collision():
        print("Game Over")
        pygame.quit()
        sys.exit()

    # eat food
    # food disappears after time
    if snake.eat(food):
        eat_sound.play()
        score += food_weight   # weigth of food
        foods_needed -= 1
        food = random_food(snake.body)
        food_weight = random.choice([1, 2, 3])  # new food with new weight
        food_timer = 0  # сброс таймера

        snake.grow()
        if foods_needed == 0:
            level += 1
            foods_needed = 3
            FPS += 2  # speed up

    # draw
    snake.draw()
    draw_food()
    draw_stats()

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
