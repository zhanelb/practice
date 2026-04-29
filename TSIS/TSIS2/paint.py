import pygame
import sys
from tools import flood_fill, save_canvas, draw_shape

pygame.init()

WIDTH, HEIGHT = 950, 550
TOOLBAR_HEIGHT = 70

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (160, 32, 240)
PINK = (255, 105, 180)
LIGHT_BLUE = (135, 206, 250)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)

font = pygame.font.SysFont("Arial", 16)
text_font = pygame.font.SysFont("Arial", 28)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

color = BLACK
tool = "pencil"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
typed_text = ""

buttons = {
    "pencil": pygame.Rect(5, 10, 70, 30),
    "line": pygame.Rect(80, 10, 60, 30),
    "eraser": pygame.Rect(145, 10, 70, 30),
    "fill": pygame.Rect(220, 10, 55, 30),
    "text": pygame.Rect(280, 10, 55, 30),

    "rect": pygame.Rect(340, 10, 55, 30),
    "circle": pygame.Rect(400, 10, 65, 30),
    "square": pygame.Rect(470, 10, 65, 30),
    "r_tri": pygame.Rect(540, 10, 60, 30),
    "e_tri": pygame.Rect(605, 10, 60, 30),
    "rhomb": pygame.Rect(670, 10, 70, 30),

    "PU": pygame.Rect(750, 10, 35, 30),
    "PI": pygame.Rect(790, 10, 35, 30),
    "LB": pygame.Rect(830, 10, 35, 30),
    "K": pygame.Rect(870, 10, 35, 30),

    "clear": pygame.Rect(910, 10, 35, 30),
}

shape_tools = ["line", "rect", "circle", "square", "r_tri", "e_tri", "rhomb"]

clock = pygame.time.Clock()

def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and (
                pygame.key.get_mods() & pygame.KMOD_CTRL or pygame.key.get_mods() & pygame.KMOD_META
                ):
                save_canvas(canvas)

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = text_font.render(typed_text, True, color)
                    canvas.blit(text_surface, text_pos)
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    typed_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < TOOLBAR_HEIGHT:
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        if name in ["pencil", "line", "eraser", "fill", "text", "rect", "circle", "square", "r_tri", "e_tri", "rhomb"]:
                            tool = name

                        elif name == "PU":
                            color = PURPLE
                        elif name == "PI":
                            color = PINK
                        elif name == "LB":
                            color = LIGHT_BLUE
                        elif name == "K":
                            color = BLACK
                        elif name == "clear":
                            canvas.fill(WHITE)

            else:
                pos = canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], color)

                elif tool == "text":
                    text_mode = True
                    text_pos = pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size * 2)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = canvas_pos(event.pos)

                if tool in shape_tools:
                    draw_shape(canvas, tool, color, start_pos, end_pos, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    if drawing and tool in shape_tools:
        preview = canvas.copy()
        current_pos = canvas_pos(pygame.mouse.get_pos())
        draw_shape(preview, tool, color, start_pos, current_pos, brush_size)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_mode:
        text_surface = text_font.render(typed_text + "|", True, color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    for name, rect in buttons.items():
        shadow = rect.move(2, 2)
        pygame.draw.rect(screen, (150, 150, 150), shadow)

        if name == tool:
            pygame.draw.rect(screen, (170, 170, 170), rect)
        else:
            pygame.draw.rect(screen, GRAY, rect)

        pygame.draw.rect(screen, BLACK, rect, 1)

        if name == "PU":
            pygame.draw.circle(screen, PURPLE, rect.center, 10)
        elif name == "PI":
            pygame.draw.circle(screen, PINK, rect.center, 10)
        elif name == "LB":
            pygame.draw.circle(screen, LIGHT_BLUE, rect.center, 10)
        elif name == "K":
            pygame.draw.circle(screen, BLACK, rect.center, 10)
        else:
            text = font.render(name, True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    info = font.render(
        f"Tool: {tool} | Size: {brush_size} | Press 1/2/3 for size | Ctrl+S to save",
        True,
        BLACK
    )
    screen.blit(info, (10, 45))

    pygame.display.update()
    clock.tick(120)