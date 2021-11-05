"""
atmanepada (1.3.12 - 1.3.93 [end])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rules to determine parasmaipada/Atmanepada.

The terms *parasmaipada* and *Atmanepada* properly refer to the substitutions
for the various lakAras. But we haven't made any substitutions yet. So, how can
we apply these *pada* designations at this stage?

The answer is that we attach these designations *to the prakriyA* to set the
derivation context. Then when we introduce the correct tiN suffix, we will
assign *parasmaipada* or *Atmanepada* to it as appropriate.
"""

import padmini.operations as op
from padmini.prakriya import Prakriya
from padmini.constants import Tag as T
from padmini.dhatu_gana import DYUT_ADI


VRDBHYAH = {"vftu~\\", "vfDu~\\", "SfDu~\\", "SfDu~^", "syandU~\\"}


def use_atmanepada(rule_code: str, p: Prakriya):
    p.add_tags(T.ATMANEPADA)
    p.step(rule_code)


def use_parasmaipada(rule_code: str, p: Prakriya):
    p.add_tags(T.PARASMAIPADA)
    p.step(rule_code)


def apply_shorthand(p: Prakriya, upasargas, dhatu, rules):
    for rule_code, rule_upasargas, rule_dhatus, pada in rules:
        # Match by default if no upasargas required.
        upa_match = not rule_upasargas
        # Match if the upasarga before the verb is in the list.
        upa_match |= bool(upasargas and upasargas[-1].text in rule_upasargas)
        dhatu_match = dhatu.text in rule_dhatus

        if upa_match and dhatu_match:
            if pada == "A":
                use_atmanepada(rule_code, p)
            elif pada == "U":
                op.optional(use_atmanepada, rule_code, p)
            elif pada == "P":
                use_parasmaipada(rule_code, p)
            else:
                assert pada == None
            # Don't apply any further rules.
            return


