"""
it_agama
~~~~~~~~
(7.2.8 - 7.2.78)

Various Sanskrit words have an "i" vowel inserted between the dhātu and the
pratyaya. This "i" is called *iṭ*. Roots use iṭ in one of three patterns:

- Roots that generally use iṭ are called *seṭ* (sa-iṭ).
- Roots that generally avoid iṭ are called *aniṭ* (an-iṭ).
- Roots that optionally use iṭ are called *veṭ* (vā-iṭ).

This prakaraṇa fully specifies the rules that add the iṭ-āgama to the prakriyā.

Order of operations:

- must run before `dvitva` for `undidizati`, etc.
- must run after `vikarana` since it checks for `sya`, `si~c`, etc.

"""

import padmini.filters as f
from padmini.sounds import s
from padmini.prakriya import Term, Prakriya
from padmini.constants import Tag as T
from padmini.term_views import TermView
from padmini import operations as op
from padmini.dhatu_gana import RADH_ADI
from .atmanepada import VRDBHYAH
from . import atidesha
from . import it_samjna


def eka_ac(t: Term) -> bool:
    num_vowels = sum(1 for L in t.text if L in s("ac"))
    # HACK to have ekac apply for am-Agama
    return num_vowels == 1 or "fa" in t.text


def optional_rule(rule: str, p: Prakriya):
    if p.allow(rule):
        return rule
    else:
        p.decline(rule)
        return None


def general_anit(p: Prakriya, index: int) -> bool:
    """General rules that prevent iT-Agama.

    (7.2.8 - 7.2.34)
    """
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return
    anit_rule = None

    if n.any(T.KRT) and n.adi in s("vaS"):
        anit_rule = "7.2.8"
    elif eka_ac(c) and (c.text == "Sri" or c.antya in s("uk")) and n.any("k"):
        anit_rule = "7.2.11"
    elif n.terms[0].u == "san" and c.text in {"Sri", "grah", "guh"}:
        anit_rule = "7.2.12"
    elif (c.text == "Svi" or c.any("I")) and n.any(T.NISTHA):
        anit_rule = "7.2.14"

    # TODO: 7.2.15
    elif c.any("A") and n.any(T.NISTHA):
        if p.all(T.BHAVE.T.KARMANI) and p.allow("7.2.17"):
            pass
        else:
            p.decline("7.2.17")
            anit_rule = "7.2.16"
    # TODO: 7.2.18 - 7.2.34

    if anit_rule:
        p.step(anit_rule)
        return True
    else:
        return False


def lit_it(p: Prakriya, index: int) -> bool:
    """iT rules specific to liT."""

    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    n.u = n.terms[0].u
    anit_rule = set_rule = None

    if not n.any("li~w"):
        return

    _7_2_10 = c.any(T.ANUDATTA) and eka_ac(c)

    # These rules are always aniT.
    if c.text in {"kf", "sf", "Bf", "vf", "stu", "dru", "sru", "Sru"}:
        anit_rule = "7.2.13"

    # Concise summary of rules:
    # - The roots in 7.2.13 are aniT. All others are seT in valAdi.
    # - However, there are the following exceptions for Tal:
    #   - roots ending in R (except R) are aniT.
    #   - roots ending in a vowel, or with a middle 'a', are veT.
    elif c.antya in s("ac") and n.u == "Tal" and _7_2_10:
        # 7.2.63 Rto bhAradvAjasya
        # In Bharadvaja's opinion, this applies only for final R. So for all
        # other roots, this condition is optional:
        if c.antya != "f":
            if p.allow("7.2.63"):
                set_rule = "7.2.63"
            else:
                p.decline("7.2.63")
                anit_rule = "7.2.61"
        # But for other anit roots, it is obligatory.
        else:
            if c.u == "f\\":
                set_rule = "7.2.66"
            else:
                anit_rule = "7.2.61"
    elif c.text in {"sfj", "dfS"} and n.u == "Tal":
        # By default, these will be seT. So the option allows aniT.
        code = "7.2.65"
        if p.allow(code):
            anit_rule = code
        else:
            p.decline(code)

    if n.any("li~w") and not (anit_rule or set_rule):
        # The effect of 7.2.13 is that all other roots are considerd `sew` by
        # default.
        p.step("7.2.13")
        if n.adi in s("val"):
            set_rule = "7.2.35"

    assert not (anit_rule and set_rule)
    if anit_rule:
        p.step(anit_rule)
    elif set_rule:
        op.insert_agama_after(set_rule, p, index, "iw")
    return True


