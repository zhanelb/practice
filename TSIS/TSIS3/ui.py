import pygame
from persistence import load_leaderboard

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK = (80, 80, 80)
BLUE = (80, 150, 255)


font = None
small_font = None


def init_fonts():
    global font, small_font
    font = pygame.font.SysFont("Verdana", 32)
    small_font = pygame.font.SysFont("Verdana", 20)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK, self.rect, 2, border_radius=10)

        text_img = small_font.render(self.text, True, BLACK)
        text_rect = text_img.get_rect(center=self.rect.center)
        screen.blit(text_img, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def draw_text(screen, text, x, y, size="small", color=BLACK):
    if size == "big":
        img = font.render(text, True, color)
    else:
        img = small_font.render(text, True, color)

    screen.blit(img, (x, y))


def main_menu(screen):
    buttons = {
        "play": Button(120, 180, 160, 45, "Play"),
        "leaderboard": Button(120, 240, 160, 45, "Leaderboard"),
        "settings": Button(120, 300, 160, 45, "Settings"),
        "quit": Button(120, 360, 160, 45, "Quit")
    }

    while True:
        screen.fill(WHITE)
        draw_text(screen, "Racer Game", 90, 90, "big")

        for button in buttons.values():
            button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, button in buttons.items():
                    if button.is_clicked(event.pos):
                        return name


def username_screen(screen):
    name = ""
    active = True

    while active:
        screen.fill(WHITE)
        draw_text(screen, "Enter your name:", 90, 180, "big")
        draw_text(screen, name, 150, 260, "big", BLUE)
        draw_text(screen, "Press ENTER to start", 90, 350)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 10:
                        name += event.unicode


def leaderboard_screen(screen):
    back = Button(120, 520, 160, 45, "Back")
    data = load_leaderboard()

    while True:
        screen.fill(WHITE)
        draw_text(screen, "Leaderboard", 85, 40, "big")

        y = 110
        for i, item in enumerate(data):
            text = f"{i + 1}. {item['name']}  Score: {item['score']}  Dist: {item['distance']}"
            draw_text(screen, text, 25, y)
            y += 35

        back.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.is_clicked(event.pos):
                    return "menu"


def game_over_screen(screen, score, distance, coins):
    retry = Button(80, 400, 110, 45, "Retry")
    menu = Button(210, 400, 110, 45, "Main Menu")

    while True:
        screen.fill((255, 120, 120))

        draw_text(screen, "Game Over", 95, 120, "big")
        draw_text(screen, f"Score: {score}", 120, 210)
        draw_text(screen, f"Distance: {distance}", 120, 250)
        draw_text(screen, f"Coins: {coins}", 120, 290)

        retry.draw(screen)
        menu.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.is_clicked(event.pos):
                    return "retry"

                if menu.is_clicked(event.pos):
                    return "menu"