"""
angasya
~~~~~~~
(6.4.1 - end of 7.4)

Rules that modify the sounds and terms in an aṅga.

This section of the text is massive, so we break it down into several smaller
prakaraṇas.
"""

import re

from padmini import filters as f
from padmini import operations as op
from padmini import sounds
from padmini.constants import Tag as T
from padmini.dhatu_gana import PU_ADI, MUC_ADI, TRMPH_ADI
from padmini.prakriya import Prakriya, Term
from padmini.sounds import s
from padmini.stem_gana import PURVA_ADI, DATARA_ADI
from padmini.term_views import TermView, StringView

from . import abhyasasya
from . import asiddhavat
from . import it_agama
from . import sup_adesha


def jha_adesha(p: Prakriya):
    """Rules that modify the jha-pratyaya.

    (7.1.1 - 7.1.7)
    """
    last = p.terms[-1]

    if last.text in {"yu~", "vu~"}:
        if last.text == "yu~":
            op.text("7.1.1", p, last, "ana")
        else:
            op.text("7.1.1", p, last, "aka")

    elif last.adi in {"P", "Q", "K", "C", "G"}:
        subs = dict(zip("Ayan", "ey", "In", "Iy", "in"), "PQKCG")
        op.adi("7.1.2", p, last, subs[last.adi])

    elif last.adi == "J":
        ps = [t for t in p.terms[:-1] if t.text]
        prev = ps[-1]
        if prev.any(T.ABHYASTA):
            op.text("7.1.4", p, last, last.text.replace("J", "at"))
        elif prev.antya != "a" and last.all(T.ATMANEPADA):
            op.text("7.1.5", p, last, last.text.replace("J", "at"))
        else:
            op.text("7.1.3", p, last, last.text.replace("J", "ant"))

        if last.all(T.ATMANEPADA):
            if prev.u == "SIN":
                op.insert_agama_after_by_term("7.1.6", p, prev, "ru~w")
            elif prev.u == "vida~" and prev.gana == 2:
                op.optional(op.insert_agama_after_by_term, "7.1.7", p, prev, "ru~w")

    # -tAt substitution needs to occur early because it conditions samprasarana.
    elif last.all(T.TIN) and last.text in ("tu", "hi"):
        if p.allow("7.1.35"):
            # N is to block pit-guNa, not for replacement of the last letter.
            op.upadesha("7.1.35", p, last, "tAta~N")
        else:
            p.decline("7.1.35")


def pratyaya_adesha(p: Prakriya):
    """Rules that substitute the pratyaya.

    (7.1.1 - 7.1.35)
    """
    tin = p.terms[-1]
    if not tin.all(T.TIN):
        return

    ps = [t for t in p.terms[:-1] if t.text]
    prev = ps[-1]

    if prev.antya == "A" and tin.u == "Ral":
        op.upadesha("7.1.34", p, tin, "O")

    # Run 3.1.83 here because it has no clear place otherwise.
    if prev.u == "SnA" and tin.text == "hi" and ps[-2].antya in s("hal"):
        op.upadesha("3.1.83", p, prev, "SAnac")


def vrddhi_adesha(p: Prakriya, c: Term, n: TermView):
    if c.any(T.F_GUNA_APAVADA):
        return

    if c.text == "mfj" and not f.is_knit(n):
        c.text = "mArj"
        p.step("7.2.114")
    else:
        nnit_vrddhi(p, c, n)


def nnit_vrddhi(p: Prakriya, c: Term, n: TermView):
    """Vrddhi conditioned on following Nit-Yit

    (7.2.115 - 7.3.35)
    """
    if not (n and n.any("Y", "R") and n.all(T.PRATYAYA)):
        return

    if c.any(T.F_AT_LOPA, T.F_GUNA_APAVADA):
        # at-lopa prevents vrddhi
        return

    # HACK
    n.u = n.terms[0].u

    if not (f.can_use_guna(c, n) or n.u == "RiN"):
        return

    na = None
    if c.text in {"jan", "vaD"} and (n.u == "ciR" or n.all(T.KRT)):
        na = "7.3.35"

    if na:
        p.step(na)
    # By "acaH" we should ignore iko guNavRddhI (vye -> vivyAya)
    elif c.antya in s("ac"):
        op.antya("7.2.115", p, c, sounds.vrddhi(c.antya))
    elif c.upadha == "a":
        op.upadha("7.2.116", p, c, "A")


