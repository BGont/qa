from .validators import PositiveInt
from .shape import GeometricShape


class Rectangle(GeometricShape):

    side1 = PositiveInt()
    side2 = PositiveInt()
    _angles = 4

    def __init__(self, side1, side2):
        super(Rectangle, self).__init__()

        self.side1 = side1
        self.side2 = side2

    @property
    def area(self):
        return self.side1 * self.side2

    @property
    def perimeter(self):
        return self.side1 * 2 + self.side2 * 2

    @property
    def angles(self):
        return self._angles
