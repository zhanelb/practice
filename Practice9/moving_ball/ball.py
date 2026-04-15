import pygame
class Ball:
    def __init__(self, x, y, radius, speed, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = (230, 124, 180)  
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.radius - self.speed >= 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.radius + self.speed <= self.screen_width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.radius - self.speed >= 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.radius + self.speed <= self.screen_height:
            self.y += self.speed
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)