def guna_adesha(p: Prakriya, index: int):
    c = p.terms[index]
    if c.all(T.AGAMA):
        return

    if c.any(T.F_AT_LOPA, T.F_GUNA_APAVADA):
        # at-lopa prevents vrddhi
        return

    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    can_guna = f.can_use_guna(c, n)
    piti_sarvadhatuke = n.all("p", T.SARVADHATUKA)
    sarva_ardha = n.any(T.SARVADHATUKA, T.ARDHADHATUKA)

    if (
        c.antya == "u"
        and n.terms[0].any("luk")
        and n.adi in s("hal")
        and piti_sarvadhatuke
        and can_guna
    ):
        if c.u == "UrRuY":
            if p.allow("7.3.90"):
                p.step("7.3.90")
            else:
                p.decline("7.3.90")
                op.antya("7.3.89", p, c, sounds.vrddhi(c.antya))
        else:
            op.antya("7.3.89", p, c, sounds.vrddhi(c.antya))

    if c.text == "mid" and n.any("S"):
        c.add_tags(T.F_GUNA)
        op.text("7.3.82", p, c, "med")

    elif n.first_non_empty.u == "jus" and c.antya in s("ik"):
        c.add_tags(T.F_GUNA)
        op.antya("7.3.83", p, c, sounds.guna(c.antya))

    elif c.text == "tfnah" and n.adi in s("hal") and piti_sarvadhatuke:
        op.mit("7.3.92", p, c, "i")

    # General case
    elif can_guna and sarva_ardha and c.antya in s("ac"):
        if c.text == "jAgf" and n.terms[0].u not in {"kvip", "ciN"} and not n.any("N"):
            c.add_tags(T.F_GUNA)
            op.antya("7.3.85", p, c, "ar")
        elif c.text in {"BU", "sU"} and n.all(T.TIN, T.SARVADHATUKA, "p"):
            p.step("7.3.88")
        elif sounds.can_guna(c.antya):
            c.add_tags(T.F_GUNA)
            op.antya("7.3.84", p, c, sounds.guna(c.antya))

    # puganta-laghu-upadha (TODO: puk)
    elif can_guna and sarva_ardha and c.upadha in sounds.HRASVA:
        # HACK: Asiddhavat, but this blocks guna.
        # TODO: move this to asiddhavat and add no_guna tag.
        if c.text == "guh" and n and n.adi in s("ac"):
            op.upadha("6.4.89", p, c, "U")
        # Per commentary on 3.1.81, make an exception for dhinv and kRNv.
        elif c.u in ("Divi~", "kfvi~"):
            pass
        # e.g. nenijAma
        elif c.any(T.ABHYASTA) and n.all("p", T.SARVADHATUKA) and n.adi in s("ac"):
            p.step("7.3.87")
        elif sounds.can_guna(c.upadha) and c.upadha in sounds.HRASVA:
            c.add_tags(T.F_GUNA)
            op.upadha("7.3.86", p, c, sounds.guna(c.upadha))


