# Must follow atidesha for kit-Nit of suffixes

from padmini import filters as f
from padmini import operations as op
from padmini.prakriya import Prakriya, Term
from padmini.constants import Tag as T
from padmini.term_views import TermView
from padmini.dhatu_gana import YAJ_ADI


def is_vaci_svapi(dhatu: Term):
    return (
        dhatu.u in ("va\\ca~", "Yizva\\pa~")
        or dhatu.u in YAJ_ADI
        # adesha for brUY
        or (dhatu.u == "va\\ci~")
    )


def vaci_svapi_samprasarana(rule, p: Prakriya, t: Term):
    # HACK: hacky samprasarana
    before = (
        "vac",
        "svap",
        "yaj",
        "vap",
        "vah",
        "vas",
        "ve",
        "vye",
        "hve",
        "vad",
        "Svi",
    )
    after = ("uc", "sup", "ij", "up", "uh", "us", "u", "vI", "hU", "ud", "SU")
    assert len(before) == len(after)
    mapping = dict(zip(before, after))
    # HACK: hacky samprasarana
    if t.text in mapping:
        op.text(rule, p, t, mapping[t.text])


def is_grahi_jya(dhatu: Term):
    # vayi~ replaces ve\\Y in 2.4.41
    return dhatu.u in {
        "graha~^",
        "jyA\\",
        "vayi~",
        "vya\\Da~",
        "vaSa~",
        "vyaca~",
        "o~vrascU~",
        "pra\\Ca~",
        "Bra\\sja~^",
        # not sure how to handle "vay" root
        "vaya~\\",
    }


def grahi_jya_samprasarana(rule, p, t: Term):
    before = ("grah", "jyA", "vay", "vyaD", "vaS", "vyac", "vrasc", "praC", "Brasj")
    after = ("gfh", "ji", "uy", "viD", "uS", "vic", "vfSc", "pfC", "Bfsj")
    assert len(before) == len(after)
    mapping = dict(zip(before, after))
    # HACK: hacky samprasarana
    if t.text in mapping:
        op.text(rule, p, t, mapping[t.text])


def run_for_dhatu(p: Prakriya):
    i, dhatu = p.find_first(T.DHATU)
    if not dhatu:
        return

    n = TermView.make(p, i)
    assert n

    if n.all("k") and is_vaci_svapi(dhatu):
        if n.any("li~w") and dhatu.u == "ve\\Y":
            p.step("6.1.40")
        else:
            vaci_svapi_samprasarana("6.1.15", p, dhatu)

    elif f.is_knit(n) and is_grahi_jya(dhatu):
        grahi_jya_samprasarana("6.1.16", p, dhatu)
        if dhatu.text == "uy" and dhatu.u == "vayi~":
            op.optional(op.text, "6.1.39", p, dhatu, "uv")

    lit_yanoh = n.all("li~w") or n.terms[0].u == "yaN"

    # True iff n can cause dvitva.
    abhyasta_karana = n.any("li~w") or n.terms[0].u in {"san", "yaN", "Slu", "caN"}

    if lit_yanoh and dhatu.text == "pyAy":
        op.text("6.1.29", p, dhatu, "pI")
    elif lit_yanoh and dhatu.text == "Svi":
        op.optional(op.text, "6.1.30", p, dhatu, "Su")
    elif dhatu.text == "hve" and abhyasta_karana:
        op.text("6.1.33", p, dhatu, "hu")


def run_for_abhyasa(p: Prakriya):
    i, dhatu = p.find_first(T.DHATU)
    if not dhatu:
        return

    n = TermView.make(p, i)
    if f.is_knit(n):
        return

    tin = p.terms[-1]
    if tin.all("li~w"):
        _, abhyasa = p.find_first(T.ABHYASA)
        if not abhyasa:
            return
        # yadā ca dhātorna bhavati tadā "liṭyabhyāsasya ubhayeṣām"
        # ityabhyāsasya api na bhavati -- kāśikā.
        if is_vaci_svapi(dhatu) and dhatu.text != "Svi":
            if n.any("li~w") and dhatu.u == "ve\\Y":
                p.step("6.1.40")
            else:
                vaci_svapi_samprasarana("6.1.17", p, abhyasa)
        elif is_grahi_jya(dhatu):
            grahi_jya_samprasarana("6.1.17", p, abhyasa)
