"""
ac_sandhi
~~~~~~~~~
(6.1.66 - 6.1.101)
"""

import re

from padmini import operations as op, sounds
from padmini.sounds import s
from padmini.prakriya import Prakriya
from padmini.constants import Tag as T
from padmini.term_views import StringView


def sup_sandhi_before_angasya(p: Prakriya):
    n = p.terms[-1]
    if not n.all(T.SUP):
        return
    c = p.terms[-2]

    if c.antya == "o" and n.u in {"am", "Sas"}:
        n.text = n.text[1:]
        op.antya("6.1.93", p, c, "A")


def find_all_matches(pattern: str, view):
    """Used because `view` might be mutated per match."""
    match = re.search(pattern, view.text)
    i = 0
    while match:
        yield match

        # Yield another only if it progresses.
        j = match.span(0)[0]
        if i != j:
            i = j
            match = re.search(pattern, view.text)
        else:
            return


def general_vowel_sandhi(p: Prakriya, terms=None):
    """

    :param terms: optional. Used as a hack to apply ac-sandhi before Ni-lopa
    without also modifying Ni.
    """
    view = StringView(terms or p.terms)
    match = re.search("([a])([aeo])", view.text)
    while match:
        view[match.span(0)[0]] = ""
        p.step("6.1.97")
        match = re.search("([a])([aeo])", view.text)

    a = s("a").regex
    ac = s("ac").regex
    ak = s("ak").regex
    ec = s("ec").regex
    ic = s("ic").regex
    ik = s("ik").regex
    for match in find_all_matches(f"({ec})({ac})", view):
        mapping = dict(zip(s("ec").items, ("ay", "av", "Ay", "Av")))
        view[match.span(0)[0]] = mapping[match.group(1)]
        p.step("6.1.78")

    match = re.search(f"({ak})({ak})", view.text)
    while match:
        first = match.group(1)
        second = match.group(2)
        if second in sounds.savarna(first):
            view[match.span(0)[0]] = ""
            view[match.span(1)[0]] = sounds.dirgha(first)
            p.step("6.1.101")

        # Loop but avoid infinite loop, which is possible here due to the
        # savarna check.
        old_start = match.span(0)[0]
        match = re.search(f"({ak})({ak})", view.text)
        if match and match.span(0)[0] == old_start:
            break

    for match in find_all_matches(f"({ik})({ac})", view):
        mapping = dict(zip("iIuUfFxX", "yyvvrrll"))
        view[match.span(0)[0]] = mapping[match.group(1)]
        p.step("6.1.77")

    match = re.search(f"({a})({ic})", view.text)
    while match:
        first = match.group(1)
        second = match.group(2)
        if second in s("ec"):
            view[match.span(0)[0]] = sounds.vrddhi(second)
            view[match.span(0)[1] - 1] = ""
            p.step("6.1.88")
        else:
            # HACK for trnah
            term = view.term_for_index(match.span(0)[0])
            if term.text == "tfnaih":
                op.text("6.1.87", p, term, "tfneh")
            else:
                view[match.span(0)[0]] = sounds.guna(second)
                view[match.span(0)[1] - 1] = ""
                p.step("6.1.87")
        match = re.search(f"({a})({ic})", view.text)


def sup_sandhi_after_angasya(p: Prakriya):
    # Program cannot model "antAdivacca" so split the rule.
    n = p.terms[-1]
    if not n.all(T.SUP):
        return
    c = p.terms[-2]

    if c.antya in s("ak") and n.any(T.V1, T.V2):
        if n.text == "am":
            op.adi("6.1.107", p, n, "")
        elif c.antya in s("a") and n.adi in s("ic"):
            p.step("6.1.104")
        elif c.antya in sounds.DIRGHA and (n.adi in s("ic") or n.u == "jas"):
            p.step("6.1.105")
        elif n.adi in s("ac"):
            antya = c.antya
            c.text = c.text[:-1]
            op.adi("6.1.102", p, n, sounds.dirgha(antya))

            if n.u == "Sas" and c.all(T.PUM):
                op.antya("6.1.103", p, n, "n")

    elif n.u in {"Nasi~", "Nas"}:
        if c.antya in s("eN"):
            op.adi("6.1.110", p, n, "")
        elif c.antya == "f":
            c.text = c.text[:-1] + "ur"
            op.adi("6.1.110", p, n, "")


def run_for_term(p: Prakriya, index: int):
    terms = p.terms
    c = terms[index]

    # Ignore this case if it starts an upadesha, otherwise roots like "vraj"
    # would by vyartha. Likewise for roots ending with 'v'
    # TODO: handle term boundaries more elegantly
    val = s("val")
    s_val = "".join(val.items)
    re_vyor_vali = f"[vy]([{s_val}])"
    if re.search(re_vyor_vali, c.text) and not c.all(T.DHATU):
        c.text = re.sub(re_vyor_vali, r"\1", c.text)
        p.step("6.1.66")

    try:
        n = [u for u in terms[index + 1 :] if u.text][0]
    except IndexError:
        return

    if c.antya in s("v y") and n.adi in val and not c.all(T.DHATU):
        op.antya("6.1.66", p, c, "")

    # TODO: NI, Ap
    # Check for Agama to avoid lopa on yAs + t.
    if (
        c.antya in s("hal")
        and n
        and len(n.text) == 1
        and n.u in ("su~", "tip", "sip")
        and not c.all(T.AGAMA)
    ):
        op.antya("6.1.68", p, n, "")

    if (c.antya in sounds.HRASVA or c.antya in s("eN")) and p.terms[-1].any(
        T.SAMBUDDHI
    ):
        op.lopa("6.1.69", p, p.terms[-1])

    if c.antya in s("a") and n.text == "us":
        op.antya("6.1.96", p, c, "")

    # ekaH pUrvapara (6.1.84)

    elif c.u == "Aw" and n.adi in s("ik"):
        c.text = ""
        op.adi("6.1.90", p, n, sounds.vrddhi(n.adi))


def run_common(p: Prakriya):
    for i, _ in enumerate(p.terms):
        run_for_term(p, i)

    general_vowel_sandhi(p)

    for i, c in enumerate(p.terms):
        try:
            n = p.terms[i + 1]
        except IndexError:
            continue
        # HACK: duplicate 6.4.92 from the asiddhavat section for ci -> cAy, cap
        if c.all("m") and n.u in {"Ric", "pu~k"} and c.text in {"cAy", "cA"}:
            if c.text == "cA":
                op.antya("6.4.92", p, c, "a")
            else:
                op.upadha("6.4.92", p, c, "a")


def run(p: Prakriya):
    sup_sandhi_before_angasya(p)
    sup_sandhi_after_angasya(p)
    run_common(p)
