"""
tin_pratyaya
~~~~~~~~~~~~
(3.4.77 - end of 3.4)

The rules in this section have two main functions:

1. Replace a giving lakāra with the appropriate tiṅ-pratyaya. This is called
   tiṅ-ādeśa ("verb ending substitution"). To perform tiṅ-ādeśa, we must know
   the puruṣa, vacana, and pada associated with this prakriyā.

2. Modify the basic tiṅ-pratyaya according to the lakāra and any other
   conditions relevant to the prakriyā (for example, vidhi-liṅ vs. āśīr-liṅ).
   This is called tiṅ-siddhi ("verb ending completion").

All of these rules are found at the end of section 3.4 of the Ashtadhyayi.
"""

import itertools

from . import it_samjna
from padmini.prakriya import Term, Prakriya, VyakaranaException
from padmini.constants import Tag as T
import padmini.filters as f
from padmini import operations as op
from padmini.sounds import s


PURUSHA = [T.PRATHAMA, T.MADHYAMA, T.UTTAMA]
VACANA = [T.EKAVACANA, T.DVIVACANA, T.BAHUVACANA]
PADA = [T.PARASMAIPADA, T.ATMANEPADA]

TIN_PARA = ["ti", "tas", "Ji", "si", "Tas", "Ta", "mi", "vas", "mas"]
NAL_ADI = ["Ral", "atus", "us", "Tal", "aTus", "a", "Ral", "va", "ma"]
TIN_NAL_MAPPING = dict(zip(TIN_PARA, NAL_ADI))
TAJHAYOH = {"ta": "eS", "Ja": "irec"}


