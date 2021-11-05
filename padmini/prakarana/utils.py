from padmini.prakriya import Prakriya, Term
from padmini.sounds import s


def per_term(p: Prakriya):
    """Windowed iterator per term."""
    terms = [t for t in p.terms if t.text]
    for i, cur in enumerate(terms):
        try:
            next = terms[i + 1]
        except IndexError:
            next = None
        yield (cur, next)


def eka_ac(t: Term) -> bool:
    num_vowels = sum(1 for L in t.text if L in s("ac"))
    # HACK to have ekac apply for am-Agama
    return num_vowels == 1 or "fa" in t.text
