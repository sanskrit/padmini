import pytest

from padmini.prakarana import abhyasasya


@pytest.mark.parametrize(
    "start,expected",
    [
        ("as", "a"),
        ("BU", "BU"),
        ("kram", "ka"),
    ],
)
def test_haladi(start, expected):
    assert abhyasasya.haladi(start) == expected


@pytest.mark.parametrize(
    "start,expected",
    [
        ("sparD", "pa"),
        ("sTA", "TA"),
        ("scyut", "cu"),
    ],
)
def test_sharpurva(start, expected):
    assert abhyasasya.sharpurva(start) == expected
