import pygame
from collections import deque
from datetime import datetime


def flood_fill(surface, x, y, fill_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))


def save_canvas(canvas):
    filename = "paint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_shape(surface, tool, color, start_pos, end_pos, size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    left = min(x1, x2)
    top = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    if tool == "line":
        pygame.draw.line(surface, color, start_pos, end_pos, size)

    elif tool == "rect":
        pygame.draw.rect(surface, color, (left, top, w, h), size)

    elif tool == "circle":
        radius = max(w, h) // 2
        pygame.draw.circle(surface, color, start_pos, radius, size)

    elif tool == "square":
        side = max(w, h)
        pygame.draw.rect(surface, color, (x1, y1, side, side), size)

    elif tool == "r_tri":
        points = [(x1, y1), (x2, y2), (x1, y2)]
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "e_tri":
        points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y1)]
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "rhomb":
        points = [
            ((x1 + x2) // 2, y1),
            (x2, (y1 + y2) // 2),
            ((x1 + x2) // 2, y2),
            (x1, (y1 + y2) // 2)
        ]
        pygame.draw.polygon(surface, color, points, size)