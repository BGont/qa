from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class PositiveInt(Validator):

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected {value!r} to be an int')
        if value <= 0:
            raise ValueError(
                f'Expected {value!r} to be greater than 0'
            )


class DegreeIntLess180(Validator):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f'Expected {value!r} to be an int')
        if value <= 0 or value >= 180:
            raise ValueError(
                f'Expected {value!r} to be greater than 0 and less than 180'
            )
