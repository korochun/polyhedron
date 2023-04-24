from math import pi, sqrt

from pytest import approx
from pytest import mark

from shadow.polyedr import Polyedr

tests = {
    "simple": 4,
    "simple_small": 4,  # масштаб не влияет
    "simple_gone": 0,   # центр грани в кубе из условия
    "simple_tilt": 2,   # поворот на 60˚
    "simple_hide": 0,   # скрытая грань
    "simple_degenerate": 0,
    "simple_partial": 4,
    "cube_rot": (1 + sqrt(3)) * 2,
    "tetrahedron": 4 / 3 * sqrt(3)
}


@mark.parametrize("name,answer", tests.items(), ids=tests.keys())
def test_example(name, answer):
    assert Polyedr(f"tests/data/{name}.geom").draw() == approx(answer)
