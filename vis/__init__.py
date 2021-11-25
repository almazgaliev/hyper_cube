import numpy as np
from typing import Tuple


def line_pixels(a: np.ndarray,
                b: np.ndarray):

    a = a.astype(int)
    b = b.astype(int)
    steep = False

    x0, y0, *_ = a
    x1, y1, *_ = b

    if abs(x1 - x0) < abs(y1 - y0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0
    derror = abs(dy) * 2

    error2 = 0

    y = y0
    for x in range(x0, x1 + 1):
        if steep:
            yield [y, x]
        else:
            yield [x, y]

        error2 += derror

        if error2 > dx:
            if y1 > y0:
                y += 1
            else:
                y -= 1
            error2 -= dx * 2


def draw_lines(vertexes: np.ndarray,
               lines: np.ndarray,
               img: np.ndarray,
               color: Tuple[int, int, int]):
    for line in lines:
        pixels = np.array(list(line_pixels(vertexes[line[0]][:-1],
                                           vertexes[line[1]][:-1]))).T
        img[pixels[0], pixels[1]] = color
