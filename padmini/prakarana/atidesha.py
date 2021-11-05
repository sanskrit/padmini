from padmini import filters as f
from padmini import operations as op
from padmini.constants import Tag as T
from padmini.dhatupatha import is_kutadi
from padmini.prakriya import Prakriya
from padmini.sounds import s
from padmini.term_views import TermView


def run_for_index(p: Prakriya, index: int):
    # Should run after it-Agama has been added.
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    iti = f.is_it_agama(n.terms[0])

    # Needs an explicit check against gana == 6 to avoid including similar
    # roots from other ganas.
    in_kutadi = is_kutadi(c)
    if (c.u == "gAN" or in_kutadi) and not n.any("R", "Y"):
        op.tag("1.2.1", p, n.terms[0], "N")

    # Must check for AGAMA specifically because of the tiN ending "iw".
    elif c.text == "vij" and iti:
        op.tag("1.2.2", p, n.terms[-1], "N")
    elif c.text == "UrRu" and iti:
        if p.allow("1.2.3"):
            p.step("1.2.3")
        else:
            n.terms[-1].add_tags("N")
            p.decline("1.2.3")

    elif n.all(T.SARVADHATUKA) and not n.all("p"):
        op.tag("1.2.4", p, n.terms[-1], "N")

    elif c.any(T.DHATU) and not f.samyoganta(c) and n.all("li~w") and not n.all("p"):
        op.tag("1.2.5", p, n.terms[-1], "k")

    elif c.text in {"BU", "inD"} and n.all("li~w"):
        op.tag("1.2.6", p, n.terms[-1], "k")

    elif n.all("li~w") and c.text in {"SranT", "granT", "danB", "svanj"}:
        # TODO: rule seems obligatory; where is optionality defined?
        op.optional(op.tag, "1.2.6.v1", p, n.terms[-1], "k")

    tin = p.terms[-1]
    if (
        tin.all(T.ATMANEPADA) and (tin.all("li~N") or n.terms[0].u == "si~c")
    ) and n.adi in s("Jal"):
        is_dhatu = c.all(T.DHATU)
        ik_halantat = c.upadha in s("ik") and c.antya in s("hal")

        if is_dhatu and ik_halantat:
            op.tag("1.2.11", p, n.terms[-1], "k")
        elif is_dhatu and c.antya in s("f"):
            op.tag("1.2.12", p, n.terms[-1], "k")


def attva_atidesha_for_index(p: Prakriya, index: int):
    """Atidesha rules that apply only if the root ends in long A.

    If we don't use a separate function for these rules, we have a dependency
    loop:

        iT-Agama --> atidesha & samprasarana

        atidesha & samprasarana --> Ad-Adesha

        Ad-Adesha --> iT-Agama (sak ca)

    So we break the loop by doing the following:

        iT-Agama (non-A) --> atidesha & samprasarana (non-A)

        atidesha & samprasarana (non-A) -> Ad-Adesha

        Ad-Adesha --> iT-Agama (A)

        iT-Agama (A) --> atidesha and samprasarana (A)


    """
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    tin = p.terms[-1]
    if (
        tin.all(T.ATMANEPADA)
        and n.terms[-1].u == "si~c"
        and (c.text == "sTA" or c.all(T.GHU))
    ):
        n.terms[-1].add_tags("k")
        op.antya("1.2.17", p, c, "i")


def run_before_attva(p: Prakriya):
    """Run before the rule "Adeca upadeze 'ziti"."""
    for i, _ in enumerate(p.terms):
        run_for_index(p, i)


def run_after_attva(p: Prakriya):
    """Run after the rule "Adeca upadeze 'ziti"."""
    for i, _ in enumerate(p.terms):
        attva_atidesha_for_index(p, i)
