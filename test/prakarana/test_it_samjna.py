import pytest

from padmini.prakarana import it_samjna
from padmini.prakriya import Prakriya, Term


@pytest.mark.parametrize(
    "raw,expected,its",
    [
        ("qukfY", "kf", {"qu", "Y"}),
        ("qupa\\ca~^z", "pac", {"qu", "a", "z", "anudAtta", "svaritet"}),
        ("mUtra~", "mUtr", {"a"}),
        ("vftu~\\", "vft", {"u", "anudAttet"}),
        ("df\\Si~r", "dfS", {"ir", "anudAtta"}),
    ],
)
def test_common(raw, expected, its):
    p = Prakriya.make([Term.make_upadesha(raw)])

    it_samjna.run(p, 0)
    res = p.terms[0]
    assert expected == res.text
    assert its == res.tags


@pytest.mark.parametrize(
    "raw,expected,its",
    [
        # Normal
        ("su~", "s", ["u"]),
        ("tip", "ti", ["p"]),
        # Exception
        ("mas", "mas", []),
        ("AtAm", "AtAm", []),
    ],
)
def test_vibhakti(raw, expected, its):
    u = Term.make_upadesha(raw)
    u.tags.add("vibhakti")
    p = Prakriya.make([u])

    it_samjna.run(p, 0)
    res = p.terms[0]
    assert expected == res.text
    assert all(it in res.tags for it in its)


@pytest.mark.parametrize(
    "raw,expected,its",
    [
        ("la~w", "l", ["a", "w"]),
        ("Ric", "i", ["R", "c"]),
    ],
)
def test_pratyaya(raw, expected, its):
    u = Term.make_upadesha(raw)
    u.tags.add("pratyaya")
    p = Prakriya.make([u])

    it_samjna.run(p, 0)
    res = p.terms[0]
    assert expected == res.text
    assert all(it in res.tags for it in its)
