"""
vikarana
~~~~~~~~~~~~~~~~~
(3.1.33 - 3.1.90)

Rules that add various intermediate suffixes, called **vikaraṇas**, between the
dhātu and the tiṅ ending. Roughly, we can split these rules into four groups:

- rules for lr̥t, lr̥ṅ, luṭ, and leṭ (3.1.33 - 3.1.34)
- rules for ām-pratyaya (3.1.35 - 3.1.42)
- rules for luṅ (3.1.43 - 3.1.67)
- rules for sārvadhātuka pratyayas (3.1.68 - 3.1.90), which includes laṭ, loṭ,
  laṅ, and vidhi-liṅ.

(āśīr-liṅ and liṭ do not use any vikaraṇas.)
"""


# The it-prakarana is applied at the very end, since there might be various
# substitutions by lopa that block the prakarana.


from padmini import filters as f
from padmini import operations as op
from padmini.prakriya import Term, Prakriya
from padmini.constants import Tag as T
from padmini.sounds import s
from padmini.dhatu_gana import PUSH_ADI, DYUT_ADI, TAN_ADI
from . import it_samjna


def _add(rule_code: str, p: Prakriya, upadesha: str):
    """Add a vikarana.

    We defer it-prakarana because we might need to apply lopa.
    """
    vikarana = Term.make_upadesha(upadesha)
    vikarana.add_tags(T.PRATYAYA, T.VIKARANA)

    _, dhatu = p.find_last(T.DHATU)
    assert dhatu
    op.insert_after(rule_code, p, dhatu, vikarana)


def _add_am(rule_code: str, p: Prakriya, am=None):
    if not am:
        am = Term.make_upadesha("Am")
        am.add_tags(T.PRATYAYA)

    _, dhatu = p.find_last(T.DHATU)
    assert dhatu
    op.insert_after(rule_code, p, dhatu, am)


def lun_vikarana(p: Prakriya):
    """Apply the vikarana rules for luG (3.1.43 - 3.1.66)

    :param p: the prakriya
    """

    _add("3.1.43", p, "cli~")
    dhatu, cli, tin = p.terms[-3:]

    # The vArttika doesn't say this specifically, but the commentator examples
    # imply that this holds only for parasmaipada.
    if dhatu.text in {"spfS", "mfS", "kfz", "tfp", "dfp"} and tin.any(T.PARASMAIPADA):
        if op.optional(op.upadesha_no_it, "3.1.44.v1", p, cli, "si~c"):
            return

    shal_igupadha_anit = (
        dhatu.antya in s("Sal")
        and dhatu.upadha in s("ik")
        # iT hasn't been added yet, so check for "U" (veT) and anudAtta (aniT).
        and (dhatu.all(T.ANUDATTA) or dhatu.all("U"))
    )
    jr_stambhu = {"jF", "stanB", "mruc", "mluc", "gruc", "gluc", "glunc", "Svi"}

    # Takes priority over shala igupadha
    pushadi_dyutadi_ldit = (
        (dhatu.u in PUSH_ADI and dhatu.gana == 4)
        or (dhatu.u in DYUT_ADI and dhatu.gana == 1)
        or dhatu.all("x")
    )
    if tin.all(T.PARASMAIPADA) and cli.u == "cli~" and pushadi_dyutadi_ldit:
        op.upadesha_no_it("3.1.55", p, cli, "aN")

    elif shal_igupadha_anit:
        if dhatu.text == "dfS":
            p.step("3.1.47")
        elif dhatu.text == "Sliz" and dhatu.gana == 4:
            op.optional(op.upadesha_no_it, "3.1.46", p, cli, "ksa")
        else:
            if dhatu.all("U"):
                # Needed if we use "ksa" with a veT root.
                if p.allow(T.F_ANIT_KSA):
                    p.add_tags(T.F_ANIT_KSA)
                    op.upadesha_no_it("3.1.45", p, cli, "ksa")
                else:
                    p.add_tags(T.F_SET_SIC)
                    p.decline(T.F_ANIT_KSA)
            else:
                op.upadesha_no_it("3.1.45", p, cli, "ksa")

    shri_dru_sru = dhatu.text in ("Sri", "dru", "sru")
    if p.all(T.KARTARI) and (dhatu.u in ("Ric", "RiN") or shri_dru_sru):
        op.upadesha_no_it("3.1.48", p, cli, "caN")
    elif dhatu.u == "kamu~\\":
        op.upadesha_no_it("3.1.48.v1", p, cli, "caN")
    elif dhatu.text in ("De", "Svi"):
        op.optional(op.upadesha_no_it, "3.1.49", p, cli, "caN")
    # TODO: 3.1.50 - 3.1.51
    elif dhatu.u == "asu~" or dhatu.text in {"vac", "KyA"}:
        op.upadesha_no_it("3.1.52", p, cli, "aN")
    elif dhatu.text in {"lip", "sic", "hve"}:
        skip = False
        if tin.all(T.ATMANEPADA):
            if p.allow("3.1.54"):
                p.step("3.1.54")
                skip = True
            else:
                p.decline("3.1.54")
        if not skip:
            op.upadesha_no_it("3.1.53", p, cli, "aN")

    # Ensure no substitution has already occurred (e.g. for Svi which can be
    # matched by 3.1.49 above).
    if tin.all(T.PARASMAIPADA) and cli.u == "cli~":
        if dhatu.text in {"sf", "SAs", "f"}:
            op.upadesha_no_it("3.1.56", p, cli, "aN")
        elif dhatu.all("ir"):
            op.optional(op.upadesha_no_it, "3.1.57", p, cli, "aN")
        elif dhatu.text in jr_stambhu:
            op.optional(op.upadesha_no_it, "3.1.58", p, cli, "aN")
        elif dhatu.text in {"kf", "mf", "df", "ruh"} and p.all(T.CHANDASI):
            op.upadesha_no_it("3.1.59", p, cli, "aN")

    # TODO: ciN (3.1.60 - 3.1.66)
    if tin.u == "ta":
        if dhatu.text == "pad":
            op.upadesha_no_it("3.1.60", p, cli, "ciR")
        elif dhatu.text in {"dIp", "jan", "buD", "pUr", "tAy", "pyAy"}:
            op.optional(op.upadesha_no_it, "3.1.61", p, cli, "ciR")

    # Base case
    if cli.u == "cli~":
        op.upadesha_no_it("3.1.44", p, cli, "si~c")


