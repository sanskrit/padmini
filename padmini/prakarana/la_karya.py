"""
la_karya
~~~~~~~~
(various rules in 3.2, 3.3, and 3.4)

Rules that introduce a specific lakāra to the prakriyā.

Most lakāras are available under multiple different semantic conditions. For
example, laṭ denotes the present tense, but it can denote the past tense if
*sma* is used as an upapada. But since Padmini focuses specifically on
generating word forms with their common semantics, implementing all of these
conditions would complicate the program with little real gain. Therefore, we
implement one common semantic condition per lakāra.
"""

import padmini.operations as op
from padmini.prakriya import Term, Prakriya
from padmini.constants import Tag as T
from . import it_samjna


def add_la(rule_code: str, p: Prakriya, dhatu: Term, la: str):
    """Add a lakAra and apply any necessary it rules."""
    la = Term.make_upadesha(la)
    la.add_tags(T.PRATYAYA)

    op.insert_after(rule_code, p, dhatu, la)
    it_samjna.run_no_index(p, la)


def run(p: Prakriya, la: str):
    """Add a lakAra to the prakriya.

    Generally, each lakAra could be added by any of several different rules.
    Here, we choose a representative rule without being pedantic about it.
    """
    _, dhatu = p.find_last(T.DHATU)

    if la == "la~w":
        add_la("3.3.123", p, dhatu, la)
    elif la == "li~w":
        add_la("3.2.114", p, dhatu, la)
    elif la == "lu~w":
        add_la("3.3.15", p, dhatu, la)
    elif la == "lf~w":
        add_la("3.3.13", p, dhatu, la)
    elif la == "le~w":
        add_la("3.4.7", p, dhatu, la)
    elif la == "lo~w":
        add_la("3.3.162", p, dhatu, la)
    elif la == "la~N":
        add_la("3.2.111", p, dhatu, la)
    elif la == "li~N":
        if p.all(T.ASHIH):
            add_la("3.3.173", p, dhatu, la)
        else:
            add_la("3.3.161", p, dhatu, la)
    elif la == "lu~N":
        add_la("3.2.110", p, dhatu, la)
    elif la == "lf~N":
        add_la("3.3.139", p, dhatu, la)
    else:
        raise VyakaranaException(f"Unknown lakara {la}.")
