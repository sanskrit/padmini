"""
sanadyanta (3.1.5 - 3.1.32)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import padmini.operations as op
from padmini.prakriya import Term, Prakriya
from padmini.constants import Tag as T
from . import it_samjna

#: Use san-pratyaya with a long abhyAsa.
MAN_BADHA = {"mAna~\\", "baDa~\\", "dAna~^", "SAna~^"}
#: Use their pratyaya optionally if followed by ArdhadhAtuka.
AYADADA = {"gupU~", "DUpa~", "vicCa~", "paRa~\\", "pana~\\", "fti", "kamu~\\"}


def add_sanadi(
    rule_code: str,
    p: Prakriya,
    dhatu: Term,
    upadesha: str,
    no_ardhadhatuka: bool = False,
):
    pratyaya = Term.make_upadesha(upadesha)
    pratyaya.add_tags(T.PRATYAYA, upadesha)

    op.insert_after(rule_code, p, dhatu, pratyaya)

    # Used e.g. for "san" after "gup" to prevent it and guNa.
    if no_ardhadhatuka:
        pratyaya.add_tags(T.F_NO_ARDHADHATUKA)

    # 3.1.32 sanAdyantA dhAtavaH
    op.samjna("3.1.32", p, pratyaya, T.DHATU)
    it_samjna.run_no_index(p, pratyaya)


def run(p: Prakriya, is_ardhadhatuka: bool):
    _, dhatu = p.find_first(T.DHATU)

    # gana needed to exclude 03.0021 kita~
    if dhatu.u in {"gupa~\\", "tija~\\", "kita~"} and dhatu.gana == 1:
        add_sanadi("3.1.5", p, dhatu, "san", no_ardhadhatuka=True)
    elif dhatu.u in MAN_BADHA:
        add_sanadi("3.1.6", p, dhatu, "san", no_ardhadhatuka=True)
    # TODO: 3.1.8 - 3.1.24
    elif dhatu.gana == 10:
        add_sanadi("3.1.25", p, dhatu, "Ric")
    # TODO: 3.1.26 - 3.1.27

    elif dhatu.u in AYADADA:
        add_pratyaya = True
        if is_ardhadhatuka:
            if p.allow("3.1.31"):
                add_pratyaya = False
                p.step("3.1.31")
            else:
                p.decline("3.1.31")

        if add_pratyaya:
            if dhatu.u in {"gupU~", "DUpa~", "vicCa~", "paRa~\\", "pana~\\"}:
                add_sanadi("3.1.28", p, dhatu, "Aya")
            elif dhatu.u == "fti":
                add_sanadi("3.1.29", p, dhatu, "IyaN")
            elif dhatu.u == "kamu~\\":
                add_sanadi("3.1.30", p, dhatu, "RiN")
