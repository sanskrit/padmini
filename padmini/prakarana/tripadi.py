"""
tripadi
~~~~~~~
(8.2.1 - end of 8.4)

The final three pādas of the Ashtadhyayi are called the **tripādi**. The tripādi
generally contains sandhi rules and other miscellaneous sound change rules.

The tripādi uses a different rule selection mechanism from the rest of the
Ashtadhyayi: whereas the rest of the text selects rules based on their priority
and allows a rule to apply if it has scope, the tripādi applies rules in order
and will never "go back" to apply an earlier rule.
"""

import re
from typing import Optional

from padmini.term_views import StringView, TermView
from padmini.sounds import s
from padmini import filters as f
from padmini import operations as op
from padmini import sounds
from .utils import per_term
from padmini.prakriya import Prakriya, VyakaranaException
from padmini.constants import Tag as T

ADESHA_CACHE = {}


def al_adesha(
    rule: str,
    p: Prakriya,
    index: int,
    tasmat: Optional[str],
    tasya: str,
    tasmin: str,
    sthani: str,
):
    """Apply letter substitution rules at term boundaries.

    :param rule: the rule ID
    :param p: the prakriya
    :param index: the index to apply the rule to
    :param tasmat: term before
    :param tasya: term replaced
    :param tasmin: term after
    :param sthana: replacement
    """
    if rule in ADESHA_CACHE:
        func = ADESHA_CACHE[rule]
        return func(p, index)

    assert tasya
    assert sthani

    def sound_pattern(expression):
        if expression:
            return s(expression).regex
        else:
            return ""

    re_tasmat = sound_pattern(tasmat)
    re_tasya = sound_pattern(tasya)
    re_tasmin = sound_pattern(tasmin)
    mapping = sounds.map_sounds(s(tasya), s(sthani))

    def adesha(p, index):
        c = p.terms[index]
        next_text = "".join(x.text for x in p.terms[index + 1 :])

        pattern = f"({re_tasmat})({re_tasya})({re_tasmin})"

        for match in re.finditer(pattern, c.text + next_text):
            prefix = c.text[: match.start(2)]
            sthana = match.group(2)
            sthani = mapping[sthana]
            if prefix != c.text and sthana != sthani:
                suffix = c.text[match.start(2) + 1 :]
                result = prefix + sthani + suffix
                c.text = result
                p.step(rule)

    adesha(p, index)
    ADESHA_CACHE[rule] = adesha
    return adesha


def na_lopa(p: Prakriya):
    sup = p.terms[-1]
    if not sup.any(T.SUP):
        return
    anga = p.terms[-2]

    if anga.antya == "n" and anga.any(T.PRATIPADIKA) and not sup.text:
        op.antya("8.2.7", p, anga, "")


def ra_to_la(p: Prakriya):
    """Change of r to l. (8.2.18 - 8.2.20)"""
    for c, n in per_term(p):
        if not n:
            continue
        # HACK to exclude kfpa (cur-gana root)
        if c.u.startswith("kfp") and c.u != "kfpa":
            c.text = c.text.replace("f", "x").replace("r", "l")
            p.step("8.2.18")
        elif c.u == "gF" and n.u == "yaN":
            c.text = c.text.replace("r", "l")
            p.step("8.2.20")
        # TODO: where is it specified that this is only for gF/girati?
        elif c.u == "gF" and c.gana == 6 and n.adi in s("ac"):
            res = c.text.replace("r", "l")
            op.optional(op.text, "8.2.21", p, c, res)


