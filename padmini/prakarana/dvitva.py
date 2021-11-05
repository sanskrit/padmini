from padmini import filters as f
from padmini import operations as op
from padmini.constants import Tag as T
from padmini.sounds import s
from padmini.prakriya import Term, Prakriya
from padmini.term_views import TermView
from padmini.prakarana.utils import eka_ac


def _double(rule: str, p: Prakriya, dhatu: Term, i: int) -> Term:
    # Special logic for Nic.
    if (
        dhatu.adi in s("ac")
        and dhatu.antya in s("hal")
        and p.terms[i + 1].u in {"Ric", "RiN"}
    ):
        ni = p.terms[i + 1]
        text = dhatu.text + ni.text

        third = Term.make_term(text[1:])
        while f.samyogadi(third) and third.adi in {"n", "d", "r"}:
            third.text = third.text[1:]
        third.u = p.terms[i + 1].u
        third.add_tags(T.DHATU)

        ni.text = third.text
        dhatu.text = dhatu.text[: -len(third.text) + 1]

        op.insert_after(rule, p, ni, third)
        op.samjna("6.1.4", p, ni, T.ABHYASA)

        dhatu.add_tags(T.ABHYASTA)
        ni.add_tags(T.ABHYASTA)
        third.add_tags(T.ABHYASTA)
        p.step("6.1.5")

    elif eka_ac(dhatu) or dhatu.adi in s("hal"):
        # TODO: correctly double jAgR
        abhyasa = Term.make_term(dhatu.text)
        op.insert_before(rule, p, dhatu, abhyasa)
        op.samjna("6.1.4", p, abhyasa, T.ABHYASA)

        abhyasa.add_tags(T.ABHYASTA)
        dhatu.add_tags(T.ABHYASTA)
        if p.terms[i + 2].u in ("Ric", "RiN"):
            p.terms[i + 2].add_tags(T.ABHYASTA)
        p.step("6.1.5")
    else:
        # Create 3 terms:
        # 1. the dhatu without the abhyasa
        # 2. the abhyasa
        # 3. the doubled portion

        # 6.1.2 ajAder dvitIyasya
        # 6.1.3 na ndrAH saMyogAdayaH
        third = Term.make_term(dhatu.text[1:])
        while f.samyogadi(third) and third.adi in {"n", "d", "r"}:
            third.text = third.text[1:]
        third.u = dhatu.u
        third.add_tags(T.DHATU)

        # Ru -> nu for UrRu
        if dhatu.text == "UrRu":
            third.text = "nu"

        abhyasa = Term.make_term(third.text)
        abhyasa.add_tags(T.ABHYASA)
        dhatu.text = dhatu.text[: -len(third.text)]

        op.insert_after(None, p, dhatu, abhyasa)
        op.insert_after(rule, p, abhyasa, third)
        op.samjna("6.1.4", p, abhyasa, T.ABHYASA)

        dhatu.add_tags(T.ABHYASTA)
        third.add_tags(T.ABHYASTA)
        abhyasa.add_tags(T.ABHYASTA)
        if p.terms[i + 3].u in ("Ric", "RiN"):
            p.terms[i + 3].add_tags(T.ABHYASTA)
        p.step("6.1.5")


def run_for_each(p: Prakriya, dhatu: Term, i: int):
    n = TermView.make_pratyaya(p, i)
    if not n:
        return

    # HACK for Nic + caN
    if n.terms[0].u in ("Ric", "RiN"):
        n = TermView.make_pratyaya(p, i + 1)

    n.u = n.terms[0].u
    if dhatu.text in {"jakz", "jAgf", "daridrA", "cakAs", "SAs", "dIDI", "vevI"}:
        # These are termed abhyasta, but they can still undergo dvitva because
        # the rules below inherit "anabhyAsasya" from 6.1.8.
        op.tag("6.1.6", p, dhatu, T.ABHYASTA)

    if n.all("li~w"):
        # kAshikA:
        #   dayateḥ iti dīṅo grahaṇaṃ na tu daya dāne ityasya.
        #   digyādeśena dvirvacanasya bādhanam iṣyate.
        if dhatu.u == "de\\N":
            op.text("7.4.9", p, dhatu, "digi")
        else:
            _double("6.1.8", p, dhatu, i)
    elif n.u in ("san", "yaN"):
        _double("6.1.9", p, dhatu, i)
    elif n.terms[0].any(T.SLU):
        _double("6.1.10", p, dhatu, i)
    elif n.u == "caN":
        _double("6.1.11", p, dhatu, i)


def run(p: Prakriya):
    i = 0
    num_terms = len(p.terms)
    while i < num_terms:
        c = p.terms[i]
        # HACK to avoid doubling the nic / nin
        if c.any(T.DHATU) and c.u not in {"Ric", "RiN"}:
            run_for_each(p, c, i)

        # Skip new terms
        i += 1 + (len(p.terms) - num_terms)
        num_terms = len(p.terms)
