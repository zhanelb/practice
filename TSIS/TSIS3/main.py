import pygame
import sys

from ui import init_fonts, main_menu, username_screen, leaderboard_screen, game_over_screen
from racer import start_game, settings_screen, WIDTH, HEIGHT

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")

init_fonts()


while True:
    choice = main_menu(screen)

    if choice == "play":
        username = username_screen(screen)

        if username is None:
            pygame.quit()
            sys.exit()

        result = start_game(screen, username)

        if result == "quit":
            pygame.quit()
            sys.exit()

        if result[0] == "game_over":
            _, score, distance, coins = result

            over_choice = game_over_screen(screen, score, distance, coins)

            if over_choice == "quit":
                pygame.quit()
                sys.exit()

            if over_choice == "retry":
                result = start_game(screen, username)

            if over_choice == "menu":
                continue

    elif choice == "leaderboard":
        result = leaderboard_screen(screen)

        if result == "quit":
            pygame.quit()
            sys.exit()

    elif choice == "settings":
        result = settings_screen(screen)

        if result == "quit":
            pygame.quit()
            sys.exit()

    elif choice == "quit":
        pygame.quit()
        sys.exit()