#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_art.py

Based off of pixegami/python-generative-art-tutorial on GitHub.
"""


import argparse
import os

from PIL import Image, ImageChops, ImageDraw

from src.colors.generator import interpolate, rand_color
from src.points.generator import (
    LovePointGenerator,
    PointGeneratorInterface,
    RandPointGenerator,
)
from src.points.point import Point
from src.util.args import parse_args


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
    points: list[Point] = [point_generator.generate() for _ in range(num_lines)]

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
        point_generator: PointGeneratorInterface = RandPointGenerator(args)
        #  point_generator: PointGeneratorInterface = LovePointGenerator(args)
        print(f"{i + 1}/{args.count}")
        generate_art(
            collection=args.collection,
            name=f"{args.collection}_img_{i}",
            target_size=args.size,
            scale_factor=args.scale_factor,
            num_lines=args.num_lines,
            point_generator=point_generator,
        )
