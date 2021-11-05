from padmini import operations as op


def test_yatha():
    before = ("tAs", "Tas", "Ta", "mip")
    after = ("tAm", "tam", "ta", "am")

    for i, b in enumerate(before):
        assert op.yatha(b, before, after) == after[i]


"""
def test_ti():
    assert S.ti("ta", "e") == "te"
    assert S.ti("AtAm", "e") == "Ate"


def test_antya():
    assert S.antya("ti", "u") == "tu"
    assert S.antya("te", "Am") == "tAm"
"""
