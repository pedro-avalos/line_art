# -*- coding: utf-8 -*-

import colorsys
import random


def rand_color() -> tuple[int, int, int]:
    """Generates a random color.

    Returns:
        tuple[int, int, int]: Random RGB color (values range 0-255).
    """

    h: float = random.random()
    s: float = 1
    v: float = 1

    float_rgb: tuple[float, float, float] = colorsys.hsv_to_rgb(h, s, v)
    rgb: list[int] = [int(x * 255) for x in float_rgb]

    return (rgb[0], rgb[1], rgb[2])


def interpolate(
    start_color: tuple[int, int, int],
    end_color: tuple[int, int, int],
    factor: float,
) -> tuple[int, int, int]:
    """Mixes the colors.

    Args:
        start_color (tuple[int, int, int]): First color.
        end_color (tuple[int, int, int]): Second color.
        factor (float): How much to mix the colors (0-1).

    Returns:
        tuple[int, int, int]: RGB color (values range 0-255).
    """

    recip: float = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor),
    )