def shiti(p: Prakriya, index: int):
    c = p.terms[index]
    ns = [u for u in p.terms[index + 1 :] if u.text]
    if not ns:
        return
    n = ns[0]

    if not n.all("S"):
        return

    if c.antya == "o" and n.u == "Syan":
        op.antya("7.3.71", p, c, "")

    sham_adi = (
        "Samu~",
        "tamu~",
        "damu~",
        "Sramu~",
        "Bramu~",
        "kzamU~",
        "klamu~",
        "madI~",
    )
    # Need gana check to avoid including Bramu~ from bhU-gaNa
    if c.u in sham_adi and n.u == "Syan" and c.gana == 4:
        c.text = c.text.replace("a", "A")
        p.step("7.3.74")

    pa_ghra = (
        "pA\\",
        "GrA\\",
        "DmA\\",
        "zWA\\",
        "mnA\\",
        "dA\\R",
        "df\\Si~r",
        "f\\",
        "sf\\",
        "Sa\\dx~",
        "za\\dx~",
    )

    # 7.3.78
    if c.all(T.DHATU) and c.u in pa_ghra and c.gana not in {2, 3}:
        piba_jighra = (
            "piba",
            "jiGra",
            "Dama",
            "tizWa",
            "mana",
            "yacCa",
            "paSya",
            "fcCa",
            "DO",
            "SIya",
            "sIda",
        )
        mapping = dict(zip(pa_ghra, piba_jighra))
        # sartervegitāyāṃ gatau dhāvādeśam icchanti। anyatra sarati, anusarati
        # ityeva bhavati. (kAzikA)
        if c.u == "sf\\":
            op.optional(op.text, "7.3.78", p, c, mapping[c.u])
        else:
            op.text("7.3.78", p, c, mapping[c.u])

    elif c.u in ("jYA\\", "janI~\\"):
        op.text("7.3.79", p, c, "jA")
    elif c.u in PU_ADI and c.gana in {5, 9}:
        c.text = c.text.replace("U", "u").replace("F", "f").replace("I", "i")
        p.step("7.3.80")

    # TODO: A-cam
    if c.text in ("zWiv", "klam"):
        c.text = op.yatha(c.text, ("zWiv", "klam"), ("zWIv", "klAm"))
        p.step("7.3.75")
    elif c.text == "kram" and p.terms[-1].all("parasmaipada"):
        op.text("7.3.76", p, c, "krAm")
    elif c.u in ("izu~", "ga\\mx~", "ya\\ma~"):
        op.antya("7.3.77", p, c, "C")


def num_agama(p: Prakriya, index: int):
    """Rules that add nu~m to the base.

    (7.1.58 - 7.1.83)

    :param p:
    :param index:
    """
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    last = p.terms[-1]
    if last.text == "Am":
        prev = p.terms[-2]
        if prev.all(T.SARVANAMA):
            op.insert_agama_before("7.1.52", p, last, "su~w")
        elif prev.text == "tri":
            op.text("7.1.53", p, "traya")
        # TODO: nadI, Ap
        elif f.is_hrasva(prev):
            op.insert_agama_before("7.1.54", p, last, "nu~w")
        elif prev.any(T.SAT) or prev.text == "catur":
            op.insert_agama_before("7.1.55", p, last, "nu~w")

    # 7.1.58 (idito nuM dhAtoH) is in `dhatu_karya`

    if c.u in MUC_ADI and n.terms[0].u == "Sa":
        op.mit("7.1.59", p, c, "n")
    elif c.u in TRMPH_ADI and n.terms[0].u == "Sa":
        op.mit("7.1.59.v1", p, c, "n")
    elif c.text in ("masj", "naS") and n.adi in s("Jal"):
        op.mit("7.1.60", p, c, "n")

    liti = n.any("li~w")
    if n.adi in s("ac"):
        if c.u in ("ra\\Da~", "jaBI~\\"):
            if c.u == "ra\\Da~" and f.is_it_agama(n.terms[0]) and not liti:
                p.step("7.1.62")
            else:
                op.mit("7.1.61", p, c, "n")
        elif c.u == "ra\\Ba~\\" and n.terms[0].u != "Sap" and not liti:
            op.mit("7.1.63", p, c, "n")
        elif c.u == "qula\\Ba~\\z" and n.terms[0].u != "Sap" and not liti:
            # TODO: 7.1.65 - 7.1.69
            op.mit("7.1.64", p, c, "n")

    if n.any(T.SARVANAMASTHANA):
        # TODO: aYc
        if c.any("u", "f") and not c.any(T.DHATU):
            op.mit("7.1.70", p, c, "n")
        if c.any(T.NAPUMSAKA) and n.adi in s("Jal ac"):
            op.mit("7.1.72", p, c, "n")
        if c.any in s("ik") and n.adi in s("ac") and n.any(T.VIBHAKTI):
            op.mit("7.1.73", p, c, "n")