def _make_tin():
    """Define the tin endings with their proper samjnas."""
    text = [
        "tip",
        "tas",
        "Ji",
        "sip",
        "Tas",
        "Ta",
        "mip",
        "vas",
        "mas",
        "ta",
        "AtAm",
        "Ja",
        "TAs",
        "ATAm",
        "Dvam",
        "iw",
        "vahi",
        "mahiN",
    ]
    terms = [Term.make_upadesha(x) for x in text]

    for i, u in enumerate(terms):
        # 3.1.1, 1.4.104
        u.add_tags(T.PRATYAYA, T.TIN, T.VIBHAKTI)
        # 1.4.101
        u.add_tags(PURUSHA[(i // 3) % 3])
        # 1.4.102
        u.add_tags(VACANA[i % 3])
        # 1.4.99 - 1.4.100
        u.add_tags(PADA[i // 9])
    return terms


TIN = _make_tin()


def adesha(p: Prakriya):
    """Replace the lakAra with a tiN-pratyaya.

    :param p: the prakriya
    """
    for purusha, vacana, pada in itertools.product(PURUSHA, VACANA, PADA):
        if p.all(purusha, vacana, pada):
            break
    else:
        raise VyakaranaException("prakriya needs all of (purusha, vacana, pada)")

    for ending in TIN:
        if ending.all(purusha, vacana, pada):
            break
    else:
        raise VyakaranaException("bad state: ending without purusha/vacana/pada match")

    la = p.terms[-1]
    la.add_tags(la.u, *ending.tags)
    op.upadesha("3.4.78", p, la, ending.u)

    # Ignone Nit-tva that we get from the lakAra. Kashika on 3.4.103:
    #
    #   lakArAzrayaGitvam AdezAnAM na bhavati.
    #
    # Likewise, this rule ignores the N of mahiN, which is just for the sake
    # of making a pratyAhAra.
    if la.any("N"):
        la.tags.remove("N")


def _jher_jus(p, la):
    if la.u != "Ji":
        return

    if la.all("li~N"):
        op.upadesha("3.4.108", p, la, "jus")

    elif f.is_nit_lakara(la):
        _, dhatu = p.find_last(T.DHATU)
        prev = [t for t in p.terms[-2::-1] if t.text][0]

        _vid = prev.text == "vid" and prev.gana == 2
        if prev.u == "si~c" or prev.any(T.ABHYASTA) or _vid:
            op.upadesha("3.4.109", p, la, "jus")
        elif prev.antya == "A" and p.terms[-2].u == "si~c":
            op.upadesha("3.4.100", p, la, "jus")
        elif la.all("la~N"):
            if dhatu.text == "dviz":
                op.optional(op.upadesha, "3.4.112", p, la, "jus")
            elif prev.antya == "A" and prev.any(T.DHATU):
                op.optional(op.upadesha, "3.4.111", p, la, "jus")


def ardhadhatuka_siddhi(p: Prakriya):
    terms = p.terms
    assert len(terms) >= 2, terms
    _, dhatu = p.find_last(T.DHATU)
    la = terms[-1]


def siddhi(p: Prakriya):
    """Apply substitutions to the given tin suffix.

    Due to rule 3.4.109 ("sic-abhyasta-vidibhyaH ca"), this should run after
    dvitva and the insertion of vikaraNas.

    :param p: the prakriya
    """

    terms = p.terms
    assert len(terms) >= 2, terms
    _, dhatu = p.find_last(T.DHATU)
    la = terms[-1]

    # 2.4.85 is a special case.
    if la.all("lu~w") and la.all(T.PRATHAMA):
        if la.all(T.EKAVACANA):
            ending = "qA"
        elif la.all(T.DVIVACANA):
            ending = "rO"
        elif la.all(T.BAHUVACANA):
            ending = "ras"
        else:
            raise VyakaranaException(f"Term in bad state: {la}")
        op.upadesha("2.4.85", p, la, ending)
        return

    # Matching for "w" will cause errors because the ending 'iw' has 'w' as an
    # anubandha. So, match the wit-lakAras by name so we can exclude 'iw':
    la_wit = {"la~w", "li~w", "lu~w", "lf~w", "le~w", "lo~w"}
    if la.all(T.ATMANEPADA) and la.any(*la_wit):
        if la.all("li~w") and la.text in TAJHAYOH:
            op.upadesha("3.4.81", p, la, TAJHAYOH[la.text])
        elif la.text == "TAs":
            op.upadesha("3.4.80", p, la, "se")
        else:
            op.ti("3.4.79", p, la, "e")

    elif la.all("li~w") and la.all(T.PARASMAIPADA):
        op.upadesha("3.4.82", p, la, TIN_NAL_MAPPING[la.text])

    elif la.all("la~w") and la.all(T.PARASMAIPADA):
        if dhatu.u == "vida~" and la.text in TIN_PARA:
            op.optional(op.upadesha, "3.4.83", p, la, TIN_NAL_MAPPING[la.text])
        if dhatu.text == "brU" and la.text in TIN_PARA[:5]:
            if p.allow("3.4.84"):
                dhatu.text = "Ah"
                op.upadesha("3.4.84", p, la, TIN_NAL_MAPPING[la.text])
            else:
                p.decline("3.4.84")

    if la.all("lo~w"):
        if la.text == "si":
            la.u = la.text = "hi"
            la.remove_tags("p")
            p.step("3.4.87")

            if p.all(T.CHANDASI):
                op.optional(op.tag, "3.4.88", p, la, "p")

        elif la.text == "mi":
            op.text("3.4.89", p, la, "ni")
        elif la.antya == "i":
            op.antya("3.4.86", p, la, "u")
        elif la.antya == "e":
            last_two = la.text[-2:]

            if la.all(T.UTTAMA) and la.text.endswith("e"):
                op.antya("3.4.93", p, la, "E")

            elif last_two in ("se", "ve"):
                if last_two == "se":
                    la.text = la.text[:-2] + "sva"
                else:
                    la.text = la.text[:-2] + "vam"
                p.step("3.4.91")

            else:
                op.antya("3.4.90", p, la, "Am")

        if la.all("uttama"):
            # 3.4.92
            agama = Term.agama("Aw")
            # Add pit to the pratyaya, not the Agama.
            la.add_tags("p")
            p.terms.insert(-1, agama)
            p.step("3.4.92")
            it_samjna.run(p, -2)

    # TODO: 3.4.94 - 3.4.98

    # Switch used below.
    keep_nit = False

    # Must occur before 3.4.100 below
    _jher_jus(p, la)

    # Include lo~w by 3.4.85
    if la.any("lo~w") or f.is_nit_lakara(la):
        # 3.4.101
        tastha = ("tas", "Tas", "Ta", "mi")
        if la.text in tastha:
            la.text = op.yatha(la.text, tastha, ("tAm", "tam", "ta", "am"))
            p.step("3.4.101")

        if la.all(T.PARASMAIPADA):
            if la.all(T.UTTAMA) and la.antya == "s":
                op.antya("3.4.99", p, la, "")
            # lo~w excluded by existence of 3.4.86
            if la.text.endswith("i") and not la.all("lo~w"):
                op.antya("3.4.100", p, la, "")

    if la.all("li~N"):
        if la.all(T.PARASMAIPADA):
            # Add Nit to the pratyaya, not the Agama.
            p.terms.insert(-1, Term.agama("yAsu~w"))
            if p.all(T.ASHIH):
                # Add kit to the pratyaya, not the Agama.
                op.tag("3.4.104", p, la, "k")
            else:
                # Add Nit to the pratyaya, not the Agama.
                op.tag("3.4.103", p, la, "N")
                keep_nit = True

            it_samjna.run(p, -2)
        else:
            p.terms.insert(-1, Term.agama("sIyu~w"))
            p.step("3.4.102")
            it_samjna.run(p, -2)

            if la.u == "Ja":
                op.upadesha("3.4.105", p, la, "ran")
            elif la.u == "iw":
                op.upadesha("3.4.106", p, la, "a")

        if "t" in la.text or "T" in la.text:
            la.text = la.text.replace("t", "st").replace("T", "sT")
            p.step("3.4.107")

    # The 'S' of 'eS' is just for sarva-Adeza (1.1.55). If it is kept, it will
    # cause many problems when deriving li~T. So, remove it here.
    if la.u == "eS":
        la.tags.remove("S")