def samyoganta_and_salopa(p: Prakriya):
    """Final samyoga. (8.2.23 - 8.2.29)"""

    # Exception to 8.2.23.
    sk = s("s k").regex
    hal = s("hal").regex
    jhal = s("Jal").regex

    # TODO: jhal case
    pattern = f"({sk}+){hal}+"
    jhal = f"{jhal}"

    # jhalo jhali
    view = StringView(p.terms)
    lopa_offset = 0
    for match in re.finditer(f"{jhal}(s){jhal}", view.text):
        start, end = match.span(1)
        view.delete_span(start - lopa_offset, end - lopa_offset)
        p.step("8.2.26")

    # saMst can be handled only with difficulty. For details, see the
    # commentary in the mAdhavIya-dhAtuvRtti:
    #
    # https://archive.org/details/237131938MadhaviyaDhatuVrtti/page/n434/mode/1up
    view = StringView(p.terms)
    vtext = view.text
    # We find all matches at the beginning of the loop. If multiple sa-lopas
    # apply, then each lopa will cause a frame shift that will affect later
    # sa-lopas. As a quick hack, manage this with `offset` so that the deletion
    # indices are always properly aligned.
    lopa_offset = 0
    for match in re.finditer(pattern + f"({jhal}|$)", vtext):
        can_apply = True
        if "sanst" in vtext:
            # Apply the rule only if the change would not affect "sanst."
            offset = 0
            for t in p.terms:
                offset += len(t.text)
                if t.text == "sanst":
                    break
            if match.span(1)[0] <= offset:
                # rule would apply to "sanst" -- block.
                can_apply = False
        if can_apply:
            start, end = match.span(1)
            view.delete_span(start - lopa_offset, end - lopa_offset)
            p.step("8.2.29")
            lopa_offset += 1

    for c, n in per_term(p):
        if not n:
            continue
        if c.antya == "r" and n.text == "s" and n is p.terms[-1]:
            op.adi("8.2.24", p, n, "")
        # Per kAzikA, applies only to s of si~c. But this seems to cause
        # problems e.g. for tAs + Dve.
        elif c.antya == "s" and n.adi == "D":
            op.antya("8.2.25", p, c, "")

    # hrasvAd aGgAt
    for i, c in enumerate(p.terms):
        try:
            n = p.terms[i + 1]
            n2 = p.terms[i + 2]
        except IndexError:
            break
        if (
            c.antya in sounds.HRASVA
            and n.text == "s"
            and n2.adi in s("Jal")
            and not c.any(T.AGAMA)
        ):
            op.lopa("8.2.27", p, n)

    for i, _ in enumerate(p.terms[:-2]):
        x, y, z = p.terms[i : i + 3]
        if x.u == "iw" and y.u == "si~c" and z.u == "Iw":
            op.lopa("8.2.28", p, y)

            # sic-lopa is siddha with respect to prior rules (8.2.3 vArttika)
            z.text = ""
            # HACK: x should always have text at this point. Temp workaround.
            if x.text:
                op.antya("6.1.101", p, x, "I")

    while f.samyoganta(view):
        last = len(view.text) - 1
        view[last] = ""
        p.step("8.2.23")


def ha_adesha(p: Prakriya):
    for index, (c, n) in enumerate(per_term(p)):
        is_dhatu = c.all(T.DHATU)
        # TODO: implement padAnta
        # By a vArttika, this applies only at term boundaries.
        druha_muha = {"dru\\ha~", "mu\\ha~", "zRu\\ha~", "zRi\\ha~"}
        if is_dhatu and c.u in druha_muha:
            op.optional(al_adesha, "8.2.33", p, index, None, "h", "Jal", "G")
        elif is_dhatu and c.u == "Ra\\ha~^" and c.antya == "h":
            al_adesha("8.2.34", p, index, None, "h", "Jal", "D")
        elif is_dhatu and c.text == "Ah":
            al_adesha("8.2.35", p, index, None, "h", "Jal", "T")
        elif is_dhatu and c.adi == "d":
            al_adesha("8.2.32", p, index, None, "h", "Jal", "G")

        al_adesha("8.2.31", p, index, None, "h", "Jal", "Q")
        if c.antya == "h" and not n:
            op.antya("8.2.31", p, c, "Q")


