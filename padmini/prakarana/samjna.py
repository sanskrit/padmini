from padmini import operations as op
from padmini.constants import Tag as T
from padmini.prakriya import Prakriya
from padmini.sounds import s
from padmini.stem_gana import SARVA_ADI, USES_DATARA_DATAMA, PURVA_ADI, PRATHAMA_ADI


def pratipadika_samjna(p: Prakriya):
    sup = p.terms[-1]
    if not sup.any(T.SUP):
        return
    anga = p.terms[-2]

    if anga.text in SARVA_ADI or anga.text in USES_DATARA_DATAMA:
        do = True
        if anga.text in PURVA_ADI and sup.u == "jas":
            if p.allow("1.1.34"):
                do = False
                p.step("1.1.34")
            else:
                p.decline("1.1.34")
        if do:
            op.tag("1.1.27", p, anga, T.SARVANAMA)

    elif anga.text in PRATHAMA_ADI and sup.u == "jas":
        op.optional(op.tag, "1.1.33", p, anga, T.SARVANAMA)

    elif anga.antya in {"I", "U"} and anga.any(T.STRI):
        op.tag("1.4.3", p, anga, T.NADI)

    elif anga.antya in {"i", "u"} and anga.text != "saKi":
        op.tag("1.4.7", p, anga, T.GHI)


def sup_samjna(p: Prakriya):
    sup = p.terms[-1]
    if not sup.any(T.SUP):
        return
    anga = p.terms[-2]

    if p.any(T.SAMBODHANA):
        op.tag("2.3.48", p, sup, T.AMANTRITA)
        if p.any(T.EKAVACANA):
            op.tag("2.3.49", p, sup, T.SAMBUDDHI)

    if sup.u == "Si":
        op.tag("1.1.42", p, sup, T.SARVANAMASTHANA)
    elif sup.u in {"su~", "O", "jas", "am", "Ow"} and not anga.any(T.NAPUMSAKA):
        op.tag("1.1.43", p, sup, T.SARVANAMASTHANA)


def run_for_index(p: Prakriya, index: int):
    c = p.terms[index]

    if c.all(T.PRATYAYA):
        if c.all("li~w"):
            c.add_tags(T.ARDHADHATUKA)
            p.step("3.4.115")
        elif c.all("li~N") and p.all(T.ASHIH):
            c.add_tags(T.ARDHADHATUKA)
            p.step("3.4.116")
        elif c.any(T.TIN, "S"):
            if not c.all(T.SARVADHATUKA):
                c.add_tags(T.SARVADHATUKA)
                p.step("3.4.113")
        else:
            # Suffixes introduced before "dhAtoH" are not called ArdhadhAtuka.
            # So they will not cause guNa and will not condition iT-Agama.
            if c.all(T.F_NO_ARDHADHATUKA):
                pass
            elif not c.all(T.ARDHADHATUKA):
                c.add_tags(T.ARDHADHATUKA)
                p.step("3.4.114")


def run(p: Prakriya):
    for i, _ in enumerate(p.terms):
        run_for_index(p, i)
