import pygame
import random
import time
from persistence import load_settings, save_settings, add_score
pygame.font.init()
WIDTH = 400
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
YELLOW = (255, 210, 50)
BLUE = (70, 130, 255)
GREEN = (70, 200, 90)
GRAY = (120, 120, 120)
PURPLE = (170, 90, 255)
ORANGE = (255, 150, 50)

LANES = [70, 160, 250, 330]


font_small = pygame.font.SysFont("Verdana", 18)


def safe_x(player_rect):
    x = random.choice(LANES)

    while abs(x - player_rect.centerx) < 70:
        x = random.choice(LANES)

    return x


class Player(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()

        self.original = pygame.image.load("materials/Player 2.png")
        self.original = pygame.transform.scale(self.original, (45, 75))

        self.image = self.original.copy()
        self.apply_color(settings["car_color"])

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def apply_color(self, color):
        if color == "red":
            self.image.fill((255, 80, 80), special_flags=pygame.BLEND_RGB_ADD)
        elif color == "green":
            self.image.fill((80, 255, 100), special_flags=pygame.BLEND_RGB_ADD)
        else:
            self.image.fill((80, 150, 255), special_flags=pygame.BLEND_RGB_ADD)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-6, 0)

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(6, 0)


class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, player_rect, speed):
        super().__init__()

        self.image = pygame.image.load("materials/Enemy 2.png")
        self.image = pygame.transform.scale(self.image, (45, 75))

        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(player_rect), -80)

        self.speed = speed

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        self.value = random.choice([1, 2, 3])
        size = 20 + self.value * 7

        self.image = pygame.image.load("materials/coin.png")
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(player_rect), -40)

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player_rect, kind):
        super().__init__()

        self.kind = kind

        if kind == "oil":
            self.image = pygame.Surface((55, 30))
            self.image.fill(BLACK)

        elif kind == "barrier":
            self.image = pygame.Surface((70, 25))
            self.image.fill(ORANGE)

        else:
            self.image = pygame.Surface((50, 35))
            self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(player_rect), -50)

        self.direction = random.choice([-2, 2])

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.kind == "barrier":
            self.rect.move_ip(self.direction, 0)

            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()

        self.kind = random.choice(["nitro", "shield", "repair"])

        self.image = pygame.Surface((35, 35))

        if self.kind == "nitro":
            self.image.fill(PURPLE)
        elif self.kind == "shield":
            self.image.fill(BLUE)
        else:
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(player_rect), -40)

        self.spawn_time = time.time()

    def move(self, speed):
        self.rect.move_ip(0, speed)

        if self.rect.top > HEIGHT:
            self.kill()

        if time.time() - self.spawn_time > 6:
            self.kill()


def draw_info(screen, score, coins, distance, finish, active_power, power_time):
    texts = [
        f"Score: {score}",
        f"Coins: {coins}",
        f"Distance: {distance}/{finish}",
        f"Left: {max(0, finish - distance)}"
    ]

    y = 10
    for text in texts:
        img = font_small.render(text, True, BLACK)
        screen.blit(img, (10, y))
        y += 25

    if active_power:
        power_text = f"Power: {active_power}"

        if active_power == "nitro":
            power_text += f" {max(0, int(power_time))}s"

        img = font_small.render(power_text, True, RED)
        screen.blit(img, (230, 10))


