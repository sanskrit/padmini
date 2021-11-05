import pytest
from padmini.constants import Tag as T
from .utils import run_all_permutations


def load_tests(filename):
    test_cases = []
    with open(filename) as f:
        for line in f:
            code, la, padas_str = line.strip().split()
            padas = set(padas_str.split(","))

            for p in padas_str.split(","):
                if p.endswith("t"):
                    padas.add(p[:-1] + "d")
            yield (code, la, padas)


def compare_forms(code, la, expected, tags):
    prakriyas = run_all_permutations(code, la, tags)
    actual = {p.text for p in prakriyas}

    if expected != actual:
        for p in prakriyas:
            p.debug_print()
            print()

    assert expected == actual


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lat.tsv"))
def test_lat_kartari(code, la, padas):
    tags = {T.PRATHAMA, T.EKAVACANA, T.KARTARI}
    compare_forms(code, la, padas, tags)


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lit.tsv"))
def test_lit_kartari(code, la, padas):
    tags = {T.PRATHAMA, T.EKAVACANA, T.KARTARI}
    compare_forms(code, la, padas, tags)


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lut.tsv"))
def test_lut_kartari(code, la, padas):
    # Use madhyama because it has distinct forms in parasmaipada/Atmanepada.
    tags = {T.MADHYAMA, T.EKAVACANA, T.KARTARI}
    compare_forms(code, la, padas, tags)


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lrt.tsv"))
def test_lrt_kartari(code, la, padas):
    tags = {T.PRATHAMA, T.EKAVACANA, T.KARTARI}
    compare_forms(code, la, padas, tags)


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lin-ashishi.tsv"))
def test_lin_ashishi_kartari(code, la, padas):
    assert la.startswith("a:")
    la = la.replace("a:", "")
    tags = {T.PRATHAMA, T.EKAVACANA, T.KARTARI, T.ASHIH}
    compare_forms(code, la, padas, tags)


@pytest.mark.parametrize("code,la,padas", load_tests("test/data/lun.tsv"))
def test_lun_kartari(code, la, padas):
    tags = {T.PRATHAMA, T.EKAVACANA, T.KARTARI}
    compare_forms(code, la, padas, tags)
