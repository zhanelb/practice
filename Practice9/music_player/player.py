import pygame
import os
class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Music Player")
        self.font = pygame.font.SysFont(None, 36)
        self.playlist = [
            "music/track1.mp3",
            "music/track2.mp3"
        ]
        self.current = 0
        self.is_playing = False
    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.is_playing = True
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
    def next_track(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()
    def prev_track(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()
    def draw_text(self, text, y):
        render = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(render, (50, y))
    def run(self):
        running = True
        while running:
            self.screen.fill((245, 184, 208))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play()
                    elif event.key == pygame.K_s:
                        self.stop()
                    elif event.key == pygame.K_n:
                        self.next_track()
                    elif event.key == pygame.K_b:
                        self.prev_track()
                    elif event.key == pygame.K_q:
                        running = False
            track_name = os.path.basename(self.playlist[self.current])
            self.draw_text(f"Track: {track_name}", 100)
            status = "Playing" if self.is_playing else "Stopped"
            self.draw_text(f"Status: {status}", 150)
            pygame.display.flip()

        pygame.quit()