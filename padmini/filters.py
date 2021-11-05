from padmini.constants import Tag as T
from .prakriya import Term
from .sounds import s, HRASVA


def samyoganta(t: Term) -> bool:
    """``True`` iff `t` ends in multiple consonants."""
    try:
        x, y = t.text[-2:]
        # HACK: check for final C without tug-agama
        if y == "C":
            return True
        return x in s("hal") and y in s("hal")
    except ValueError:
        return False


def samyogadi(t: Term) -> bool:
    """``True`` iff `t` starts with multiple consonants."""
    try:
        x, y = t.text[:2]
        return x in s("hal") and y in s("hal")
    except ValueError:
        return False


def is_it_agama(t: Term) -> bool:
    """``True`` iff `t` is the iṭ-āgama."""
    return t.u == "iw" and t.all(T.AGAMA)


def is_aprkta(t: Term) -> bool:
    """``True`` iff `t` is apr̥kta (a single-sound pratyaya)."""
    return t.all(T.PRATYAYA) and len(t.text) == 1


def is_laghu(t: Term) -> bool:
    """``True`` iff the last syllable of `t` is or could be laghu."""
    # 1.4.10 hrasvaM laghu
    # 1.4.11 saMyoge guru
    # TODO: remove C hack
    return t.antya in HRASVA or (
        t.upadha in HRASVA and not samyoganta(t) and t.antya != "C"
    )


def is_hrasva(t: Term) -> bool:
    """``True`` iff the last sound of `t` is a short vowel."""
    # 1.4.10 hrasvaM laghu
    return t.antya in HRASVA


def is_guru(t: Term) -> bool:
    """``True`` iff the last syllable of `t` is guru."""
    return not is_laghu(t)


def is_knit(t: Term) -> bool:
    return t.any("k", "N")


def is_asti(t: Term) -> bool:
    return t.u == "asa~" and t.gana == 2


def can_use_guna(c: Term, n: Term):
    # 1.1.5 kNiti ca
    if n.any("k", "N"):
        return False
    # 1.1.6 dIdhI-vevI-iTAm
    if c.u in {"dIDIN", "vevIN"} or is_it_agama(c):
        return False

    # 1.1.3 iko guNavRddhI
    # TODO: check for ik?
    return True


def is_nit_lakara(la: Term) -> bool:
    return la.any("la~N", "li~N", "lu~N", "lf~N")


def is_eka_ac(t: Term) -> bool:
    num_vowels = sum(1 for L in t.text if L in s("ac"))
    # HACK to have ekac apply for am-Agama
    return num_vowels == 1 or "fa" in t.text