def iit_agama(p: Prakriya):
    for index, _ in enumerate(p.terms):
        c = p.terms[index]
        n = TermView.make_pratyaya(p, index)

        if not c.text or not n:
            continue

        # Prevent loops
        # TODO: find a cleaner solution to this.
        if c.u == "Iw":
            return

        sarva = n.all(T.SARVADHATUKA)
        hali = n.adi in s("hal")
        if sarva and hali:
            piti = n.all("p")
            if piti and c.text == "brU":
                # i + 1 to skip luk
                op.insert_agama_after("7.3.93", p, index + 1, "Iw")
            elif piti and c.u == "yaN":
                op.optional(op.insert_agama_after, "7.3.94", p, index, "Iw")
            elif c.u in ("tu\\", "ru", "zwu\\Y", "Sam", "ama~"):
                op.optional(op.insert_agama_after, "7.3.95", p, index, "Iw")
            elif c.u in {"asa~", "si~c"} and f.is_aprkta(n):
                op.insert_agama_after("7.3.96", p, index, "Iw")

    _, dhatu = p.find_last(T.DHATU)
    if not dhatu:
        return
    last = p.terms[-1]
    if dhatu.u in {"rud", "svap", "Svas", "praR", "jakz"} and f.is_aprkta(last):
        if p.allow("7.3.99"):
            op.insert_agama_after("7.3.96", p, index, "Iw")
        else:
            p.decline("7.3.99")
            op.insert_agama_after("7.3.98", p, index, "Iw")


def lin_karya(p: Prakriya):
    tin = p.terms[-1]

    if not tin.all(T.SARVADHATUKA):
        return

    if tin.all("li~N"):
        anga = p.terms[-3]
        agama = p.terms[-2]
        assert agama.all(T.AGAMA)

        if "s" in agama.text or "s" in tin.text:
            agama.text = agama.text.replace("s", "")
            if tin.antya == "s":
                tin.text = tin.text.replace("s", "") + "s"
            else:
                tin.text = tin.text.replace("s", "")
            p.step("7.2.79")
        # yAs -> yA due to 7.2.79 above.
        if anga.antya == "a" and agama.text == "yA":
            op.text("7.2.80", p, agama, "Iy")

    # TODO: not sure where to put this. Not lin.
    prev = p.terms[-2]
    if prev.antya == "a" and tin.adi == "A" and tin.all("N"):
        op.adi("7.2.81", p, tin, "Iy")


def final_f_and_dirgha(p: Prakriya, index: int):
    c = p.terms[index]
    if not c.text:
        return
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    kniti = f.is_knit(n)
    akrtsarvadhatukayoh = not n.any(T.SARVADHATUKA, T.KRT)
    shayaklinksu = n.terms[0].u in {"Sa", "yak"} or (
        (p.terms[-1].all("li~N", T.ARDHADHATUKA) and n.adi == "y")
    )
    if c.antya == "f" and shayaklinksu and kniti:
        # nyAsa on 7.4.29:
        #
        #     `ṛ gatiprāpaṇayoḥ` (dhātupāṭhaḥ-936), `ṛ sṛ gatau`
        #     (dhātupāṭhaḥ-1098,1099) - ityetayor bhauvādika-
        #     jauhotyādikayor grahaṇam
        if f.samyogadi(c) or c.text == "f":
            op.antya("7.4.29", p, c, "ar")
        else:
            op.antya("7.4.28", p, c, "ri")
    elif akrtsarvadhatukayoh and (n.terms[0].u == "cvi" or n.adi == "y"):
        if c.antya == "f":
            op.antya("7.4.27", p, c, "rI")
        else:
            if n.terms[0].u == "cvi":
                op.antya("7.4.26", p, c, sounds.dirgha(c.antya))
            else:
                op.antya("7.4.25", p, c, sounds.dirgha(c.antya))


def nittva(p, index):
    c = p.terms[index]
    if not c.text:
        return
    try:
        n = p.terms[index + 1]
    except IndexError:
        return

    if c.text == "go" and n.all(T.SARVANAMASTHANA):
        op.tag("7.1.90", p, n, "R")
    elif c.antya == "o" and n.all(T.SARVANAMASTHANA):
        op.tag("7.1.90.v1", p, n, "R")
    elif n.u == "Ral" and n.all(T.UTTAMA):
        if p.allow("7.1.91"):
            n.remove_tags("R")
            p.step("7.1.91")
        else:
            p.decline("7.1.91")
    elif c.antya == "f" and n.u == "su~" and not n.any(T.SAMBUDDHI):
        op.antya("7.1.94", p, c, "an")


