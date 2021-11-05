from padmini import operations as op
from padmini.constants import Tag as T
from padmini.dhatu_gana import CUR_MIT, KUSMADI, GARVADI
from padmini.prakriya import Term, Prakriya
from . import it_samjna


def run(p: Prakriya, pratipadika: str, linga: str):
    pratipadika = Term.make_term(pratipadika)

    # The prAtipadika enters the prakriyA
    p.terms = [pratipadika]
    p.step("start")

    # Samjna rules
    op.samjna("1.2.45", p, pratipadika, T.PRATIPADIKA)
    pratipadika.add_tags(linga)
