from .validators import PositiveInt
from .shape import GeometricShape


class Quadrate(GeometricShape):

    side_length = PositiveInt()
    _angles = 4

    def __init__(self, side_length):
        super(Quadrate, self).__init__()

        self.side_length = side_length

    @property
    def area(self):
        return self.side_length ** 2

    @property
    def perimeter(self):
        return self.side_length * 4

    @property
    def angles(self):
        return self._angles
