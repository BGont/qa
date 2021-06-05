from math import pi

from .validators import PositiveInt
from .shape import GeometricShape


class Circle(GeometricShape):

    radius = PositiveInt()
    _angles = 0

    def __init__(self, radius):
        super(Circle, self).__init__()

        self.radius = radius

    @property
    def area(self):
        return round(self.radius ** 2 * pi, 3)

    @property
    def perimeter(self):
        return round(2 * self.radius * pi, 3)

    @property
    def angles(self):
        return self._angles