def ardhadhatuke(p: Prakriya, index: int):
    """iT rules that condition on a following ArdhadhAtuka suffix.

    (7.2.35 - 7.2.36 and 7.2.41 - 7.2.75)
    """

    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    # HACK
    n.u = n.terms[0].u

    anit_rule = set_rule = None

    # Special cases
    if (c.antya == "f" or c.text == "han") and n.u == "sya":
        # Takes priority over 7.2.44 below.
        set_rule = "7.2.70"
    elif n.u == "si~c":
        if c.text == "aYj" and n.u == "si~c":
            set_rule = "7.2.71"

        para = p.terms[-1].all(T.PARASMAIPADA)
        if para:
            if c.u in {"zwu\\Y", "zu\\Y", "DUY"}:
                set_rule = "7.2.72"
            elif c.text in {"yam", "ram", "nam"}:
                c.text += "s"
                set_rule = "7.2.73"
            elif c.antya == "A":
                # Handle this after running Attva. See the run_after_attva
                # function for details.
                return

    elif c.text == "IS" and n.adi == "s":
        set_rule = "7.2.77"
        op.insert_agama_after(set_rule, p, index, "iw")
        p.step(set_rule)
        return

    elif c.text in {"IS", "Iq", "jan"} and (n.adi == "s" or n.terms[-1].u == "Dvam"):
        # See kAshika on 7.2.78 for inclusion of IS here.
        set_rule = "7.2.78"
        op.insert_agama_after(set_rule, p, index, "iw")
        p.step(set_rule)
        return

    if not n or not n.all(T.ARDHADHATUKA):
        return

    antya_para = p.terms[-1].all(T.PARASMAIPADA)
    krta_crta = {"kft", "cft", "Cfd", "tfd", "nft"}

    if set_rule or anit_rule:
        pass

    elif c.u in RADH_ADI and n.adi in s("val"):
        # All of these roots are in scope for 7.2.10 (aniT).
        # So, this option allows seT-tva.
        set_rule = optional_rule("7.2.45", p)

    elif c.u in {"izu~", "zaha~\\", "luBa~", "ruza~", "riza~"} and n.adi == "t":
        anit_rule = optional_rule("7.2.48", p)

    elif c.text in krta_crta and n.adi == "s" and n.u != "si~c":
        anit_rule = optional_rule("7.2.57", p)

    elif c.text == "gam" and antya_para and n.adi == "s":
        set_rule = "7.2.58"

    elif c.u in VRDBHYAH and c.gana == 1 and antya_para and n.adi == "s":
        anit_rule = "7.2.59"

    elif c.u == "kfpU~\\" and antya_para and (n.adi == "s" or n.u == "tAsi~"):
        anit_rule = "7.2.60"

    # TODO: not sure I undesrtand the scope of this rule.
    elif c.text in {"snu", "kram"} and n.adi in s("val"):
        if p.terms[-1].all(T.ATMANEPADA) and n.terms[0].u == "sIyu~w":
            anit_rule = "7.2.36"

    # Optional rules (Udit and others)

    if anit_rule or set_rule:
        pass
    elif n.adi in s("val"):
        if c.u in ("svf", "zUN", "DUY") or c.any("U"):
            # Synchronize choice of "it" with the choice of lun-vikarana.
            if p.all(T.F_ANIT_KSA):
                anit_rule = "7.2.44"
            elif p.all(T.F_SET_SIC):
                pass
            else:
                anit_rule = optional_rule("7.2.44", p)
        elif (n.any("li~N") or n.u == "si~c") and p.terms[-1].any(T.ATMANEPADA):
            vrt = c.text == "vf" or c.antya == "F"
            if vrt and n.any(T.ARDHADHATUKA):
                # By default, all of these roots are seT.
                # So, the option allows anit.
                anit_rule = optional_rule("7.2.42", p)
            elif c.antya == "f" and f.samyogadi(c):
                if c.all(T.ANUDATTA):
                    # For anit roots, optional seT.
                    set_rule = optional_rule("7.2.43", p)
                else:
                    # For seT roots, optional aniT.
                    anit_rule = optional_rule("7.2.43", p)

    # General cases

    if anit_rule or set_rule:
        pass
    # 7.2.10 is a niyama to the general rule, which applies only to
    # ArdhadhAtuka suffixes. So we add a check for ArdhadhAtukatva here.
    #
    # Any li~w root not explictly included in 7.2.13 is also iT.
    elif c.any(T.ANUDATTA) and eka_ac(c) and not n.any("li~w"):
        anit_rule = "7.2.10"
    elif n.adi in s("val") and n.any(T.ARDHADHATUKA):
        set_rule = "7.2.35"

    assert not (
        set_rule and anit_rule
    ), f"Both {set_rule} and {anit_rule} set -- bad state"

    if anit_rule:
        p.step(anit_rule)
        return True
    if set_rule:
        op.insert_agama_after(set_rule, p, index, "iw")
        return False


