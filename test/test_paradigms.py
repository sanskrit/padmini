import itertools
import json

import pytest
from padmini.dhatupatha import load_dhatus
from padmini.prakarana import tin_pratyaya as tin
from .utils import run_all_permutations


dhatus = {f"{x.gana}.{x.number}": x for x in load_dhatus()}


def iter_paradigm_tests(filename):
    with open(filename) as f:
        test_data = []
        for datum in json.load(f):
            if isinstance(datum, str):
                continue

            padas = set()
            for item in datum["padas"]:
                padas.update(item.split(","))
            yield (datum["dhatu"], datum["la"], datum.get("tags", []), padas)


sarvadhatuka = iter_paradigm_tests("test/data/sarvadhatuka.json")


@pytest.mark.parametrize("dhatu_code, la, tags, padas", sarvadhatuka)
def test_sarvadhatuka(dhatu_code, la, tags, padas):
    actual = set()
    prakriya_map = {}

    for purusha, vacana in itertools.product(tin.PURUSHA, tin.VACANA):
        tags = {purusha, vacana}
        prakriyas = run_all_permutations(dhatu_code, la, tags)
        for p in prakriyas:
            prakriya_map[p.text] = p

    actual = set(prakriya_map.keys())

    # Debug print only for errors
    if padas != actual:
        for form in actual:
            if form not in padas:
                prakriya_map[form].debug_print()

    assert padas == actual


ardhadhatuka = iter_paradigm_tests("test/data/ardhadhatuka.json")


@pytest.mark.parametrize("dhatu_code, la, tags, padas", ardhadhatuka)
def test_ardhadhatuka(dhatu_code, la, tags, padas):
    actual = set()
    prakriya_map = {}

    for purusha, vacana in itertools.product(tin.PURUSHA, tin.VACANA):
        p_tags = {purusha, vacana} | set(tags)
        prakriyas = run_all_permutations(dhatu_code, la, p_tags)
        for p in prakriyas:
            prakriya_map[p.text] = p

    actual = set(prakriya_map.keys())

    # Debug print only for errors
    if padas != actual:
        for form in sorted(actual):
            prakriya_map[form].debug_print()

    assert padas == actual
