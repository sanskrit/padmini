import itertools
import pytest

from padmini.prakarana import atmanepada
from padmini.prakarana import it_samjna
from padmini.prakriya import Prakriya, Term
from padmini.constants import Tag


@pytest.mark.parametrize(
    "dhatu,gana,expected",
    [
        # Default
        ("BU", 1, "P"),
        # anudAttet
        ("eDa~\\", 1, "A"),
        # Nit
        ("hnu\\N", 2, "A"),
        # svaritet
        ("dvi\\za~^", 2, "U"),
        # Yit
        ("qukf\\Y", 8, "U"),
        # ni-viS (one upasarga, A)
        ("vi\\Sa~", 6, "P"),
        ("ni-vi\\Sa~", 6, "A"),
        # pari-ji, vi-ji, ava-ji (choice of upasarga, A)
        ("ji\\", 1, "P"),
        ("pari-ji\\", 1, "A"),
        ("vi-ji\\", 1, "A"),
        ("ava-ji\\", 1, "A"),
        # pra-vah (one upasarga, P)
        ("pra-vah\\a~^", 1, "P"),
    ],
)
def test_atmanepada_lat(dhatu, gana, expected):
    terms = dhatu.split("-")

    upasargas = [Term.make_term(x) for x in terms[:-1]]
    for u in upasargas:
        u.add_tags("upasarga")

    dhatu = Term.make_dhatu(terms[-1], gana)
    dhatu.add_tags("dhatu")

    # Prepare the prakriya
    pratyaya = Term.make_upadesha("la~w")
    pratyaya.add_tags("pratyaya")
    p = Prakriya.make(upasargas + [dhatu, pratyaya])
    for i, u in enumerate(p.terms):
        if not u.all("upasarga"):
            it_samjna.run(p, i)
    p.add_tags("kartari")
    assert not p.options_seen

    atmanepada.run(p)

    assert expected in {"P", "A", "U"}
    if expected == "P":
        assert p.any(Tag.PARASMAIPADA)
        assert not p.options_seen
    elif expected == "A":
        assert p.any(Tag.ATMANEPADA)
        assert not p.options_seen
    else:
        assert p.options_seen
