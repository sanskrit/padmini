import json

import pytest
from padmini.constants import Tag as T
from . import utils


SKIP = {
    # Skip irregular words for now.
    "viSvapA",
    "saKi",
    "susaKi",
    "pati",
    # In progress
    "payas",
}


def iter_paradigm_tests(filename):
    vibhaktis = [T.V1, T.V2, T.V3, T.V4, T.V5, T.V6, T.V7, T.V1]
    vacanas = [T.EKAVACANA, T.DVIVACANA, T.BAHUVACANA]
    lingas = {"pum": T.PUM, "napuMsaka": T.NAPUMSAKA, "strI": T.STRI}

    with open(filename) as f:
        test_data = []
        for datum in json.load(f):
            if isinstance(datum, str):
                continue

            all_padas = datum["padas"]
            stem = datum["stem"]
            linga = lingas[datum["linga"]]
            if stem in SKIP:
                continue

            for i, padas in enumerate(all_padas):
                vibhakti = vibhaktis[i // 3]
                vacana = vacanas[i % 3]
                tags = {vibhakti, vacana}
                if (i // 3) == 7:
                    tags.add(T.SAMBODHANA)
                # TODO: sambodhana
                padas = set(p for p in padas.split("/"))
                yield (stem, linga, tags, padas)


paradigms = iter_paradigm_tests("test/data/subanta.json")


@pytest.mark.parametrize("stem,linga,tags,expected", paradigms)
def test_paradigm(stem, linga, tags, expected):
    prakriyas = utils.all_subantas(stem, linga, tags)
    actual = {p.text for p in prakriyas}

    if expected != actual:
        for p in prakriyas:
            p.debug_print()
            print()

    assert expected == actual
