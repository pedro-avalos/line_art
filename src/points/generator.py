# -*- coding: utf-8 -*-

import abc
import math
import random

from src.points.point import Point


class PointGeneratorInterface(metaclass=abc.ABCMeta):
    """Class to represent any generator of points."""

    @classmethod
    def __subclasshook__(cls, subclass) -> bool:
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
            self.maximum
            - int(
                (0.8 * random.random() * self.maximum * math.cos(i))
                - (0.6 * random.random() * self.maximum * math.cos(2 * i))
                - (0.2 * random.random() * self.maximum * math.cos(3 * i))
                - (0.1 * random.random() * self.maximum * math.cos(4 * i))
            ),
        )
