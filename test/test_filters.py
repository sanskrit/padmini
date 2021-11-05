import pytest
from padmini.prakriya import Term
import padmini.filters as f


@pytest.mark.parametrize(
    "text,expected",
    [
        ("sTA", True),
        ("BU", False),
        ("as", False),
    ],
)
def test_samyogadi(text, expected):
    t = Term.make_upadesha(text)
    assert f.samyogadi(t) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("kram", False),
        ("BU", False),
        ("syand", True),
    ],
)
def test_samyoganta(text, expected):
    t = Term.make_upadesha(text)
    assert f.samyoganta(t) == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        ("hu", True),
        ("uK", True),
        ("hU", False),
        ("ind", False),
    ],
)
def test_is_laghu(text, expected):
    t = Term.make_upadesha(text)
    assert f.is_laghu(t) == expected