def sarvadhatuke(p: Prakriya, index: int):
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    if n.adi in s("val") and n.all(T.SARVADHATUKA):
        if c.u in ("rudi~r", "Yizva\\pa~", "Svasa~", "ana~", "jakza~"):
            # index+1 to skip vikarana
            # TODO: less hacky
            op.insert_agama_after("7.2.76", p, index + 1, "iw")
            return


def it_dirgha(p: Prakriya, c: Term, n: TermView):
    """Rules that lengthen the iṭ.

    (7.2.37 - 7.2.40)
    """

    it = n.terms[0]
    la = p.terms[-1]

    if not la.any("li~w"):
        if c.text == "grah":
            it.text = "I"
            p.step("7.2.37")
        elif c.antya == "F" or c.text == "vf":
            if la.any("li~N"):
                p.step("7.2.39")
            elif any(x.u == "si~c" for x in n.terms) and la.any(T.PARASMAIPADA):
                p.step("7.2.40")
            else:
                op.optional(op.text, "7.2.38", p, it, "I")


def run_for_index(p: Prakriya, index: int):
    c = p.terms[index]

    # Abhyasa might come second
    if not c.any(T.DHATU, T.ABHYASA):
        return

    found = lit_it(p, index)
    if found:
        return
    is_anit = general_anit(p, index)
    if is_anit:
        return
    is_anit = ardhadhatuke(p, index)
    if is_anit:
        return
    is_anit = sarvadhatuke(p, index)
    if is_anit:
        return

    n = TermView.make_pratyaya(p, index)
    if not n:
        return
    it = n.terms[0]
    if f.is_it_agama(it):
        it_dirgha(p, c, n)


def run_after_attva_for_index(p: Prakriya, index: int):
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n or not n.all(T.ARDHADHATUKA):
        return

    if n.terms[0].u == "si~c":
        para = p.terms[-1].all(T.PARASMAIPADA)
        if para:
            if c.antya == "A" and n.adi in s("val"):
                c.text += "s"
                op.insert_agama_after("7.2.73", p, index, "iw")


def run_before_attva(p: Prakriya):
    for index, _ in enumerate(p.terms):
        run_for_index(p, index)


def run_after_attva(p: Prakriya):
    for index, _ in enumerate(p.terms):
        run_after_attva_for_index(p, index)
