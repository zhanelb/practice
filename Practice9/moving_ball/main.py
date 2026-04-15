import pygame
import sys
from ball import Ball
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
ball = Ball(400, 300, 25, 5, WIDTH, HEIGHT)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed() 
    ball.move(keys)                  
    screen.fill((255, 255, 255))    
    ball.draw(screen)           
    pygame.display.flip()
pygame.quit()
sys.exit()