import itertools
import pytest

from padmini.prakriya import Prakriya, Term
from padmini.prakarana import tin_pratyaya as tin
from padmini.prakarana import it_samjna


@pytest.mark.parametrize(
    "la,pada,expected",
    [
        ("la~w", "p", "ti tas Ji si Tas Ta mi vas mas"),
        ("la~w", "a", "ta AtAm Ja TAs ATAm Dvam i vahi mahi"),
    ],
)
def test_adesha(la, pada, expected):
    # Comprehensive test for all purusha/vacana/pada.
    results = []
    for purusha, vacana in itertools.product(tin.PURUSHA, tin.VACANA):
        u = Term.make_upadesha(la)
        p = Prakriya.make([u])
        p.add_tags(purusha, vacana)
        if pada == "p":
            p.add_tags(tin.PADA[0])
        if pada == "a":
            p.add_tags(tin.PADA[1])

        tin.adesha(p)
        results.append(p.terms[-1].text)

    for e, actual in zip(expected.split(), results):
        assert e == actual


def iter_purusha_vacana_pada():
    for purusha, vacana, pada in itertools.product(tin.PADA, tin.PURUSHA, tin.VACANA):
        yield purusha, vacana, pada


@pytest.mark.parametrize(
    "la,expected",
    [
        (
            "la~w",
            ["ti tas Ji si Tas Ta mi vas mas", "te Ate Je se ATe Dve e vahe mahe"],
        ),
        ("li~w", ["a atus us Ta aTus a a va ma", "e Ate ire se ATe Dve e vahe mahe"]),
        (
            "lu~w",
            ["A rO ras si Tas Ta mi vas mas", "A rO ras se ATe Dve e vahe mahe"],
        ),
        (
            "lf~w",
            ["ti tas Ji si Tas Ta mi vas mas", "te Ate Je se ATe Dve e vahe mahe"],
        ),
        ("la~N", ["t tAm J s tam ta am va ma", "ta AtAm Ja TAs ATAm Dvam i vahi mahi"]),
        ("lu~N", ["t tAm J s tam ta am va ma", "ta AtAm Ja TAs ATAm Dvam i vahi mahi"]),
        ("lf~N", ["t tAm J s tam ta am va ma", "ta AtAm Ja TAs ATAm Dvam i vahi mahi"]),
        (
            "lo~w",
            [
                "tu tAm Ju hi tam ta A-ni A-va A-ma",
                "tAm AtAm JAm sva ATAm Dvam A-E A-vahE A-mahE",
            ],
        ),
        (
            "li~N",
            [
                "yAs-st yAs-stAm yAs-us",
                "yAs-s yAs-stam yAs-sta",
                "yAs-am yAs-va yAs-ma",
                "sIy-sta sIy-AstAm sIy-ran",
                "sIy-sTAs sIy-AsTAm sIy-Dvam",
                "sIy-a sIy-vahi sIy-mahi",
            ],
        ),
    ],
)
def test_siddhi(la, expected):
    """Test the basic form of each ending.

    This checks the surface form only -- no it checks yet.
    """
    results = []
    for purusha, vacana, pada in iter_purusha_vacana_pada():
        # Dummy root
        dhatu = Term.make_upadesha("BU")
        dhatu.add_tags("dhatu")

        u = Term.make_upadesha(la)
        p = Prakriya.make([dhatu, u])
        p.add_tags(purusha, vacana, pada)

        # Run earlier steps
        it_samjna.run(p, 1)
        tin.adesha(p)
        it_samjna.run(p, 1)
        tin.siddhi(p)
        for i, _ in enumerate(p.terms):
            it_samjna.run(p, i)
        results.append(p)

    expected = " ".join(expected)
    for e, prakriya in zip(expected.split(), results):
        actual = "-".join(x.text for x in prakriya.terms[1:])
        assert e == actual