def settings_screen(screen):
    settings = load_settings()

    sound_button = pygame.Rect(90, 150, 220, 45)
    color_button = pygame.Rect(90, 230, 220, 45)
    difficulty_button = pygame.Rect(90, 310, 220, 45)
    back_button = pygame.Rect(90, 470, 220, 45)

    colors = ["blue", "red", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = pygame.font.SysFont("Verdana", 30).render("Settings", True, BLACK)
        screen.blit(title, (120, 60))

        buttons = [
            (sound_button, f"Sound: {settings['sound']}"),
            (color_button, f"Car color: {settings['car_color']}"),
            (difficulty_button, f"Difficulty: {settings['difficulty']}"),
            (back_button, "Back")
        ]

        for rect, text in buttons:
            pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
            img = font_small.render(text, True, BLACK)
            screen.blit(img, (rect.x + 20, rect.y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                if color_button.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                if difficulty_button.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    save_settings(settings)

                if back_button.collidepoint(event.pos):
                    return "menu"


def start_game(screen, username):
    settings = load_settings()

    if settings["sound"]:
        try:
            pygame.mixer.music.load("materials/background.wav")
            pygame.mixer.music.play(-1)
        except:
            pass

    try:
        coin_sound = pygame.mixer.Sound("materials/coin.mp3")
        crash_sound = pygame.mixer.Sound("materials/crash.wav")
    except:
        coin_sound = None
        crash_sound = None

    background = pygame.image.load("materials/AnimatedStreet.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    player = Player(settings)

    traffic = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powers = pygame.sprite.Group()

    clock = pygame.time.Clock()

    coins = 0
    score = 0
    distance = 0
    finish_distance = 2000

    active_power = None
    shield = False
    nitro_end_time = 0

    if settings["difficulty"] == "easy":
        road_speed = 4
        traffic_timer = 90
        obstacle_timer = 120

    elif settings["difficulty"] == "hard":
        road_speed = 7
        traffic_timer = 45
        obstacle_timer = 70

    else:
        road_speed = 5
        traffic_timer = 65
        obstacle_timer = 95

    frame = 0
    bg_y = 0

    while True:
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        if active_power == "nitro":
            if time.time() > nitro_end_time:
                active_power = None
            current_speed = road_speed + 4
        else:
            current_speed = road_speed

        player.move()

        bg_y += current_speed
        if bg_y >= HEIGHT:
            bg_y = 0

        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - HEIGHT))

        distance += current_speed // 2

        if distance > 500:
            traffic_timer = max(30, traffic_timer - 1)

        if distance > 1000:
            obstacle_timer = max(45, obstacle_timer - 1)

        if frame % traffic_timer == 0:
            traffic.add(TrafficCar(player.rect, current_speed + 2))

        if frame % 80 == 0:
            coins_group.add(Coin(player.rect))

        if frame % obstacle_timer == 0:
            kind = random.choice(["oil", "barrier", "pothole"])
            obstacles.add(Obstacle(player.rect, kind))

        if frame % 350 == 0:
            powers.add(PowerUp(player.rect))

        for car in traffic:
            car.move()
            screen.blit(car.image, car.rect)

        for coin in coins_group:
            coin.move(current_speed)
            screen.blit(coin.image, coin.rect)

        for obstacle in obstacles:
            obstacle.move(current_speed)
            screen.blit(obstacle.image, obstacle.rect)

        for power in powers:
            power.move(current_speed)
            screen.blit(power.image, power.rect)

        screen.blit(player.image, player.rect)

        collected_coin = pygame.sprite.spritecollideany(player, coins_group)
        if collected_coin:
            coins += collected_coin.value
            score += collected_coin.value * 10

            if settings["sound"] and coin_sound:
                coin_sound.play()

            collected_coin.kill()

        collected_power = pygame.sprite.spritecollideany(player, powers)
        if collected_power and active_power is None:
            active_power = collected_power.kind

            if active_power == "nitro":
                nitro_end_time = time.time() + 4

            elif active_power == "shield":
                shield = True

            elif active_power == "repair":
                if len(obstacles) > 0:
                    list(obstacles)[0].kill()
                score += 20
                active_power = None

            collected_power.kill()

        hit_traffic = pygame.sprite.spritecollideany(player, traffic)
        hit_obstacle = pygame.sprite.spritecollideany(player, obstacles)

        if hit_obstacle:
            if hit_obstacle.kind == "oil":
                player.rect.move_ip(random.choice([-40, 40]), 0)
                hit_obstacle.kill()
            else:
                if shield:
                    shield = False
                    active_power = None
                    hit_obstacle.kill()
                else:
                    if settings["sound"] and crash_sound:
                        crash_sound.play()

                    final_score = score + coins * 5 + distance // 10
                    add_score(username, final_score, distance)
                    return ("game_over", final_score, distance, coins)

        if hit_traffic:
            if shield:
                shield = False
                active_power = None
                hit_traffic.kill()
            else:
                if settings["sound"] and crash_sound:
                    crash_sound.play()

                final_score = score + coins * 5 + distance // 10
                add_score(username, final_score, distance)
                return ("game_over", final_score, distance, coins)

        if distance >= finish_distance:
            final_score = score + coins * 5 + distance // 10 + 200
            add_score(username, final_score, distance)
            return ("game_over", final_score, distance, coins)

        power_time = 0
        if active_power == "nitro":
            power_time = nitro_end_time - time.time()

        draw_info(screen, score, coins, distance, finish_distance, active_power, power_time)

        pygame.display.update()
        clock.tick(FPS)