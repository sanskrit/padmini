import itertools

from padmini import operations as op
from padmini.constants import Tag as T
from padmini.prakriya import Term, Prakriya, VyakaranaException
from . import it_samjna


VIBHAKTI = [T.V1, T.V2, T.V3, T.V4, T.V5, T.V6, T.V7]
VACANA = [T.EKAVACANA, T.DVIVACANA, T.BAHUVACANA]


def _make_sup():
    text = [
        "su~",
        "O",
        "jas",
        "am",
        "Ow",
        "Sas",
        "wA",
        "ByAm",
        "Bis",
        "Ne",
        "ByAm",
        "Byas",
        "Nasi~",
        "ByAm",
        "Byas",
        "Nas",
        "os",
        "Am",
        "Ni",
        "os",
        "sup",
    ]
    terms = [Term.make_upadesha(x) for x in text]

    for i, u in enumerate(terms):
        # 3.1.1, 1.4.104
        u.add_tags(T.PRATYAYA, T.SUP, T.VIBHAKTI)
        u.add_tags(VIBHAKTI[(i // 3)])
        u.add_tags(VACANA[i % 3])
    return terms


SUP = _make_sup()


def adesha(p: Prakriya):
    """Add a sup-pratyaya.

    :param p: the prakriya
    """
    for vibhakti, vacana in itertools.product(VIBHAKTI, VACANA):
        if p.all(vibhakti, vacana):
            break
    else:
        raise VyakaranaException("prakriya needs all of (vibhakti, vacana)")

    for ending in SUP:
        if ending.all(vibhakti, vacana):
            break
    else:
        raise VyakaranaException("bad state: ending without vibhakti/vacana match")

    sup = Term.make_upadesha(ending.u)
    sup.add_tags(sup.u, *ending.tags)
    p.terms += [sup]
    p.step("4.1.2")
    it_samjna.run_no_index(p, sup)


def run(p: Prakriya):
    adesha(p)
