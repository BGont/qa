from abc import ABC, abstractmethod


class GeometricShape(ABC):
    def __init__(self):
        self._name = self.__class__.__name__

    @property
    def name(self):
        return self._name

    @property
    @abstractmethod
    def area(self):
        pass

    @property
    @abstractmethod
    def angles(self):
        pass

    @property
    @abstractmethod
    def perimeter(self):
        pass

    def add_area(self, geometric_shape):
        if isinstance(geometric_shape, GeometricShape):
            return round(self.area + geometric_shape.area, 3)
        else:
            raise TypeError("Argument is not subclass of GeometricShape")
