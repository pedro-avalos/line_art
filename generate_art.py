#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_art.py

Based off of pixegami/python-generative-art-tutorial on GitHub.
"""


import abc
import argparse
import colorsys
import os
import random
from typing import NamedTuple
import math

from PIL import Image, ImageChops, ImageDraw


class Point(NamedTuple):
    """Class to represent a point.

    Attributes:
        x (int): x-coordinate.
        y (int): y-coordinate.
    """

    x: int
    y: int


class PointGeneratorInterface(metaclass=abc.ABCMeta):
    """Class to represent any generator of points."""

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "generate") and callable(subclass.generate)

    @abc.abstractmethod
    def generate(self) -> Point:
        """Generates a point."""

        raise NotImplementedError


class RandPointGenerator(PointGeneratorInterface):
    """Class to generate random points.

    Attributes:
        minimum (int): Minimum value for x or y in the point.
        maximum (int): Maximum value for x or y in the point.
    """

    def __init__(
        self,
        minimum: int,
        maximum: int,
    ) -> None:

        super().__init__()
        self.minimum: int = minimum
        self.maximum: int = maximum

    def generate(self) -> Point:
        return Point(
            random.randint(self.minimum, self.maximum),
            random.randint(self.minimum, self.maximum),
        )


class LovePointGenerator(PointGeneratorInterface):
    """Class to generate points based on a distorted heart.

    Attributes:
        minimum (int): Minimum value for the image's coordinates.
        maximum (int): Maximum value for the image's coordinates.
        t (float): Current value for parametric equation.
        step (float): What to increase t by each generation.
    """

    def __init__(self, minimum: int, maximum: int, n: int) -> None:
        super().__init__()
        self.minimum: int = minimum
        self.maximum: int = maximum
        self.t: float = 0
        self.step: float = (2 * math.pi) / n

    def generate(self) -> Point:
        i: float = self.t
        self.t += self.step
        return Point(
            self.maximum - int(self.maximum * pow(math.sin(i), 3)),
            self.maximum - int(
                ((0.8 * random.random() * self.maximum) * math.cos(i))
                - ((0.6 * random.random() * self.maximum) * math.cos(2 * i))
                - ((0.2 * random.random() * self.maximum) * math.cos(3 * i))
                - ((0.1 * random.random() * self.maximum) * math.cos(4 * i)))
        )



def parse_args() -> argparse.Namespace:
    """Parses the arguments.

    Returns:
        argparse.Namespace: Namespace of the arguments passed to the script.
    """

    parser = argparse.ArgumentParser(description="Generate random art")
    parser.add_argument(
        "--collection",
        type=str,
        help="name of collection",
        required=False,
        default="collection",
    )
    parser.add_argument(
        "--count",
        type=int,
        help="how many images to generate",
        required=False,
        default=10,
    )
    parser.add_argument(
        "--size",
        type=int,
        help="size of the image in pixels",
        required=False,
        default=720,
    )
    parser.add_argument(
        "--scale_factor",
        type=int,
        help="scaling used in antialiasing",
        required=False,
        default=2,
    )
    parser.add_argument(
        "--margin",
        type=float,
        help="margin size",
        required=False,
        default=0.1,
    )
    parser.add_argument(
        "--num_lines",
        type=int,
        help="how many lines to draw",
        required=False,
        default=10,
    )

    return parser.parse_args()


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


def generate_points(
    generator: PointGeneratorInterface,
    n: int,
) -> list[Point]:
    """Generate the list of points.

    Args:
        func (Callable["...", tuple[int, int]]): Function used to generate a single point.
        args (dict[str, Any]): Arguments passed to each call of func.
        n (int): How many points to generate.

    Returns:
        list[Point]: List of points.
    """

    return [generator.generate() for _ in range(n)]


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


def generate_art(
    collection: str,
    name: str,
    target_size: int,
    scale_factor: int,
    num_lines: int,
    point_generator: PointGeneratorInterface,
) -> None:
    """Generates and saves the art piece(s).

    Args:
        collection (str): Folder containing the image.
        name (str): Name of the image, without the file extension.
        target_size (int): Size of the image.
        scale_factor (int): Scaling for antialiasing.
        num_lines (int): Number of lines to draw.
        point_generator (PointGeneratorInterface): Used to generate points.
    """

    # Where to store image
    output_dir: str = os.path.join("output", collection)
    img_path: str = os.path.join(output_dir, f"{name}.png")

    # Parameters
    bg_color: tuple[int, int, int] = (0, 0, 0)
    size: int = target_size * scale_factor

    # Create the directory and base image
    os.makedirs(output_dir, exist_ok=True)
    img: Image.Image = Image.new("RGB", (size, size), color=bg_color)

    # Generate colors of lines
    start_color: tuple[int, int, int] = rand_color()
    end_color: tuple[int, int, int] = rand_color()

    # Generate the points
    points: list[Point] = generate_points(generator=point_generator, n=num_lines)

    # Draw bounding box
    min_x: int = points[0].x
    max_x: int = points[0].x
    min_y: int = points[0].y
    max_y: int = points[0].y
    for (x, y) in points:
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    # Center the image
    delta_x = min_x - (size - max_x)
    delta_y = min_y - (size - max_y)
    points = [Point(x - delta_x // 2, y - delta_y // 2) for (x, y) in points]

    # Draw the points
    thickness: int = scale_factor
    n: int = len(points) - 1
    for i, p1 in enumerate(points):
        # Create the overlay
        overlay_img: Image.Image = Image.new("RGB", (size, size), color=bg_color)
        overlay_draw: ImageDraw.ImageDraw = ImageDraw.Draw(overlay_img)

        # Connect last point to first, or to the next element
        p2 = points[0] if i == n else points[i + 1]

        # Find the current color for the line
        color_factor: float = i / n
        line_color: tuple[int, int, int] = interpolate(
            start_color, end_color, color_factor
        )

        # Draw the line
        overlay_draw.line((p1, p2), fill=line_color, width=thickness)

        # Increase the thickness for the next line
        thickness += scale_factor if color_factor < 0.5 else -scale_factor

        # Add the overlay channel
        img = ImageChops.add(img, overlay_img)

    # Resize to make it smoother
    img = img.resize(
        (size // scale_factor, size // scale_factor), resample=Image.ANTIALIAS
    )

    # Save the image
    img.save(img_path)


if __name__ == "__main__":
    args: argparse.Namespace = parse_args()

    for i in range(args.count):
        size: int = args.size
        minimum: int = int(size * args.margin)
        maximum: int = size - minimum
        point_generator: PointGeneratorInterface = RandPointGenerator(minimum, maximum)
        #  point_generator: PointGeneratorInterface = LovePointGenerator(
        #      minimum=minimum,
        #      maximum=maximum,
        #      n=args.num_lines,
        #  )
        print(f"{i + 1}/{args.count}")
        generate_art(
            collection=args.collection,
            name=f"{args.collection}_img_{i}",
            target_size=args.size,
            scale_factor=args.scale_factor,
            num_lines=args.num_lines,
            point_generator=point_generator,
        )
