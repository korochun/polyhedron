from pytest import approx
from pytest import mark

from shadow.polyedr import Polyedr

tests = {
    "simple": 4
}


@mark.parametrize("name,answer", tests.items())
def test_(name, answer):
    assert Polyedr(f"tests/data/{name}.geom").draw() == approx(answer)
