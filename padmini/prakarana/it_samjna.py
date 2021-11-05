"""
it_samjna
~~~~~~~~~
(1.3.2 - 1.3.9)

The most "core" prakaraṇa is the it-saṁjñā-prakaraṇa, which identifies remove
different `it` sounds from an upadeśa. Most derivations use this prakaraṇa at
least once.
"""

import re

from padmini.sounds import s
from padmini.prakriya import Prakriya, Term
from padmini.constants import Tag as T


def run_no_index(p: Prakriya, u: Term):
    """Extract its."""

    ac = s("ac")
    hal = s("hal")
    tusma = s("tu~ s m")
    cutu = s("cu~ wu~")
    lashaku = s("l S ku~")

    # it-prakarana runs only for upadeshas. If not an upadesha, skip.
    if u.u != u.text:
        return

    raw = text = u.u
    its = set()

    # Varttika
    irit = False
    if text.endswith("i~r"):
        text = text[:-3]
        its.add("ir")
        irit = True
    elif text.endswith("i~^r"):
        text = text[:-4]
        its.add("ir")
        its.add(T.SVARITET)
        irit = True

    # include anudAttet / svaritet
    s_ac = "".join(ac.items)
    splits = re.split(f"([{s_ac}]~[\\\\^]?)", text)
    if len(splits) > 1:
        text = "".join(splits[::2])

        # Add its
        it_groups = splits[1::2]
        if any("\\" in it for it in it_groups):
            its.add(T.ANUDATTET)
        if any("^" in it for it in it_groups):
            its.add(T.SVARITET)
        for it in splits[1::2]:
            it = re.sub(r"[\\^~]", "", it)
            its.add(it)
        p.step("1.3.2")

    # Also handle general udatta/svarita
    if "\\" in text:
        its.add(T.ANUDATTA)
    if "^" in text:
        its.add(T.SVARITA)
    text = re.sub(r"[\\^~]", "", text)

    vibhaktau_tusmah = u.all(T.VIBHAKTI) and raw[-1] in tusma
    if raw[-1] in hal and not vibhaktau_tusmah and not irit:
        its.add(raw[-1])
        text = text[:-1]
        p.step("1.3.4")

    if raw[:2] in ("Yi", "wu", "qu"):
        its.add(raw[:2])
        text = text[2:]
        p.step("1.3.5")

    # `elif` because 1.3.5 can't apply at the same time as the rules below.
    elif u.all(T.PRATYAYA):
        if raw[0] == "z":
            its.add(raw[0])
            text = text[1:]
            p.step("1.3.6")

        elif raw[0] in cutu:
            # CJWQ are replaced later in the grammar.
            # If we substitute them now, those rules will become vyartha.
            if raw[0] not in "CJWQ":
                its.add(raw[0])
                text = text[1:]
                p.step("1.3.7")

        elif not u.any(T.TADDHITA) and raw[0] in lashaku:
            # Keep the first "l" of the lakAras.
            # Otherwise, rule 3.4.77 will become vyartha.
            LAKARA = {
                "la~w",
                "li~w",
                "lu~w",
                "lf~w",
                "le~w",
                "lo~w",
                "la~N",
                "li~N",
                "lu~N",
                "lf~N",
            }
            if raw not in LAKARA:
                its.add(raw[0])
                text = text[1:]
                p.step("1.3.8")

    u.text = text
    u.add_tags(*its)
    if text != raw:
        p.step("1.3.9")


def run(p: Prakriya, index: int):
    run_no_index(p, p.terms[index])
