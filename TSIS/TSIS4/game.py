import pygame
import random
import sys
import json
import os
from db import save_result, get_leaderboard, get_personal_best

WIDTH, HEIGHT = 600, 600
CELL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 150, 255)
PURPLE = (180, 0, 255)

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)
BIG_FONT = pygame.font.SysFont("Arial", 40)


class SnakeGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.username = ""
        self.state = "menu"
        self.load_settings()

        try:
            pygame.mixer.init()
            if self.settings["sound"]:
                pygame.mixer.music.load("snake.mp3")
                pygame.mixer.music.play(-1)
                self.eat_sound = pygame.mixer.Sound("snakebg.mp3")
            else:
                self.eat_sound = None
        except:
            self.eat_sound = None

    def load_settings(self):
        if not os.path.exists("settings.json"):
            self.settings = {
                "snake_color": [240, 17, 117],
                "grid": True,
                "sound": True
            }
            self.save_settings()
        else:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def draw_text(self, text, x, y, color=WHITE, big=False):
        font = BIG_FONT if big else FONT
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def button(self, text, x, y, w, h):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        color = (80, 80, 80)
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            color = (120, 120, 120)

        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=10)
        label = FONT.render(text, True, WHITE)
        self.screen.blit(label, (x + 20, y + 12))

        return x < mouse[0] < x + w and y < mouse[1] < y + h and click[0]

    def username_screen(self):
        active = True
        while active:
            self.screen.fill(BLACK)
            self.draw_text("Enter username:", 170, 180, WHITE, True)
            pygame.draw.rect(self.screen, WHITE, (150, 260, 300, 45), 2)
            self.draw_text(self.username, 165, 270)

            self.draw_text("Press ENTER to continue", 155, 340)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.username.strip():
                        self.personal_best = get_personal_best(self.username)
                        self.new_game()
                        self.state = "playing"
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if len(self.username) < 15:
                            self.username += event.unicode

            pygame.display.update()
            self.clock.tick(30)

    def menu(self):
        while self.state == "menu":
            self.screen.fill(BLACK)
            self.draw_text("SNAKE GAME", 180, 100, WHITE, True)

            if self.button("Play", 210, 200, 180, 50):
                self.username_screen()

            if self.button("Leaderboard", 210, 270, 180, 50):
                self.state = "leaderboard"

            if self.button("Settings", 210, 340, 180, 50):
                self.state = "settings"

            if self.button("Quit", 210, 410, 180, 50):
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def new_game(self):
        self.snake = [(300, 300), (280, 300), (260, 300)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.speed = 8
        self.foods_needed = 3

        self.obstacles = []
        self.food = self.random_empty_cell()
        self.food_weight = random.choice([1, 2, 3])
        self.food_spawn_time = pygame.time.get_ticks()

        self.poison = self.random_empty_cell()
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0

        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.saved = False

    def random_empty_cell(self):
        while True:
            x = random.randint(0, (WIDTH - CELL) // CELL) * CELL
            y = random.randint(0, (HEIGHT - CELL) // CELL) * CELL
            pos = (x, y)

            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def draw_grid(self):
        if self.settings["grid"]:
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw_snake(self):
        snake_color = tuple(self.settings["snake_color"])

        for i, part in enumerate(self.snake):
            color = snake_color if i == 0 else (245, 86, 157)
            pygame.draw.rect(self.screen, color, (*part, CELL, CELL))

    def draw_food(self):
        if self.food_weight == 1:
            color = RED
        elif self.food_weight == 2:
            color = ORANGE
        else:
            color = YELLOW

        pygame.draw.rect(self.screen, color, (*self.food, CELL, CELL))

    def draw_poison(self):
        pygame.draw.rect(self.screen, DARK_RED, (*self.poison, CELL, CELL))

    def draw_powerup(self):
        if self.powerup:
            if self.powerup_type == "speed":
                color = BLUE
            elif self.powerup_type == "slow":
                color = GREEN
            else:
                color = PURPLE

            pygame.draw.rect(self.screen, color, (*self.powerup, CELL, CELL))

    def draw_obstacles(self):
        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (*block, CELL, CELL))

    def draw_stats(self):
        text = f"Score: {self.score}  Level: {self.level}  Best: {self.personal_best}"
        self.draw_text(text, 10, 10)

        if self.shield:
            self.draw_text("Shield ON", 10, 40, PURPLE)

    def spawn_powerup(self):
        if self.powerup is None and random.randint(1, 120) == 1:
            self.powerup = self.random_empty_cell()
            self.powerup_type = random.choice(["speed", "slow", "shield"])
            self.powerup_spawn_time = pygame.time.get_ticks()

    def check_powerup_timer(self):
        now = pygame.time.get_ticks()

        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None
            self.powerup_type = None

        if self.active_power and now > self.power_end_time:
            self.active_power = None
            self.speed = 8 + (self.level - 1) * 2

    def make_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = self.level + 2

        for i in range(count):
            block = self.random_empty_cell()

            head = self.snake[0]
            distance = abs(block[0] - head[0]) + abs(block[1] - head[1])

            if distance > CELL * 3:
                self.obstacles.append(block)

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.snake.insert(0, new_head)
        self.snake.pop()

    def grow(self):
        self.snake.append(self.snake[-1])

    def collision(self):
        head = self.snake[0]
        x, y = head

        hit = False

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            hit = True

        if head in self.snake[1:]:
            hit = True

        if head in self.obstacles:
            hit = True

        if hit:
            if self.shield:
                self.shield = False
                self.snake[0] = (300, 300)
                return False
            return True

        return False

    def eat_food(self):
        if self.snake[0] == self.food:
            if self.eat_sound:
                self.eat_sound.play()

            self.score += self.food_weight
            self.foods_needed -= 1
            self.grow()

            self.food = self.random_empty_cell()
            self.food_weight = random.choice([1, 2, 3])
            self.food_spawn_time = pygame.time.get_ticks()

            if self.foods_needed == 0:
                self.level += 1
                self.foods_needed = 3
                self.speed += 2
                self.make_obstacles()

    def eat_poison(self):
        if self.snake[0] == self.poison:
            for i in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            if len(self.snake) <= 1:
                self.state = "gameover"

            self.poison = self.random_empty_cell()

    def eat_powerup(self):
        if self.powerup and self.snake[0] == self.powerup:
            now = pygame.time.get_ticks()

            if self.powerup_type == "speed":
                self.active_power = "speed"
                self.speed += 5
                self.power_end_time = now + 5000

            elif self.powerup_type == "slow":
                self.active_power = "slow"
                self.speed = max(4, self.speed - 4)
                self.power_end_time = now + 5000

            elif self.powerup_type == "shield":
                self.shield = True

            self.powerup = None
            self.powerup_type = None

    def check_food_timer(self):
        now = pygame.time.get_ticks()

        if now - self.food_spawn_time > 7000:
            self.food = self.random_empty_cell()
            self.food_weight = random.choice([1, 2, 3])
            self.food_spawn_time = now

    def playing(self):
        while self.state == "playing":
            self.screen.fill(BLACK)
            self.draw_grid()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != (0, CELL):
                        self.next_direction = (0, -CELL)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -CELL):
                        self.next_direction = (0, CELL)
                    elif event.key == pygame.K_LEFT and self.direction != (CELL, 0):
                        self.next_direction = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-CELL, 0):
                        self.next_direction = (CELL, 0)

            self.move_snake()

            if self.collision():
                self.state = "gameover"

            self.eat_food()
            self.eat_poison()
            self.eat_powerup()
            self.check_food_timer()
            self.spawn_powerup()
            self.check_powerup_timer()

            self.draw_food()
            self.draw_poison()
            self.draw_powerup()
            self.draw_obstacles()
            self.draw_snake()
            self.draw_stats()

            pygame.display.update()
            self.clock.tick(self.speed)

    def game_over(self):
        if not self.saved:
            save_result(self.username, self.score, self.level)
            self.personal_best = max(self.personal_best, self.score)
            self.saved = True

        while self.state == "gameover":
            self.screen.fill(BLACK)

            self.draw_text("GAME OVER", 180, 120, RED, True)
            self.draw_text(f"Score: {self.score}", 220, 200)
            self.draw_text(f"Level: {self.level}", 220, 240)
            self.draw_text(f"Personal best: {self.personal_best}", 180, 280)

            if self.button("Retry", 210, 350, 180, 50):
                self.new_game()
                self.state = "playing"

            if self.button("Main Menu", 210, 420, 180, 50):
                self.state = "menu"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def leaderboard(self):
        data = get_leaderboard()

        while self.state == "leaderboard":
            self.screen.fill(BLACK)
            self.draw_text("LEADERBOARD", 170, 40, WHITE, True)

            y = 110
            self.draw_text("Rank  Name        Score  Level  Date", 60, y)
            y += 40

            for i, row in enumerate(data):
                username, score, level, played_at = row
                date = played_at.strftime("%d.%m.%Y")
                line = f"{i+1}.    {username[:8]:8}   {score:4}   {level:3}   {date}"
                self.draw_text(line, 60, y)
                y += 30

            if self.button("Back", 210, 520, 180, 50):
                self.state = "menu"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def settings_screen(self):
        colors = [
            [240, 17, 117],
            [0, 200, 0],
            [0, 150, 255],
            [255, 255, 0]
        ]

        color_index = 0

        while self.state == "settings":
            self.screen.fill(BLACK)
            self.draw_text("SETTINGS", 210, 80, WHITE, True)

            self.draw_text(f"Grid: {self.settings['grid']}", 180, 180)
            if self.button("Toggle Grid", 180, 220, 220, 45):
                self.settings["grid"] = not self.settings["grid"]
                pygame.time.delay(200)

            self.draw_text(f"Sound: {self.settings['sound']}", 180, 290)
            if self.button("Toggle Sound", 180, 330, 220, 45):
                self.settings["sound"] = not self.settings["sound"]
                pygame.time.delay(200)

            if self.button("Change Snake Color", 150, 400, 300, 45):
                color_index = (color_index + 1) % len(colors)
                self.settings["snake_color"] = colors[color_index]
                pygame.time.delay(200)

            if self.button("Save & Back", 190, 500, 220, 50):
                self.save_settings()
                self.state = "menu"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(30)

    def run(self):
        while True:
            if self.state == "menu":
                self.menu()
            elif self.state == "playing":
                self.playing()
            elif self.state == "gameover":
                self.game_over()
            elif self.state == "leaderboard":
                self.leaderboard()
            elif self.state == "settings":
                self.settings_screen()