def per_term_1b(p: Prakriya, index: int):
    c = p.terms[index]
    try:
        n = [u for u in p.terms[index + 1 :] if u.text][0]
    except IndexError:
        n = None

    vrascha = {
        "o~vrascU~",
        "Bra\\sja~^",
        "sf\\ja~\\",
        "sf\\ja~",
        "mfjU~",
        "ya\\ja~^",
        "rAj",
        "BrAjf~\\",
    }

    jhali_ante = not n or n.adi in s("Jal")
    if (c.u in vrascha or c.antya in s("C S")) and jhali_ante:
        if c.text.endswith("tC"):
            # TODO: seems implied, not sure.
            c.text = c.text[:-2] + "z"
            p.step("8.2.36")
        else:
            op.antya("8.2.36", p, c, "z")

    if c.antya in s("cu~") and (not n or n.adi in s("Jal")):
        mapping = sounds.map_sounds(s("cu~"), s("ku~"))
        op.antya("8.2.30", p, c, mapping[c.antya])

    sdhvoh = n and (n.adi == "s" or n.all(T.PRATYAYA) and n.u.startswith("Dv"))
    basho_bhash = sounds.map_sounds_s("baS", "Baz")
    if c.adi in basho_bhash and c.antya in s("JaS") and sdhvoh:
        op.adi("8.2.37", p, c, basho_bhash[c.adi])

    # Exclude the following from 8.2.39 so that the corresponding rules aren't
    # vyartha:
    # - c for 8.2.30 (coH kuH)
    # - S for 8.2.36 (vraSca-Brasja-...-Ca-SAM zaH)
    # - s for 8.2.66 (sasajuSo ruH)
    # - h for 8.2.31 (ho QaH)
    if c.antya in s("Jal") and c.antya not in s("c S s h") and not n:
        mapping = sounds.map_sounds(s("Jal"), s("jaS"))
        op.antya("8.2.39", p, c, mapping[c.antya])

    if c.all(T.DHATU) and c.u != "quDA\\Y":
        # TODO: abhyasa
        if c.antya in s("Jaz") and n and n.adi in s("t T"):
            op.adi("8.2.40", p, n, "D")

    if c.antya in s("z Q") and n.adi == "s":
        op.antya("8.2.41", p, c, "k")

    if c.any(T.DHATU) and c.antya == "m" and n.adi in {"m", "v"}:
        op.antya("8.2.65", p, c, "n")

    # TODO: sajuS

    try:
        rn = p.terms[index + 1]
    except IndexError:
        rn = None
    next_is_last = index + 1 == len(p.terms) - 1
    if c.antya == "s" and next_is_last and rn.text == "" and rn.u == "tip":
        # Exception to general rule 8.2.66 below
        op.antya("8.2.73", p, c, "d")

    elif c.antya == "s" and (not n or (next_is_last and rn.text == "")):
        op.antya("8.2.66", p, c, "ru~")

    if c.antya in s("s d") and rn and rn.text == "" and rn.u == "sip":
        if c.antya == "s":
            op.optional(op.antya, "8.2.74", p, c, "ru~")
        else:
            op.optional(op.antya, "8.2.75", p, c, "ru~")

    # 8.2.77
    # TODO: sajuS
    if c.all(T.DHATU):
        # TODO: bha
        if c.text in ("kur", "Cur"):
            # Do nothing.
            p.step("8.2.79")
        elif c.antya in s("r v"):
            if c.upadha in {"i", "u", "f", "x"}:
                if n and n.adi in s("hal"):
                    op.upadha("8.2.77", p, c, sounds.dirgha(c.upadha))
                elif not n:
                    op.upadha("8.2.76", p, c, sounds.dirgha(c.upadha))
        if (
            len(c.text) >= 3
            and c.text[-3] in s("ik")
            and c.upadha in "rv"
            and c.antya in s("hal")
        ):
            c.text = c.text[:-3] + sounds.dirgha(c.text[-3]) + c.text[-2:]
            p.step("8.2.78")

    # 8.3.15
    # TODO: next pada
    has_ru = c.text.endswith("ru~") or c.text.endswith("r")
    if has_ru and not n:
        c.text = c.text.replace("ru~", "H")
        if c.text.endswith("r"):
            c.text = c.text[:-1] + "H"
        p.step("8.3.15")


