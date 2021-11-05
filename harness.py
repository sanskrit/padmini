from typing import NamedTuple, List

from padmini.ashtadhyayi import tinanta
from padmini.constants import Tag as T
from padmini.prakriya import Prakriya
from padmini.dhatupatha import load_dhatus
from test.utils import run_all_permutations


def _skip_step(self, rule):
    pass


Prakriya.step = _skip_step


LAKARA = [
    "la~w",
    "li~w",
    "lu~w",
    "lf~w",
    "lo~w",
    "la~N",
    "ashir-lin",
    "li~N",
    "lu~N",
    "lf~N",
]

TIN_LIST = [
    "tip",
    "tas",
    "Ji",
    "sip",
    "Tas",
    "Ta",
    "mip",
    "vas",
    "mas",
    "ta",
    "AtAm",
    "Ja",
    "tAs",
    "ATAm",
    "Dvam",
    "iw",
    "vahi",
    "mahiN",
]


def _to_xml(p: Prakriya, dhatu, la: str, tin: str) -> str:
    form = p.text
    root = dhatu.upadesha
    num = f"{dhatu.gana}.{dhatu.number}"
    if T.ASHIH in tags:
        la = "ASIrliN"
    else:
        la = la.replace("~", "")

    return f'<f form="{form}"><root name="{root}" num="{num}"/><{la}/><{tin}/></f>'


print('<!DOCTYPE forms SYSTEM "verbforms.dtd">')
print("<forms>")
for dhatu in load_dhatus():
    for la in LAKARA:
        tags = set()
        if la == "ashir-lin":
            la = "li~N"
            tags = {T.ASHIH}

        pairs = [
            (T.PRATHAMA, T.EKAVACANA),
            (T.PRATHAMA, T.DVIVACANA),
            (T.PRATHAMA, T.BAHUVACANA),
            (T.MADHYAMA, T.EKAVACANA),
            (T.MADHYAMA, T.DVIVACANA),
            (T.MADHYAMA, T.BAHUVACANA),
            (T.UTTAMA, T.EKAVACANA),
            (T.UTTAMA, T.DVIVACANA),
            (T.UTTAMA, T.BAHUVACANA),
        ]
        for i, (purusha, vacana) in enumerate(pairs):
            final_tags = {vacana, purusha} | tags

            code = f"{dhatu.gana}.{dhatu.number}"
            try:
                prakriyas = run_all_permutations(code, la, final_tags)
            except Exception:
                print("<error/>")
                continue
            for p in prakriyas:
                index = i
                if p.terms[-1].all(T.ATMANEPADA):
                    index += 9
                tin = TIN_LIST[index]
                print(_to_xml(p, dhatu, la, tin))
print("</forms>")