def run_for_each_2(p: Prakriya, index: int):
    terms = p.terms

    c = terms[index]
    if not c.text:
        return
    n = TermView.make_pratyaya(p, index)

    nittva(p, index)

    if n:
        kniti = n.any("k", "N")
        if c.u == "SIN":
            if kniti and n.adi == "y":
                op.antya("7.4.22", p, c, "ay")
            elif n.all(T.SARVADHATUKA):
                op.antya("7.4.21", p, c, sounds.guna(c.antya))

    # HACK: check for "dhatu" to avoid processing "yAs"-Agama
    # TODO: don't do this hack.
    if (
        c.antya == "s"
        and c.all(T.DHATU)
        and n
        and n.terms[0].adi == "s"
        and n.all(T.ARDHADHATUKA)
    ):
        op.antya("7.4.49", p, c, "t")

    if c.text == "tAs" or f.is_asti(c):
        if n.adi == "s":
            op.antya("7.4.50", p, c, "")
        elif n.adi == "r":
            op.antya("7.4.51", p, c, "")
        elif n.adi == "e":
            op.antya("7.4.52", p, c, "h")

    elif c.u in ("dIDIN", "vevIN") and n.adi in s("i u"):
        op.antya("7.4.53", p, c, "")

    # Must occur before guna and after 7.3.77 (gam -> gacC).
    samhitayam_tuk(p)

    # Vrddhi takes priority over guna. For example, Nic is Ardhadhatuka (guna)
    # and Nit (vrddhi), but it will cause vrddhi if possible.
    vrddhi_adesha(p, c, n)
    guna_adesha(p, index)

    # TODO: 7.4.23-4
    if n:
        final_f_and_dirgha(p, index)


def samhitayam_tuk(p: Prakriya):
    view = StringView(p.terms)
    vtext = view.text

    for match in re.finditer("[aiufx](C)", vtext):
        index = match.span(1)[0]
        term = view.term_for_index(index)
        if term.any(T.ABHYASA):
            # tena cicchadatuḥ, cicchiduḥ ityatra tukabhyāsasya grahaṇena na
            # gṛhyate iti halādiḥśeṣeṇa na nivartyate
            # -- kAzikA
            pass
        else:
            view[match.span(1)[0]] = "tC"
            p.step("6.1.73")

    match = re.search("[AIUFXeEoO](C)", vtext)
    if match:
        view[match.span(1)[0]] = "tC"
        p.step("6.1.75")


def cajoh_kuh(p: Prakriya, index: int):
    """Conversion of cu~ to ku~ in various contexts.

    (7.3.52 - 7.3.69)
    """
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    # HACK
    n.u = n.terms[0].u

    mapping = {"c": "k", "j": "g", "h": "G"}

    # TODO: do niyama only under the conditions below.
    niyama = None
    if c.adi in s("ku~"):
        niyama = "7.3.59"
    elif c.text in {"aj", "vraj"}:
        niyama = "7.3.60"
    # TODO: pra-vac
    elif c.text in {"yaj", "yAc", "ruc", "fc"} and n.u == "Ryat":
        niyama = "7.3.66"
    if niyama:
        p.step(niyama)
        return

    if c.antya in s("c j") and (n.any("G") or n.u == "Ryat"):
        op.antya("7.3.52", p, c, mapping[c.antya])
    elif c.text == "han":
        if n.any("Y", "R") or n.adi == "n":
            op.adi("7.3.54", p, c, "G")
        elif c.all(T.ABHYASTA):
            op.adi("7.3.55", p, c, "G")
    elif c.text == "hi" and c.all(T.ABHYASTA) and n.u != "caN":
        op.adi("7.3.56", p, c, "G")

    sanlitoh = n.u == "san" or n.all("li~w")
    if c.text == "ji" and c.gana == 1 and c.all(T.ABHYASTA) and sanlitoh:
        op.adi("7.3.57", p, c, "g")
    elif c.text == "ci" and c.all(T.ABHYASTA) and sanlitoh:
        op.optional(op.adi, "7.3.58", p, c, "k")


def dhatu_rt_adesha(p: Prakriya, index: int):
    c = p.terms[index]
    if not c.text and not c.all(T.DHATU):
        return

    if c.antya == "F":
        if c.upadha in s("pu~ v"):
            op.antya("7.1.102", p, c, "ur")
        else:
            op.antya("7.1.100", p, c, "ir")
    # HACK: 7.1.101 before dvitva