def natva(p: Prakriya):
    """Rules that change `n` to `R`. (8.4.1 - 8.4.39)

    :param p: the prakriya
    """
    i, u = p.find_first(T.DHATU)
    if u and (
        (u.u == "kzuBa~" and p.terms[i + 1].u in {"SnA", "SAnac"})
        or (u.u == "tfpa~" and p.terms[i + 1].u == "Snu")
    ):
        p.step("8.4.39")
        return

    # TODO: AG and num
    view = StringView(p.terms)
    between = s("aw ku~ pu~ M").regex
    match = re.search(f"[rzfF]({between}*)n", view.text)

    if match:
        # End of pada
        if match.span(0)[1] == len(view.text):
            p.step("8.4.37")
        else:
            view[match.span(0)[1] - 1] = "R"
            if match.group(1):
                p.step("8.4.2")
            else:
                trigger = view[match.span(0)[0]]
                if trigger in "rz":
                    p.step("8.4.1")
                else:
                    p.step("8.4.1-v")


def stoh_scuna_stuna(p):
    view = StringView(p.terms)
    scu = s("S cu~")
    swu = s("z wu~")
    stu = s("s tu~")
    match = re.search(f"({stu.regex})({scu.regex})", view.text)
    if match:
        first, second = match.group(1), match.group(2)
        if first in s("tu~") and second == "z":
            p.step("8.4.43")
        else:
            mapping = dict(zip(stu.items, scu.items))
            view[match.span(0)[0]] = mapping[first]
            p.step("8.4.40")

    match = re.search(f"({scu.regex})({stu.regex})", view.text)
    if match:
        first, second = match.group(1), match.group(2)
        if first == "S":
            p.step("8.4.44")
        else:
            mapping = dict(zip(stu.items, scu.items))
            view[match.span(0)[0] + 1] = mapping[second]
            p.step("8.4.40")

    match = re.search(f"({stu.regex}){swu.regex}", view.text)
    if match:
        res = match.group(1)
        mapping = dict(zip(stu.items, swu.items))
        view[match.span(0)[0]] = mapping[res]
        p.step("8.4.41")
    match = re.search(f"({swu.regex})({stu.regex})", view.text)
    if match:
        res = match.group(2)
        mapping = dict(zip(stu.items, swu.items))
        view[match.span(0)[0] + 1] = mapping[res]
        p.step("8.4.41")


def murdhanya(p: Prakriya):
    """mUrdhanya when preceded by certain sounds.

    (8.3.55 - 8.3.119)
    """
    for i, (c, n) in enumerate(per_term(p)):
        if not n:
            continue
        inku = s("iR2 ku~")
        # HACK: don't include agama
        adesha_pratyaya = n.any(T.PRATYAYA, T.F_ADESHA_ADI, T.AGAMA)
        apadanta = not (n.text == s and n is p.terms[-1])
        if c.antya in inku and n.adi == "s" and adesha_pratyaya and apadanta:
            op.adi("8.3.59", p, n, "z")

        elif c.u in {"va\\sa~", "SAsu~", "Gasx~"} and c.upadha in inku:
            op.antya("8.3.60", p, c, "z")

        # HACK
        for i, u in enumerate(p.terms):
            if c is u:
                break
        n = TermView.make_pratyaya(p, i)
        if not n:
            continue

        if (
            c.antya in s("iR2")
            and not c.any(T.AGAMA)
            and (n.any("lu~N", "li~w") or n.all(T.ARDHADHATUKA, "li~N"))
        ):
            last = n.terms[-1]
            if not (last.adi == "D" or n.text.endswith("zIDvam")):
                continue

            do = True
            if f.is_it_agama(n.terms[0]):
                code = "8.3.79"
                if p.allow(code):
                    p.step(code)
                else:
                    do = False
                    p.decline(code)

            if do:
                last.text = last.text.replace("D", "Q")
                p.step("8.3.78")


def overall_1(p: Prakriya):
    """Rules that apply to the overall prakriya."""

    view = StringView(p.terms)

    # 8.3.24
    # TODO: next term
    # TODO: a-padAnta
    jhal = s("Jal").regex
    for match in re.finditer(f"([mn])({jhal})", view.text):
        view[match.span(1)[0]] = "M"
        p.step("8.3.24")


