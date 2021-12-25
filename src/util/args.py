# -*- coding: utf-8 -*-

import argparse


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
        "--num_points",
        type=int,
        help="how many points to generate",
        required=False,
        default=10,
    )

    return parser.parse_args()
