import pytest
from lesson6_oop import Triangle


@pytest.fixture
def triangle_object():
    shape_object = Triangle(20, 20, 60)
    return shape_object


def test_name(triangle_object):
    assert triangle_object.name == "Triangle"


def test_area(triangle_object):
    assert triangle_object.area == 173.205


def test_perimeter(triangle_object):
    assert triangle_object.perimeter == 60


def test_angles(triangle_object):
    assert triangle_object.angles == 3


@pytest.mark.parametrize("added_shape, expected",
                         [(Triangle(10, 10, 60), 216.506)])
def test_add_area(triangle_object, added_shape, expected):
    assert triangle_object.add_area(added_shape) == expected


def test_side3(triangle_object):
    assert triangle_object.side3 == 20