def dha(p: Prakriya):
    """Rules for retroflex Dha."""
    view = StringView(p.terms)
    # Save the text before Dha-lopa for a cleaner comparison below.
    vtext = view.text

    # Placed after 8.4.41, otherwise this is vyartha
    match = re.search(f"([Q])[Q]", view.text)
    if match:
        view[match.span(0)[0]] = ""
        p.step("8.3.13")

        # Placed here, otherwise this is vyartha
        # matches aN (no f, x)
        match = re.search(f"([aAiIuU])[Q]", view.text)
        if match:
            # HACK to check for sah and vah
            if "saQ" in vtext or "sAQ" in vtext or "vaQ" in vtext or "vAQ" in vtext:
                view[match.span(0)[0]] = "o"
                p.step("6.3.112")
            else:
                res = match.group(1)
                view[match.span(0)[0]] = sounds.dirgha(res)
                p.step("6.3.111")


def savarna(p):
    """Rules dealing with savarna letters."""

    view = StringView(p.terms)
    vtext = view.text
    yay = s("yay").regex
    for match in re.finditer(f"(M)({yay})", vtext):
        anusvara_index = match.span(1)[0]
        para = match.group(2)

        replacement = None
        if para in s("ku~"):
            replacement = "N"
        elif para in s("cu~"):
            replacement = "Y"
        elif para in s("wu~"):
            replacement = "R"
        elif para in s("tu~"):
            replacement = "n"
        elif para in s("pu~"):
            replacement = "m"
        else:
            raise VyakaranaException(f"Unknown following sound {para}.")
        view[anusvara_index] = replacement
        p.step("8.4.58")

    hal = s("hal").regex
    yam = s("yam").regex
    jhar = s("Jar").regex

    view = StringView(p.terms)
    match = re.search(f"{hal}({yam})({yam})", view.text)
    if match:
        c = match.group(1)
        n = match.group(2)
        if c == n:
            if p.allow("8.4.64"):
                view.delete_span(*match.span(1))
            else:
                p.decline("8.4.64")

    view = StringView(p.terms)
    match = re.search(f"{hal}({jhar})({jhar})", view.text)
    if match:
        c = match.group(1)
        n = match.group(2)
        if n in sounds.savarna(c):
            if p.allow("8.4.65"):
                view.delete_span(*match.span(1))
            else:
                p.decline("8.4.65")


def per_term_2(p: Prakriya, index: int):
    try:
        n = [u for u in p.terms[index + 1 :] if u.text][0]
    except IndexError:
        n = None

    c = p.terms[index]

    al_adesha("8.4.53", p, index, None, "Jal", "JaS", "jaS")
    if c.all(T.ABHYASA):
        al_adesha("8.4.54", p, index, None, "Jal", None, "jaS car")

    # 8.2.38, but indicated here by use of "dadhas" in the rule.
    sdhvoh = n and (n.adi == "s" or n.all(T.PRATYAYA) and n.u.startswith("Dv"))
    if c.u == "quDA\\Y" and c.text == "D" and (n.adi in s("t T") or sdhvoh):
        prev = p.terms[index - 1]
        prev.text = "Da"
        c.text = "d"
        p.step("8.2.38")

    al_adesha("8.4.55", p, index, None, "Jal", "Kar", "car")

    if c.antya in s("Jal") and not n:
        mapping = sounds.map_sounds(s("Jal"), s("car"))
        op.optional(op.antya, "8.4.56", p, c, mapping[c.antya])


def run(p: Prakriya):
    na_lopa(p)
    ra_to_la(p)
    samyoganta_and_salopa(p)
    ha_adesha(p)

    for i, _ in enumerate(p.terms):
        per_term_1b(p, i)

    murdhanya(p)
    overall_1(p)

    natva(p)
    stoh_scuna_stuna(p)
    dha(p)

    for i, _ in enumerate(p.terms):
        per_term_2(p, i)

    savarna(p)
