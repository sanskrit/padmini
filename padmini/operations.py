import re
from typing import List, Optional

from .constants import Tag as T
from .prakarana import it_samjna
from .prakriya import Term, Prakriya
from .sounds import s


def optional(func, rule: str, p: Prakriya, *args) -> bool:
    """Wrapper that defines an optional operation.

    If the original operation has this syntax::

        func(rule, p, *args)

    Then we can make the operation optional with::

        optional(func, rule, p, *args)

    :param func: the :mod:`operation` function to apply
    :param rule: the rule ID
    :param p: the prakriya
    :param args: the args to pass to `func`
    :return: ``True`` iff the option was accepted.
    """
    if p.allow(rule):
        func(rule, p, *args)
        return True
    else:
        p.decline(rule)
        return False


### Delete a term's text


def lopa(rule: str, p: Prakriya, u: Term):
    """Delete the given term."""
    u.text = ""
    p.step(rule)


def luk(rule: str, p: Prakriya, u: Term):
    """Delete the given term with `luk`."""
    u.text = ""
    u.add_tags(T.LUK)
    p.step(rule)


def slu(rule: str, p: Prakriya, u: Term):
    """Delete the given term with `Slu`."""
    u.u = ""
    u.text = ""
    u.add_tags(T.SLU)
    p.step(rule)


### Replace text in a term


def adi(rule: Optional[str], p: Prakriya, u: Term, sub: str):
    """Replace the first sound."""
    L = u.adi
    if L != sub:
        u.text = sub + u.text[1:]
        if rule:
            p.step(rule)


def antya(rule: str, p: Prakriya, u: Term, sub: str):
    """Replace the last sound."""
    L = u.antya
    if L != sub:
        u.text = u.text[:-1] + sub
        p.step(rule)


def mit(rule: str, p: Prakriya, u: Term, sub: str):
    """Insert after the last vowel."""
    ac = s("ac").regex
    hal = s("hal").regex
    u.text = re.sub(f"({ac})({hal}*)$", f"\\1{sub}\\2", u.text)
    p.step(rule)


def ti(rule: str, p: Prakriya, u: Term, sub: str):
    """Replace from the last vowel on."""
    ac = s("ac").regex
    hal = s("hal").regex
    u.text = re.sub(f"{ac}{hal}*$", sub, u.text)
    p.step(rule)


def upadha(rule_code: str, p: Prakriya, u: Term, sub: str):
    """Replace the penultimate sound."""
    u.text = u.text[:-2] + sub + u.text[-1]
    p.step(rule_code)


def text(rule: str, p: Prakriya, u: Term, sub: str):
    """Replace `Term.text`."""
    u.text = sub
    p.step(rule)


def upadesha(rule: str, p: Prakriya, u: Term, sub: str):
    """Replace `Term.upadesha` and apply `it_samjna.run`."""
    u.u = u.text = sub
    p.step(rule)
    it_samjna.run_no_index(p, u)


def upadesha_no_it(rule: str, p: Prakriya, u: Term, sub: str):
    """Replace `Term.upadesha` with no follow_up, in case we need to apply lopa."""
    u.u = u.text = sub
    p.step(rule)


### Insert term


def insert_before(rule: str, p: Prakriya, needle: Term, new_term: Term):
    """Insert before the given term."""
    found = False
    for i, t in enumerate(p.terms):
        if t is needle:
            found = True
            break
    assert found
    p.terms.insert(i, new_term)
    p.step(rule)


def insert_after(rule: Optional[str], p: Prakriya, needle: Term, new_term: Term):
    """Insert after the given term."""
    found = False
    for i, t in enumerate(p.terms):
        if t is needle:
            found = True
            break
    assert found
    p.terms.insert(i + 1, new_term)
    if rule:
        p.step(rule)


def insert_agama_before(rule: str, p: Prakriya, needle: Term, upa: str):
    agama = Term.agama(upa)
    insert_before(rule, p, needle, agama)
    it_samjna.run_no_index(p, agama)


def insert_agama_after(rule: str, p: Prakriya, index: int, upa: str):
    p.terms.insert(index + 1, Term.agama(upa))
    p.step(rule)
    it_samjna.run(p, index + 1)


def insert_agama_after_by_term(rule: str, p: Prakriya, needle: Term, upa: str):
    agama = Term.agama(upa)
    insert_after(rule, p, needle, agama)
    it_samjna.run_no_index(p, agama)


### Add samjna


def tag(rule: str, p: Prakriya, u: Term, *tags: List[str]):
    """Add new tags to `u`."""
    u.add_tags(*tags)
    p.step(rule)


samjna = tag


### Legacy rules


def yatha(text: str, before, after):
    """Legacy function. Replace in 1:1 correspondence."""
    assert len(before) == len(after)
    mapping = dict(zip(before, after))
    return mapping[text]


def antya_yatha(base: str, before, after) -> str:
    """Legacy function. Replace from the last sound on."""
    last = base[-1]
    mapping = dict(zip(before, after))
    return base[:-1] + mapping[last]
