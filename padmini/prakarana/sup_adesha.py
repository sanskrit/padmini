from padmini import operations as op
from padmini.constants import Tag as T
from padmini.prakriya import Prakriya, Term
from padmini.stem_gana import DATARA_ADI, PURVA_ADI
from . import samjna


def adanta_sup_adesha(p: Prakriya):
    anga, sup = p.terms[-2:]
    if anga.antya != "a":
        return

    nasi_nyoh = {"Nasi~": "smAt", "Ni": "smin"}
    ta_nasi_nasam = {"wA": "ina", "Nasi~": "At", "Nas": "sya"}
    if sup.text == "Bis":
        if anga.text in {"idam", "adas"}:
            p.step("7.1.11")
        else:
            op.text("7.1.9", p, sup, "Es")

    elif anga.any(T.SARVANAMA) and sup.u in nasi_nyoh:
        do_sub = True
        if anga.text in PURVA_ADI:
            if p.allow("7.1.16"):
                p.step("7.1.16")
                do_sub = False
            else:
                p.decline("7.1.16")

        if do_sub:
            op.text("7.1.15", p, sup, nasi_nyoh[sup.u])

    if sup.u in ta_nasi_nasam and sup.text in {"A", "as"}:
        op.text("7.1.12", p, sup, ta_nasi_nasam[sup.u])

    elif sup.u == "Ne":
        if anga.any(T.SARVANAMA):
            op.text("7.1.14", p, sup, "smE")
        else:
            op.text("7.1.13", p, sup, "ya")

    elif anga.any(T.SARVANAMA) and sup.u == "jas":
        op.upadesha("7.1.17", p, sup, "SI")


def yusmad_asmad_sup_adesha(p: Prakriya):
    anga, sup = p.terms[-2:]
    if anga.text not in {"yuzmad", "asmad"}:
        return

    if sup.u == "Nas":
        op.text("7.1.27", p, sup, "a")
    elif sup.u == "Ne" or sup.any(T.PRATHAMA, T.DVITIYA):
        if sup.u == "Sas":
            p.step("7.1.29")
        else:
            op.text("7.1.28", p, sup, "am")
    elif sup.u == "Byas":
        if sup.any(T.PANCAMI):
            op.text("7.1.31", p, sup, "at")
        else:
            op.text("7.1.30", p, sup, "Byam")
    elif sup.all(T.PANCAMI, T.EKAVACANA):
        op.text("7.1.32", p, sup, "at")
    # TODO: 7.1.33


def ni_adesha(p, anga, sup):
    if sup.u == "Ni" and anga.antya in {"i", "u"}:
        op.text("7.3.118", p, sup, "O")
        if anga.any(T.GHI):
            op.antya("7.3.119", p, anga, "a")
    if anga.any(T.GHI) and sup.u == "wA" and not anga.any(T.STRI):
        op.text("7.3.120", p, sup, "nA")


def run(p: Prakriya):
    """(7.1.19 - 7.1.32)"""

    anga, sup = p.terms[-2:]
    if not sup.any(T.SUP):
        return

    ni_adesha(p, anga, sup)

    jas_shas = {"jas", "Sas"}
    if anga.u in {"dAp", "wAp", "cAp"} and sup.text == "O":
        op.upadesha("7.1.18", p, sup, "SI")

    elif anga.any(T.NAPUMSAKA) and sup.text == "O":
        op.upadesha("7.1.19", p, sup, "SI")

    elif anga.any(T.NAPUMSAKA) and sup.u in jas_shas:
        op.upadesha("7.1.20", p, sup, "Si")

    elif anga.text == "azwA" and anga.u == "azwan" and sup.u in jas_shas:
        op.upadesha("7.1.21", p, sup, "OS")

    elif anga.text == "zaz" and sup.u in jas_shas:
        op.luk("7.1.22", p, sup)

    elif anga.any(T.NAPUMSAKA) and sup.u in {"su~", "am"}:
        if anga.antya == "a":
            if anga.text in DATARA_ADI:
                op.text("7.1.25", p, sup, "adq")
            else:
                op.text("7.1.24", p, sup, "am")
        else:
            op.luk("7.1.23", p, sup)
    else:
        adanta_sup_adesha(p)

    yusmad_asmad_sup_adesha(p)

    # Add new samjnas
    samjna.sup_samjna(p)
