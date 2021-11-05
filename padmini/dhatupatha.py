from typing import NamedTuple, List
from padmini.prakriya import Term


class DhatupathaEntry(NamedTuple):
    upadesha: str
    gana: str
    number: str


def load_dhatus() -> List[DhatupathaEntry]:
    res = []
    with open("data/dhatupatha.tsv") as f:
        for line in f:
            line = line.strip()
            code, upadesha, meaning = line.split("\t")
            gana, number = code.split(".")
            if upadesha == "-":
                continue

            res.append(DhatupathaEntry(upadesha, gana, number))
    return res


def is_kutadi(term: Term):
    # Check number explicitly because some roots are duplicated within tudAdi
    # but outside this gana (e.g. juq).
    return term.gana == 6 and 93 <= term.number <= 137