def run(p: Prakriya):
    upasargas = []
    for t in p.terms:
        if t.any(T.UPASARGA):
            upasargas.append(t)
        else:
            break

    # Use first because of "pUrvavat sanaH"
    _, dhatu = p.find_first(T.DHATU)
    la = p.terms[-1]

    if p.any(T.ATMANEPADA):
        # E.g. if set by gana sutra (see `dhatu_karya`)
        return

    if p.any(T.BHAVE, T.KARMANI):
        use_atmanepada("1.3.13", p)

    vidhi_lin = la.u == "li~N" and not p.all(T.ASHIH)

    # Needed for rules 1.3.60 and 1.3.61 below.
    is_sarvadhatuka = la.u in {"la~w", "lo~w", "la~N"} or vidhi_lin
    # Needed for rule 1.3.61 below.
    is_lun_lin = la.u in {"lu~N", "li~N"}

    # Most of these rules can be expressed in a simple shorthand. The last
    # field in each in each tuple is whether the pada is always Atmanepada (A),
    # always parasmaipada (P), or dependent on some semantic condition (U).
    #
    # Rules that can't easily be modeled in this format are further below.
    basic_rules = [
        ("1.3.17", ["ni"], "viS", "A"),
        ("1.3.18", ["pari", "vi", "ava"], "ji", "A"),
        ("1.3.19", ["vi", "parA"], "ji", "A"),
        ("1.3.20", ["AN"], "dA", "U"),
        ("1.3.21", ["anu", "sam", "pari"], "krIq", "A"),
        ("1.3.22", ["sam", "ava", "pra", "vi"], "sTA", "A"),
        ("1.3.23", [], "sTA", "U"),
        ("1.3.24", ["ud"], "sTA", "U"),
        ("1.3.25", ["upa"], "sTA", "U"),
        # 1.3.26 can be handled with 1.3.25.
        ("1.3.27", ["ud", "vi"], "tap", "U"),
        ("1.3.28", ["AN"], ["yam", "han"], "U"),
        # TODO: f in class 1 only
        ("1.3.29", ["sam"], ["gam", "fC", "praC", "svf", "f", "Sru", "vid"], "U"),
        ("1.3.30", ["ni", "sam", "upa", "vi"], ["hve"], "A"),
        ("1.3.31", ["AN"], ["hve"], "U"),
        # 1.3.32 - 1.3.37 can be handled with 1.3.72.
        ("1.3.38", [], ["kram"], "U"),
        # 1.3.39 - 1.3.43 can be handled with 1.3.38.
        # 1.3.44 - 1.3.46 can be handled with 1.3.76.
        ("1.3.47", [], ["vad"], "U"),
        # 1.3.48 - 1.3.50 can be handled with 1.3.47.
        ("1.3.51", ["ava"], ["grah"], "A"),
        # TODO: 1.3.52 - 1.3.56
        # 1.3.57 - 1.3.60 are further below.
        # TODO: 1.3.61 - 1.3.64.
        ("1.3.65", ["sam"], ["kzRu"], "A"),
        # TODO: 1.3.66 - 1.3.71.
        # 1.3.72 is further below.
        ("1.3.73", ["apa"], ["vad"], "U"),
        # 1.3.74 is further below.
        ("1.3.75", ["sam", "ud", "AN"], ["yam"], "U"),
        # 1.3.76 is further below.
        # 1.3.77 has similar scope to 1.3.72.
        # 1.3.78 is further below.
        ("1.3.79", ["anu", "parA"], ["kf"], "P"),
        ("1.3.80", ["aBi", "prati", "ati"], ["kzip"], "P"),
        ("1.3.81", ["pra"], ["vah"], "P"),
        ("1.3.82", ["pari"], ["mfz"], "P"),
        ("1.3.83", ["vi", "AN", "pari"], ["ram"], "P"),
        # 1.3.84 sets anuvrtti for 1.3.85
        ("1.3.85", ["upa"], ["ram"], "U"),
        # TODO: 1.3.86 - 1.1.93
    ]
    apply_shorthand(p, upasargas, dhatu, basic_rules)

    san_rules = [
        # Reordered to take priority over 1.3.57
        ("1.3.58", ["anu"], ["jYA"], "P"),
        ("1.3.59", ["prati", "AN"], ["Sru"], "P"),
        ("1.3.57", [], ["jYA", "Sru", "smf", "dfS"], "A"),
    ]
    if p.find(lambda x: x.all(T.PRATYAYA, "san")):
        apply_shorthand(p, upasargas, dhatu, san_rules)

    # Specific rules (ubhayapada)

    if p.any(T.PARASMAIPADA, T.ATMANEPADA):
        # Matched above already
        pass
    elif dhatu.text == "nAT":
        # vArttika
        op.optional(use_parasmaipada, "1.3.21.v7", p)
    elif dhatu.text == "sasj":
        # Kaumudi
        op.optional(use_atmanepada, "sasj-k", p)
    elif dhatu.text == "Sad" and is_sarvadhatuka:
        # Technically the condition here is "Siti", but sArvadhAtuka is close
        # enough.
        use_atmanepada("1.3.60", p)
    elif dhatu.u == "mf\\N":
        if not (is_sarvadhatuka or is_lun_lin):
            use_parasmaipada("1.3.61", p)
    elif dhatu.u in DYUT_ADI and dhatu.gana == 1 and la.u == "lu~N":
        op.optional(use_parasmaipada, "1.3.91", p)
    # TODO: san
    elif dhatu.u in VRDBHYAH and dhatu.gana == 1 and la.u in {"lf~w", "lf~N"}:
        op.optional(use_parasmaipada, "1.3.92", p)
    elif dhatu.u == "kfpU~\\" and la.u in {"lf~w", "lf~N", "lu~w"}:
        op.optional(use_parasmaipada, "1.3.93", p)

    # General rules

    if p.any(T.PARASMAIPADA, T.ATMANEPADA):
        # Matched above already
        pass
    elif dhatu.any("N", T.ANUDATTET):
        use_atmanepada("1.3.12", p)
    elif dhatu.any("Y", T.SVARITET):
        op.optional(use_atmanepada, "1.3.72", p)
    elif len(p.terms) == 3 and p.terms[1].u == "Ric":
        op.optional(use_atmanepada, "1.3.74", p)
    elif dhatu.text == "jYA" and not upasargas:
        op.optional(use_atmanepada, "1.3.76", p)

    if p.all(T.KARTARI) and not p.all(T.ATMANEPADA):
        use_parasmaipada("1.3.78", p)

    assert p.any(T.PARASMAIPADA, T.ATMANEPADA)