def am_pratyaya_lit(p: Prakriya):
    _, dhatu = p.find_last(T.DHATU)
    la = p.terms[-1]

    if dhatu.text == "kAs" or dhatu.all(T.PRATYAYA):
        _add_am("3.1.35", p)
    # jAgf is handled separately below.
    elif not f.is_eka_ac(dhatu) and dhatu.text not in {"jAgf", "UrRu"}:
        _add_am("3.1.35.v1", p)
    elif dhatu.adi in s("ic") and f.is_guru(dhatu) and dhatu.u != "fCa~":
        _add_am("3.1.36", p)
    elif dhatu.text in {"day", "ay", "As"}:
        _add_am("3.1.37", p)
    elif dhatu.text in {"uz", "jAgf"} or (dhatu.text == "vid" and dhatu.gana == 2):
        if op.optional(_add_am, "3.1.38", p):
            if dhatu.text == "vid":
                # vid does not go through guNa.
                dhatu.add_tags(T.F_GUNA_APAVADA)
        else:
            return
    elif dhatu.text in {"BI", "hrI", "hu"} or dhatu.u == "quBf\\Y":
        am = Term.make_upadesha("Am")
        am.add_tags(T.PRATYAYA, T.SLU)
        if not op.optional(_add_am, "3.1.39", p, am):
            return
    else:
        return

    # "Am" added.
    # TODO: qukf//Y?
    kf = Term.make_dhatu("kf", 8)
    kf.add_tags(T.DHATU)
    p.terms = p.terms[:-1] + [kf, p.terms[-1]]
    p.step("3.1.40")


def am_pratyaya_lot(p: Prakriya):
    _, dhatu = p.find_last(T.DHATU)
    la = p.terms[-1]

    if dhatu.text == "vid" and dhatu.gana == 2 and la.any("lo~w"):
        if op.optional(_add_am, "3.1.41", p):
            # Derive by nipAtana
            dhatu.add_tags(T.F_GUNA_APAVADA)
            kf = Term.make_dhatu("qukf\\Y", 8)
            kf.text = "kf"
            kf.add_tags(T.DHATU)
            p.terms = p.terms[:-1] + [kf, p.terms[-1]]
            p.step("3.1.40")


