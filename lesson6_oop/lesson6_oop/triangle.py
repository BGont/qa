from math import sqrt, cos, radians

from .validators import PositiveInt, DegreeIntLess180
from .shape import GeometricShape


class Triangle(GeometricShape):

    side1 = PositiveInt()
    side2 = PositiveInt()
    degree = DegreeIntLess180()
    _angles = 3

    def __init__(self, side1, side2, degree):
        super(Triangle, self).__init__()

        self.side1 = side1
        self.side2 = side2
        self.degree = degree

    @property
    def side3(self):
        radians_degree = round(radians(self.degree), 3)
        side3_ = sqrt(self.side1 ** 2 + self.side2 ** 2 - 2*self.side1*self.side2*cos(radians_degree))
        return round(side3_, 2)

    @property
    def area(self):
        half_perimeter = self.perimeter / 2
        area_ = sqrt(half_perimeter * (half_perimeter - self.side1) * (half_perimeter - self.side2) * (half_perimeter - self.side3))
        return round(area_, 3)

    @property
    def perimeter(self):
        return self.side1 + self.side2 + self.side3

    @property
    def angles(self):
        return self._angles