def ato_dirgha(p: Prakriya, index: int):
    """Lengthen -a of the anga when certain suffixes follow."""
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    n.u = n.terms[0].u

    if n.all(T.SARVADHATUKA):
        if c.antya == "a" and n.adi in s("yaY"):
            op.antya("7.3.101", p, c, "A")
    elif n.all(T.SUP):
        if c.antya == "a":
            if n.all(T.BAHUVACANA) and n.adi in s("Jal"):
                op.antya("7.3.103", p, c, "e")
            elif n.adi in s("yaY"):
                op.antya("7.3.102", p, c, "A")
            elif n.terms[0].text == "os":
                op.antya("7.3.104", p, c, "e")
        if c.antya in sounds.HRASVA and c.antya != "a":
            if n.any(T.SAMBUDDHI):
                op.antya("7.3.108", p, c, sounds.guna(c.antya))
            elif n.u == "jas":
                op.antya("7.3.109", p, c, sounds.guna(c.antya))
            elif c.antya == "f" and (n.u == "Ni" or n.any(T.SARVANAMASTHANA)):
                op.antya("7.3.110", p, c, sounds.guna(c.antya))
            elif c.any(T.GHI) and n.any("N"):
                op.antya("7.3.111", p, c, sounds.guna(c.antya))


def optional_rule(rule: str, p: Prakriya):
    if p.allow(rule):
        return rule
    else:
        p.decline(rule)
        return None


def sic_vrddhi(p: Prakriya):
    """sic-vrddhi applies only for parasmaipada endings.

    Must follow `it_agama` due to 7.2.4.

    (7.2.1 - 7.2.7)
    """
    try:
        i, dhatu = p.find_last(T.DHATU)
        if not dhatu:
            return

        tin = p.terms[-1]

        x, y = p.terms[i + 1 : i + 3]
        if x.u == "iw":
            it, sic = x, y
        else:
            it = None
            sic = x
    except (IndexError, ValueError):
        return

    if not (dhatu and sic.u == "si~c" and tin.all(T.PARASMAIPADA)):
        return

    # A dhatu followed by ArdhadhAtuka has its final `a` deleted by 6.4.48.
    # But in the context of the rules below, we should ignore the effect of
    # 6.4.48 per 1.1.57 (acaH parasmin pUrvavidhau) and cause no changes for
    # such roots. (Motivating examples: agopAyIt, avadhIt)
    if p.all(T.F_AT_LOPA):
        return

    # 1.2.1 -- skip vrddhi for these sounds
    # HACK: check only sic, atidesha should not apply to it.
    if (it and it.any("N")) or sic.any("N"):
        return

    if dhatu.upadha == "a" and dhatu.antya in s("l r"):
        # apavAda to 7.2.7 below, so run this first.
        op.upadha("7.2.2", p, dhatu, sounds.vrddhi(dhatu.upadha))
        return

    block_rule = None
    # TODO: don't add hack for tug-Agama. Should reorder.
    if it:
        # TODO: other cases
        if (
            dhatu.antya in s("h m y")
            or dhatu.text in {"kzaR", "Svas", "jAgf", "Svi"}
            or dhatu.all("e")
        ):
            block_rule = "7.2.5"
        elif dhatu.text == "UrRu":
            block_rule = optional_rule("7.2.6", p)
        elif dhatu.adi in s("hal") and dhatu.upadha == "a" and dhatu.antya != "C":
            block_rule = optional_rule("7.2.7", p)
        # Base case
        elif dhatu.antya in s("hal"):
            block_rule = "7.2.4"

    if block_rule:
        p.step(block_rule)
        return

    if dhatu.antya in s("ac"):
        op.antya("7.2.1", p, dhatu, sounds.vrddhi(dhatu.antya))
    elif f.samyoganta(dhatu):
        # 7.2.3 applies to the final vowel generally, even if samyoganta
        text = dhatu.text
        if text[-3] in s("ac"):
            dhatu.text = text[:-3] + sounds.vrddhi(text[-3]) + text[-2:]
        else:
            # e.g. "mansj", "pracC"
            dhatu.text = dhatu.text.replace("a", "A")
        p.step("7.2.3")
    else:
        op.upadha("7.2.3", p, dhatu, sounds.vrddhi(dhatu.upadha))