def sarvadhatuka_vikarana(p: Prakriya):
    _, dhatu = p.find_last(T.DHATU)
    tin = p.terms[-1]

    kartari = p.all(T.KARTARI)

    if not kartari:
        _add("3.1.67", p, "yak")
        return

    # Optional cases
    gana_4_declined = False
    if dhatu.text in {"BrAS", "BlAS", "Bram", "kram", "klam", "tras", "truw", "laz"}:
        used_option = op.optional(_add, "3.1.70", p, "Syan")

        # Needed to make 3.1.69 available to roots like Bram
        if (not used_option) and dhatu.gana == 4:
            gana_4_declined = True

    # TODO: anupasarga
    elif dhatu.u == "yasu~":
        op.optional(_add, "3.1.71", p, "Syan")
    elif dhatu.u == "akzU~":
        op.optional(_add, "3.1.75", p, "Snu")
    elif dhatu.u == "takzU~":
        op.optional(_add, "3.1.76", p, "Snu")
    elif dhatu.u in ("sta\\nBu~", "stu\\nBu~", "ska\\nBu~", "sku\\nBu~", "sku\\Y"):
        op.optional(_add, "3.1.82", p, "Snu")

    _, added_vikarana = p.find_first(T.VIKARANA)
    if added_vikarana:
        return

    if dhatu.gana == 4 and not gana_4_declined:
        _add("3.1.69", p, "Syan")
    elif dhatu.gana == 5 or dhatu.text == "Sru":
        if dhatu.text == "Sru":
            dhatu.text = "Sf"
            _add("3.1.74", p, "Snu")
        else:
            _add("3.1.73", p, "Snu")
    elif dhatu.gana == 6:
        _add("3.1.77", p, "Sa")
    elif dhatu.gana == 7:
        dhatu.add_tags("Snam")
        op.mit("3.1.78", p, dhatu, "na")
    elif dhatu.gana == 8 or dhatu.u == "qukf\\Y":
        _add("3.1.79", p, "u")
    elif dhatu.u in ("Divi~", "kfvi~"):
        dhatu.text = dhatu.text[:-1] + "a"
        _add("3.1.80", p, "u")
    elif dhatu.gana == 9:
        _add("3.1.81", p, "SnA")
    else:
        _add("3.1.68", p, "Sap")


def optional_rule(rule: str, p: Prakriya):
    if p.allow(rule):
        return rule
    else:
        p.decline(rule)
        return None


def vikarana_lopa(p: Prakriya):
    """For certain roots and gaNas, delete the vikaraNa.

    (2.4.72 - 2.4.82)
    """

    # TODO: extend this to other pratyayas -- should properly be pratyaya_lopa
    _, dhatu = p.find_last(T.DHATU)
    _, vikarana = p.find_first(T.VIKARANA)
    tin = p.terms[-1]

    if not vikarana:
        return

    if vikarana.u == "Sap":
        if dhatu.gana == 2:
            op.luk("2.4.72", p, vikarana)
        elif dhatu.gana == 3:
            op.slu("2.4.75", p, vikarana)
    elif vikarana.u == "si~c" and tin.all(T.PARASMAIPADA):
        luk = aluk = None
        if dhatu.text in {"GrA", "De", "So", "Co", "so"}:
            # De takes luk by 2.4.77, so this allows aluk.
            if dhatu.text == "De":
                aluk = optional_rule("2.4.78", p)
            # Other roots avoid luk by default, so this allows luk.
            else:
                luk = optional_rule("2.4.78", p)

        # Run only if aluk was not used above.
        if (not aluk) and (
            dhatu.text in {"sTA", "BU"}
            or (dhatu.text == "gA" and dhatu.gana == 2)
            or (dhatu.text == "pA" and dhatu.gana == 1)
            or dhatu.all(T.GHU)
        ):
            luk = "2.4.77"

        assert not (luk and aluk)
        if luk:
            op.luk(luk, p, vikarana)
        elif aluk:
            p.step(aluk)
    elif vikarana.u == "si~c" and tin.text in {"ta", "TAs"}:
        if dhatu.u in TAN_ADI:
            op.optional(op.luk, "2.4.79", p, vikarana)


def run(p: Prakriya):
    tin = p.terms[-1]

    if tin.any("lf~w", "lf~N", "lu~w"):
        if tin.any("lf~w", "lf~N"):
            _add("3.1.33", p, "sya")
        else:
            _add("3.1.33", p, "tAsi~")
    elif tin.any("lu~N"):
        lun_vikarana(p)
    elif tin.any("li~w"):
        am_pratyaya_lit(p)
    else:
        if tin.any("lo~w"):
            # Just for vidāṅkurvantu, etc.
            am_pratyaya_lot(p)
        if tin.all(T.SARVADHATUKA):
            sarvadhatuka_vikarana(p)

    _, vikarana = p.find_first(T.VIKARANA)
    if vikarana:
        vikarana_lopa(p)
        # Run it-samjna-prakarana only after the lopa phase is complete.
        if vikarana.text:
            it_samjna.run_no_index(p, vikarana)

    # HACK for gAN gatau (bhvAdi). The long A should be handled early because
    # it blocks `AtmanepadezvanataH` and `Ato GitaH`.
    try:
        p.debug(p.terms[-3].text, p.terms[-2].text)
        if p.terms[-3].text == "gA" and p.terms[-2].text == "a":
            p.terms[-2].text = ""
            p.step("6.1.101")
    except IndexError:
        pass
