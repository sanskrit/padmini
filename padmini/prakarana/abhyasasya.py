"""
abhyasasya
~~~~~~~~~~
 (7.4.58 - end of 7.4)

Rules that modify the abhyāsa.
"""


from padmini import filters as f
from padmini import operations as op
from padmini import sounds
from padmini.constants import Tag as T
from padmini.prakriya import Prakriya, Term, VyakaranaException
from padmini.sounds import s

from .sanadyanta import MAN_BADHA


def _has_following_san(p: Prakriya, needle: Term) -> bool:
    seen_needle = False
    for t in p.terms:
        if needle is t:
            seen_needle = True
            continue
        if seen_needle:
            if t.u == "san":
                return True
            elif not t.any(T.DHATU, T.AGAMA):
                return False
            else:
                continue
    return False


def haladi(text: str) -> str:
    """Simplifies the abhyasa per 7.4.60."""
    buf = []
    for i, L in enumerate(text):
        if L in s("hal"):
            if i == 0:
                buf.append(L)
        else:
            buf.append(L)
            return "".join(buf)
    raise VyakaranaException(f"abhyasa without vowel: {text}")


def sharpurva(text: str) -> str:
    """Simplifies the abhyasa per 7.4.61."""
    buf = []
    found = False
    for i, L in enumerate(text):
        if i == 0:
            assert L in s("Sar")
        elif L in s("Kay"):
            buf.append(L)
        elif L in s("ac"):
            buf.append(L)
            return "".join(buf)
    raise VyakaranaException(f"abhyasa without vowel: {text}")


def run_for_each(p: Prakriya, c: Term, dhatu: Term):
    """Rules that modify the abhyasa."""
    la = p.terms[-1]

    # TODO: svAp
    if dhatu.text == "dyut":
        op.text("7.4.67", p, c, "dit")
    if dhatu.text == "vyaT" and la.any("li~w"):
        op.text("7.4.68", p, c, "viT")

    if c.adi in s("Sar") and c.text[1] in s("Kay"):
        res = sharpurva(c.text)
        if res != c.text:
            op.text("7.4.61", p, c, res)
    else:
        res = haladi(c.text)
        if res != c.text:
            op.text("7.4.60", p, c, res)

    kuhozcu = sounds.map_sounds(s("ku~ h"), s("cu~"))
    if c.adi in kuhozcu:
        op.adi("7.4.62", p, c, kuhozcu[c.adi])
    if c.antya in sounds.DIRGHA:
        op.antya("7.4.59", p, c, sounds.hrasva(c.antya))
    if c.antya == "f":
        op.antya("7.4.66", p, c, "a")

    if dhatu.u == "i\\R" and la.any("k"):
        op.adi("7.4.69", p, c, "I")

    # liT changes (7.4.70 - 7.4.74)
    if la.all("li~w"):
        if c.text == "a":
            op.text("7.4.70", p, c, "A")
            # From the Kashika-vrtti:
            #
            #     ṛkāraikadeśo repho halgrahaṇena gṛhyate, tena iha api dvihalo
            #     'ṅgasya nuḍāgamo bhavati. ānṛdhatuḥ, ānṛdhuḥ.
            #
            #
            if dhatu.antya in s("hal") and dhatu.upadha in s("f hal"):
                # 'A' acepted only by some grammarians
                if dhatu.adi == "A":
                    op.optional(op.insert_agama_after_by_term, "7.4.71", p, c, "nu~w")
                else:
                    op.insert_agama_after_by_term("7.4.71", p, c, "nu~w")
            # For aSnoti only, not aSnAti
            elif dhatu.text == "aS" and dhatu.gana == 5:
                op.insert_agama_after_by_term("7.4.72", p, c, "nu~w")
        # 2 is for as -> bhU
        elif dhatu.text == "BU" and dhatu.gana in (1, 2):
            op.text("7.4.73", p, c, "ba")
        # TODO: 7.4.74

    # Slu changes
    if p.find(lambda x: x.all(T.SLU)):
        if dhatu.text in ("nij", "vij", "viz"):
            op.antya("7.4.75", p, c, sounds.guna(c.antya))
        elif dhatu.u in ("quBf\\Y", "mA\\N", "o~hA\\N"):
            op.antya("7.4.76", p, c, "i")
        elif dhatu.text in ("f", "pf", "pF"):
            op.antya("7.4.77", p, c, "i")
        # TODO: 7.4.78


def run_sani_cani_for_each(p: Prakriya, c: Term, dhatu: Term):
    # san and sanvat changes
    abhyasta_index, _ = p.find_last(T.ABHYASTA)
    laghu_cani = (
        # caN-pare
        p.terms[abhyasta_index].u in ("Ric", "RiN")
        and p.find(lambda x: x.u == "caN")
        # laghuni
        and f.is_laghu(dhatu)
        # an-ak-lope
        and not dhatu.any(T.F_AT_LOPA)
    )

    sanvat = laghu_cani or _has_following_san(p, c)
    if sanvat:
        if laghu_cani and dhatu.text in {
            "smf",
            "dF",
            "tvar",
            "praT",
            "mrad",
            "stF",
            "spaS",
        }:
            op.antya("7.4.95", p, c, "a")
            return

        elif c.antya == "a":
            op.antya("7.4.79", p, c, "i")
        elif (
            dhatu.adi in s("pu~ yaR j")
            and len(dhatu.text) >= 2
            and dhatu.text[1] == "a"
        ):
            op.antya("7.4.80", p, c, "i")
        # TODO: 7.4.81

    # TODO: 7.4.95
    if laghu_cani:
        if not f.samyogadi(dhatu):
            op.antya("7.4.94", p, c, sounds.dirgha(c.antya))

    # TODO: scope of this? Sarvadhatuka only?
    if dhatu.u in MAN_BADHA:
        op.antya("3.1.6", p, c, sounds.dirgha(c.antya))


def run(p: Prakriya):
    for i, t in enumerate(p.terms):
        if not t.any(T.ABHYASA):
            continue

        dhatu = p.terms[i + 1]
        run_for_each(p, t, dhatu)


def run_sani_cani(p: Prakriya):
    for i, t in enumerate(p.terms):
        if not t.any(T.ABHYASA):
            continue

        dhatu = p.terms[i + 1]
        run_sani_cani_for_each(p, t, dhatu)
