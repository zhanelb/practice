import pygame
from game import SnakeGame

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("TSIS4 Snake Game")

game = SnakeGame(screen)
game.run()

pygame.quit()