def cani_before_guna(p: Prakriya):
    index, c = p.find_first(T.DHATU)
    if not c:
        return

    try:
        nic = p.terms[index + 1]
        nici = nic.u in ("Ric", "RiN")
    except IndexError:
        nici = False
    try:
        can = p.terms[index + 2]
        cani = can.u == "caN"
    except IndexError:
        cani = False

    # 7.4.7 blocks guna.
    if c.upadha in s("f") and nici and cani:
        if p.allow("7.4.7"):
            c.add_tags(T.F_GUNA_APAVADA)
            op.upadha("7.4.7", p, c, "f")
        else:
            p.decline("7.4.7")

    last = p.terms[-1]
    if c.text in {"SF", "dF", "pF"} and last.any("li~w") and c.gana != 10:
        if p.allow("7.4.12"):
            c.add_tags(T.F_GUNA_APAVADA)
            op.antya("7.4.12", p, c, "f")
        else:
            p.decline("7.4.12")


def hacky_before_dvitva(p: Prakriya):
    cani_before_guna(p)

    for c in p.terms:
        if c.any(T.DHATU) and c.upadha == "F":
            op.upadha("7.1.101", p, c, "ir")


def cani_after_guna(p: Prakriya):
    """Rules conditioned on a following caN-pratyaya (luN-vikarana).

    (7.4.1 - 7.4.6)
    """
    index, c = p.find_first(T.DHATU)
    if not c:
        return

    try:
        nic = p.terms[index + 1]
        has_agama = False
        if nic.any(T.AGAMA):
            has_agama = True
            nic = p.terms[index + 2]
            can = p.terms[index + 3]
        else:
            can = p.terms[index + 2]
    except IndexError:
        return

    if nic.u not in ("Ric", "RiN"):
        return
    if can.u != "caN":
        return

    # Ignore 'f' because it is handled by 7.4.7.
    if c.upadha in s("ac") and c.upadha not in s("f"):
        res = sounds.hrasva(c.upadha)
        if c.any(T.F_AT_LOPA) or c.text == "SAs" or c.any("f"):
            p.step("7.4.2")
        elif res != c.upadha:
            op.upadha("7.4.1", p, c, res)
    elif has_agama and c.antya in s("ac"):
        # HACK for agama
        res = sounds.hrasva(c.antya)
        op.antya("7.4.1", p, c, res)


def liti(p: Prakriya):
    """Rules conditioned on a following liT-pratyaya.

    (7.4.9 - 7.4.12)
    """
    index, c = p.find_first(T.DHATU)
    tin = p.terms[-1]
    if not tin.all("li~w"):
        return

    if c.antya == "f" and f.samyogadi(c) and not tin.all("R"):
        c.add_tags(T.F_GUNA)
        op.antya("7.4.10", p, c, "ar")
    elif c.u == "fCa~":
        c.add_tags(T.F_GUNA)
        op.adi("7.4.11", p, c, "ar")
    elif c.antya == "F" or c.u == "f\\" and not tin.all("R"):
        c.add_tags(T.F_GUNA)
        op.antya("7.4.12", p, c, "ar")


def ani(p: Prakriya):
    """Rules conditioned on a following aN-pratyaya (luN-vikarana)

    (7.4.16 - 7.4.20)
    """
    index, c = p.find_last(T.DHATU)
    if not c:
        return
    n = p.terms[index + 1]

    if n.u != "aN":
        return

    if c.antya in s("f") or c.text == "dfS":
        if c.text == "dfS":
            op.text("7.4.16", p, c, "darS")
        else:
            op.antya("7.4.16", p, c, "ar")
    elif c.u == "asu~":
        op.insert_agama_after("7.4.17", p, index, "Tu~k")
    elif c.text == "Svi":
        op.antya("7.4.18", p, c, "a")
    elif c.text == "pat":
        op.mit("7.4.19", p, c, "p")
    elif c.text == "vac":
        op.mit("7.4.20", p, c, "u")


def ksasya(p: Prakriya):
    index, dhatu = p.find_last(T.DHATU)
    if not dhatu:
        return
    c = p.terms[index + 1]

    if c.u != "ksa":
        return

    n = p.terms[index + 2]
    if n.adi in s("ac"):
        op.antya("7.3.72", p, c, "")
    if dhatu.text in {"duh", "dih", "lih", "guh"} and n.all(T.ATMANEPADA):
        op.optional(op.antya, "7.3.73", p, c, "")


