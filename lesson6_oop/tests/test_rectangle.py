import pytest
from lesson6_oop import Rectangle, Quadrate


@pytest.fixture
def rectangle_object():
    shape_object = Rectangle(side1=4, side2=2)
    return shape_object


def test_name(rectangle_object):
    assert rectangle_object.name == "Rectangle"


def test_area(rectangle_object):
    assert rectangle_object.area == 8


def test_perimeter(rectangle_object):
    assert rectangle_object.perimeter == 12


def test_angles(rectangle_object):
    assert rectangle_object.angles == 4


@pytest.mark.parametrize("added_shape, expected",
                         [(Rectangle(side1=3, side2=2), 14), (Quadrate(side_length=5), 33)])
def test_add_area(rectangle_object, added_shape, expected):
    assert rectangle_object.add_area(added_shape) == expected
