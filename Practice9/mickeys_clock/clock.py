import pygame
import datetime
import math
class MickeyClock:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Mickey Clock")
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("images/mickeyclock.jpeg")
        self.bg = pygame.transform.scale(self.bg, (600, 600))
        self.center = (300, 300)
    def get_time(self):
        now = datetime.datetime.now()
        return now.minute, now.second
    def draw_hand(self, angle, length, color, width):
        rad = math.radians(angle)
        x = self.center[0] + length * math.cos(rad)
        y = self.center[1] - length * math.sin(rad)
        pygame.draw.line(self.screen, color, self.center, (x, y), width)
    def draw(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.blit(self.bg, (0, 0))
            minutes, seconds = self.get_time()
            min_angle = 90 - minutes * 6
            sec_angle = 90 - seconds * 6
            self.draw_hand(min_angle, 120, (0, 0, 0), 6)  
            self.draw_hand(sec_angle, 140, (255, 0, 0), 3) 
            pygame.display.flip()
            self.clock.tick(1)
        pygame.quit()