def nau(p: Prakriya, index: int):
    c = p.terms[index]
    n = TermView.make_pratyaya(p, index)
    if not n:
        return

    n.u = n.terms[0].u
    if n.u not in {"Ric", "RiN"}:
        return

    # HACK: avoid adding augments for ajAdi-dvitva.
    if n.any(T.ABHYASA):
        return

    if c.text in {"f", "hrI", "vlI", "rI", "knUy", "kzmAy"} or c.antya == "A":
        op.insert_agama_after_by_term("7.3.36", p, c, "pu~k")
    elif c.text in {"zA", "DA", "sA", "hvA", "vyA", "pA", "pE"} or c.u == "ve\\Y":
        do = True
        if c.u == "ve\\Y":
            if op.optional(op.insert_agama_after_by_term, "7.3.38", p, c, "ju~k"):
                do = False
        if do:
            op.insert_agama_after_by_term("7.3.37", p, c, "yu~k")
    elif c.text == "pA" and c.gana == 2:
        op.insert_agama_after_by_term("7.3.37.v1", p, c, "lu~k")
    # TODO: 7.3.39
    elif c.text in {"prI", "DU"}:
        # Optional per Haradatta (see commentary on prIY in siddhAnta-kaumudI)
        op.optional(op.insert_agama_after_by_term, "7.3.37.v2", p, c, "nu~k")
    # TODO: 7.3.39
    elif c.text == "BI":
        op.optional(op.insert_agama_after_by_term, "7.3.40", p, c, "zu~k")
    elif c.text == "sPAy":
        op.antya("7.3.41", p, c, "v")
    elif c.text == "Sad":
        op.optional(op.antya, "7.3.42", p, c, "t")
    elif c.text == "ruh":
        op.optional(op.antya, "7.3.43", p, c, "p")


def vibhaktau(p: Prakriya):
    sup = p.terms[-1]
    if not sup.all(T.SUP):
        return
    stem = p.terms[-2]

    if stem.text == "rE" and sup.adi in s("hal"):
        op.antya("7.2.85", p, stem, "A")
    elif stem.text in {"yuzmad", "asmad"}:
        if sup.adi in s("ac"):
            op.antya("7.2.89", p, stem, "y")
        elif sup.text:
            op.antya("7.2.86", p, stem, "A")
        elif sup.all(T.V2):
            op.antya("7.2.87", p, stem, "A")
        elif sup.all(T.V1, T.DVIVACANA):
            op.antya("7.2.88", p, stem, "A")
        else:
            op.antya("7.2.90", p, stem, "")


def run_remainder(p: Prakriya):
    sup_adesha.run(p)
    pratyaya_adesha(p)
    vibhaktau(p)

    # ksasya must run lin_karya so that at-lopa takes effect and prevents
    # "ato yeyaH"
    ksasya(p)
    # 7.2.79 - 7.2.81
    lin_karya(p)

    for index, _ in enumerate(p.terms):
        shiti(p, index)

    # Must come before asiddhavat rule 6.4.78 (e.g. "iyarti", ekahalmadhya)
    abhyasasya.run(p)

    index = 0
    while index < len(p.terms):
        has_at = p.any(T.F_AT_AGAMA)
        asiddhavat.run_before_guna(p, index)
        # Added at-Agama -- this causes a frame shift. Correct the pointer.
        if p.any(T.F_AT_AGAMA) != has_at:
            index += 1

        # num-Agama must come after asiddhavat rule 6.2.24, which causes na-lopa.
        num_agama(p, index)
        index += 1

    sic_vrddhi(p)

    for index, _ in enumerate(p.terms):
        nau(p, index)
        cajoh_kuh(p, index)
        run_for_each_2(p, index)

    # Rules for various lun-vikaranas.
    liti(p)
    ani(p)

    # Asiddhavat must run before cani for "Ner aniTi"
    for index, _ in enumerate(p.terms):
        c = p.terms[index]
        if c.text:
            asiddhavat.run_nau(p, index)

    cani_after_guna(p)
    abhyasasya.run_sani_cani(p)

    for index, _ in enumerate(p.terms):
        c = p.terms[index]
        if not c.text:
            continue

        asiddhavat.run_after_guna(p, index)
        dhatu_rt_adesha(p, index)
        ato_dirgha(p, index)

    asiddhavat.run_dirgha(p)
