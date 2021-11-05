from padmini import operations as op
from padmini.constants import Tag as T
from padmini.dhatu_gana import CUR_MIT, KUSMADI, GARVADI
from padmini.prakriya import Term, Prakriya
from . import it_samjna


def run(p: Prakriya, dhatu: str, dhatu_code: str):
    gana, _, number = dhatu_code.partition(".")
    dhatu = Term.make_dhatu(dhatu, int(gana), number)

    # The root enters the prakriyA
    p.terms = [dhatu]
    p.step("start")

    # Samjna rules
    op.samjna("1.3.1", p, dhatu, T.DHATU)
    it_samjna.run_no_index(p, dhatu)

    if dhatu.text in {"dA", "de", "do", "DA", "De"} and dhatu.u != "dA\\p":
        op.samjna("1.1.20", p, dhatu, T.GHU)

    # satva
    if dhatu.adi == "z":
        # Vartika -- no change for zWiv or zvask
        if dhatu.text in ("zWiv", "zvazk"):
            p.step("6.1.64.v1")
        # Vartika -- also change next sound
        elif dhatu.text[:2] in ("zw", "zW", "zR"):
            dhatu.text = dhatu.text.replace("zw", "st")
            dhatu.text = dhatu.text.replace("zW", "sT")
            dhatu.text = dhatu.text.replace("zR", "sn")
            dhatu.add_tags(T.F_ADESHA_ADI)
        else:
            dhatu.add_tags(T.F_ADESHA_ADI)
            op.adi("6.1.64", p, dhatu, "s")

    # natva
    elif dhatu.adi == "R":
        dhatu.add_tags(T.F_ADESHA_ADI)
        op.adi("6.1.65", p, dhatu, "n")

    # nu~m-Agama
    # Although this is declared in the "aNgasya" section of the Ashtadhyayi,
    # applying this rule there will cause problems, e.g. when applying 3.1.80
    # (dhinvikRNvyor a ca). To see why, try moving this rule and running the
    # tests.
    #
    # TODO: why exception for cakz?
    if dhatu.all("i") and dhatu.u != "ca\\kzi~\\N":
        op.mit("7.1.58", p, dhatu, "n")

    # gaNa-sUtras
    if dhatu.gana == 10:
        if dhatu.u in CUR_MIT:
            dhatu.add_tags("m")
        # Need to check range explicitly because some of these roots appear
        # multiple times in the gana, e.g. lakza~
        if dhatu.u in KUSMADI and (not number or 192 <= int(number) <= 236):
            p.step("kusmadi")
            p.add_tags(T.ATMANEPADA)
        elif dhatu.u in GARVADI and (not number or 440 <= int(number) <= 449):
            p.step("garvadi")
            p.add_tags(T.ATMANEPADA)

    # These two roots are always used with the upasarga adhi-:
    if dhatu.u in {"i\\N", "i\\k"}:
        upa = Term.make_upadesha("aDi")
        p.terms = [upa] + p.terms
        upa.add_tags(T.UPASARGA)
        p.step("1.4.80")
