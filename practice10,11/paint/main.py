import pygame
import sys

pygame.init()

# screen
width, height = 950, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint with Buttons")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (160, 32, 240)
PINK = (255, 105, 180)
LIGHT_BLUE = (135, 206, 250)
GRAY = (200, 200, 200)

screen.fill(WHITE)

# tool settings
color = BLACK
tool = "brush"
drawing = False
radius = 5

font = pygame.font.SysFont("Arial", 18)

# buttons (rectangles)
buttons = {
    "brush": pygame.Rect(10, 10, 80, 35),
    "eraser": pygame.Rect(95, 10, 80, 35),
    "circle": pygame.Rect(180, 10, 80, 35),
    "rect": pygame.Rect(265, 10, 80, 35),
    "square": pygame.Rect(350, 10, 80, 35),
    "r_tri": pygame.Rect(435, 10, 80, 35),
    "e_tri": pygame.Rect(520, 10, 80, 35),
    "rhomb": pygame.Rect(605, 10, 80, 35),

    "PU": pygame.Rect(690, 10, 40, 35),
    "PI": pygame.Rect(735, 10, 40, 35),
    "LB": pygame.Rect(780, 10, 40, 35),
    "K": pygame.Rect(825, 10, 40, 35),

    "clear": pygame.Rect(870, 10, 70, 35),
}

clock = pygame.time.Clock()


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            drawing = True

            # check buttons
            for name, rect in buttons.items():
                if rect.collidepoint(mx, my):

                    # tools
                    if name in ["brush", "eraser", "circle", "rect", "square", "r_tri", "e_tri", "rhomb"]:
                        tool = name
                    if name == "clear":
                        screen.fill(WHITE)
                    # colors
                    if name == "PU":
                        color = PURPLE
                    if name == "PI":
                        color = PINK
                    if name == "LB":
                        color = LIGHT_BLUE
                    if name == "K":
                        color = BLACK

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    mx, my = pygame.mouse.get_pos()

    # drawing area (not over buttons)
    if drawing and my > 50:

        if tool == "brush":
            pygame.draw.circle(screen, color, (mx, my), radius)

        elif tool == "eraser":
            pygame.draw.circle(screen, WHITE, (mx, my), radius * 2)

        elif tool == "circle":
            pygame.draw.circle(screen, color, (mx, my), 30)

        elif tool == "rect":
            pygame.draw.rect(screen, color, (mx, my, 40, 40))
        elif tool == "square":
            pygame.draw.rect(screen, color, (mx, my, 50, 50))

        elif tool == "r_tri":
            points = [(mx, my), (mx+50, my), (mx, my+50)]
            pygame.draw.polygon(screen, color, points)

        elif tool == "e_tri":
            points = [(mx, my), (mx+50, my), (mx+25, my-43)]
            pygame.draw.polygon(screen, color, points)

        elif tool == "rhomb":
            points = [
                (mx, my-30),
                (mx+30, my),
                (mx, my+30),
                (mx-30, my)
            ]
            pygame.draw.polygon(screen, color, points)

    
    for name, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)

        text = font.render(name, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(120)