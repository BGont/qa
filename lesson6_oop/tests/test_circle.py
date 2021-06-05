import pytest
from lesson6_oop import Circle, Quadrate


@pytest.fixture
def circle_object():
    shape_object = Circle(radius=10)
    return shape_object


def test_name(circle_object):
    assert circle_object.name == "Circle"


def test_area(circle_object):
    assert circle_object.area == 314.159


def test_perimeter(circle_object):
    assert circle_object.perimeter == 62.832


def test_angles(circle_object):
    assert circle_object.angles == 0


@pytest.mark.parametrize("added_shape, expected",
                         [(Quadrate(side_length=10), 414.159)])
def test_add_area(circle_object, added_shape, expected):
    assert circle_object.add_area(added_shape) == expected
