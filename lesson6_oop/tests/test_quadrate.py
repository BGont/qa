import pytest
from lesson6_oop import Quadrate, Triangle


@pytest.fixture
def quadrate_object():
    shape_object = Quadrate(side_length=3)
    return shape_object


def test_name(quadrate_object):
    assert quadrate_object.name == "Quadrate"


def test_area(quadrate_object):
    assert quadrate_object.area == 9


def test_perimeter(quadrate_object):
    assert quadrate_object.perimeter == 12


def test_angles(quadrate_object):
    assert quadrate_object.angles == 4


@pytest.mark.parametrize("added_shape, expected",
                         [(Quadrate(side_length=5), 34), (Quadrate(side_length=6), 45), (Triangle(20, 20, 60), 182.205)])
def test_add_area(quadrate_object, added_shape, expected):
    assert quadrate_object.add_area(added_shape) == expected


def test_add_area_wrong_argument(quadrate_object):
    wrong_obj = object()
    with pytest.raises(TypeError):
        assert quadrate_object.add_area(wrong_obj)
