import pytest
from padmini import sounds as S


@pytest.mark.parametrize(
    "p,expected",
    [
        ("ac", "aAiIuUfFxXeEoO"),
        ("yaR", "yrvl"),
        ("hal", "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"),
        ("Yam", "YmNRn"),
        ("Sar", "Szs"),
    ],
)
def test_pratyahara(p, expected):
    assert S._pratyahara(p) == set(expected)


@pytest.mark.parametrize(
    "sound,expected",
    [
        ("k", "kKgGN"),
        ("c", "cCjJY"),
        ("a", "aA"),
    ],
)
def test_savarna(sound, expected):
    assert S.savarna(sound) == set(expected)


def test_map_sounds_jhal_jash():
    mapping = S.map_sounds(S.s("Jal"), S.s("jaS"))
    assert mapping == {
        "J": "j",
        "B": "b",
        "G": "g",
        "Q": "q",
        "D": "d",
        "j": "j",
        "b": "b",
        "g": "g",
        "q": "q",
        "d": "d",
        "K": "g",
        "P": "b",
        "C": "j",
        "W": "q",
        "T": "d",
        "c": "j",
        "w": "q",
        "t": "d",
        "k": "g",
        "p": "b",
        "S": "j",
        "z": "q",
        "s": "d",
        "h": "g",
    }


# Flaky
def test_map_sounds_kuh_cu():
    mapping = S.map_sounds(S.s("ku~ h"), S.s("cu~"))
    assert mapping == {
        "k": "c",
        "K": "C",
        "g": "j",
        "G": "J",
        "N": "Y",
        "h": "J",
    }
