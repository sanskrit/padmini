# final -A (laliTa, aluH vs laleTa)
# finac -> (avak)

import xml.etree.ElementTree as ET


def group_by_root(filename):
    xml = ET.parse(filename).getroot()
    results = {}

    for f in xml:
        if not f.tag == "f":
            continue
        # child_tags = {e.tag for e in f}

        form = f.attrib["form"]

        # Ignore forms that end with 'd' as dhaval does not have these.
        if form.endswith("d"):
            continue

        num = f.find("root").attrib["num"]
        if num not in results:
            results[num] = set()
        results[num].add(form)
    return results


dhaval = group_by_root("dhaval.xml")
padmini = group_by_root("padmini.xml")

# dhaval -> padmini
remap = {
    "01.0073": "01.0878",
    "01.0878": "01.0073",
    "01.0074": "01.0879",
    "01.0879": "01.0074",
    "01.0075": "01.0880",
    "01.0880": "01.0075",
    "01.0098": "01.0892",
    "01.0892": "01.0098",
    "01.0187": "01.1152",
    "01.1152": "01.0187",
    "01.0215": "01.0998",
    "01.0998": "01.0215",
    "01.0392": "01.0852",
    "01.0852": "01.0392",
    "01.0957": "01.0205",
    "01.0205": "01.0957",
    "02.0076": "02.0077",
    # loop of 3
    "01.1106": "01.0740",
    "01.0739": "01.1106",
    "01.0740": "01.0739",
    # Continue
    "06.0002": "06.0162",
    "06.0162": "06.0002",
    # Pair
    "01.1115": "01.1047",
    "01.1047": "01.1115",
    # Pair
    "01.0864": "01.1014",
    "01.1014": "01.0864",
    # Pair
    "01.0546": "01.1031",
    "01.1031": "01.0546",
    # Pair
    "01.0330": "01.0359",
    "01.0331": "01.0330",
    "01.0359": "01.0331",
}

# A small or one-off fix
rudh_nalopa = {
    "07.0010",
    "07.0016",
    "07.0020",
    "07.0021",
    "07.0022",
    "07.0023",
}
misc_issue = {
    "05.0008",  # avarIQvam
    "01.1133",
    "01.1138",  # sfp > srap
    "01.1157",  # yaj > yaz
    "01.0237",
    "10.0124",
    "10.0155",
    "10.0231",
    "07.0013",
    "10.0373",
    "08.0005",
    "08.0010",
    "01.0392",
    "01.0535",
    "01.0538",
    "01.0742",
    "01.0812",
    "01.0985",
    "01.0988",
    "01.1020",
    "01.1148",
    "04.0063",
    "04.0158",
    "06.0077",
    "09.0043",
    "05.0018",
    "05.0020",
    "06.0108",  # kutAdi
    "09.0036",  # Correct A aorist
    "01.1161",  # samprasarana
    "03.0001",  # zluvacca
    "03.0002",  # zluvacca
    "03.0003",  # zluvacca
    "03.0006",  # zluvacca
    "04.0034",  # vibhASA lIyateH
    "04.0025",  # jRR stambhu
    "05.0001",  # su 7.2.72
    "09.0020",  # DUY 7.2.72
    "02.0007",  # khyA
    "05.0028",  # tfp
    "09.0032",  # I Agama
    "02.0057",  # meyAt is correct
    "01.1114",  # anit root
    "09.0027",  # unknown error
    "03.0019",  # chaandasa
    "04.0075",  # sic kittva
    "04.0083",  # root in asit
    "06.0006",  # kfz, allowed by 7.2.3
    "06.0158",  # spfS, allowed by 7.2.3
    "06.0161",  # mfs, allowed by 7.2.3
    "04.0092",  # dfp, allowed by 7.2.3
    "04.0093",  # dfp, allowed by 7.2.3
    "01.1145",  # kfz, allowed by 7.2.3
    "01.1162",  # vyeyAt
    "01.1063",  # seyAt
    "03.0020",  # ki abhyastasya piti sarva
    "03.0021",  # kit abhyastasya piti sarva
    "03.0022",  # tur abhyastasya piti sarva
    "03.0023",  # Diz abhyastasya piti sarva
    "02.0028",  # optional It
    "02.0029",  # optional It
    "02.0038",  # optional It
    "01.1131",  # svanj
    "01.1081",  # svf, should remove svarzyAmi per comment on rddhanoH sye
    "01.1058",  # styai, vAnyasya (e)
    "01.1059",  # styai, vAnyasya (e)
    "01.1048",  # still in scope for 7.2.13
    "05.0007",  # still in scope for 7.2.13
    "06.0067",  # kuryAt disabled by 8.2.79
    "02.0004",  # duh, lugvA
    "02.0005",  # dih, lugvA
    "02.0006",  # lih, lugvA
    "01.1043",  # guh, lugvA
    "01.0737",  # grah
    "01.0756",  # should be vrddhi, seT
    "01.0792",  # uSa-vida-jAgR
    "01.0864",  # SarD is seT in Atmanepada
    "01.0865",  # syand is seT in Atmanepada
    "01.0866",  # kxp is aniT in parasmaipada
    "04.0077",  # reDaTuH
    "04.0090",  # randh num
    "04.0094",  # pushadi
    "04.0145",  # pushadi
    "05.0026",  # debitha
    "04.0056",  # should be vAvartAm
    "04.0067",  # vid not in vetti
    "07.0019",  # hinddhi
    "06.0037",  # trmpadi
    "06.0049",  # krta-crta (cart)
    "07.0008",  # krta-crta (Cart)
    "07.0009",  # krta-crta (tart)
}
# Anit ending in R. I believe these cannot use "itha".
thal_it_rt = {
    "01.1046",
    "01.1080",
    "01.1082",
    "01.1083",
    "01.1084",
    "01.1086",
    "01.1087",
    "01.1088",
    "01.1089",
    "01.1115",
    "05.0006",
    "05.0013",
    "05.0014",
    "05.0015",
    "06.0139",
}
# gupU-dhUpa etc.
aaya = {
    "01.0461",
    "01.0462",
    "01.0511",
    "06.0159",
}
# Extra support for vet roots
uudit = {
    "01.0050",
    "01.0434",
    "01.0510",
    "01.0736",
    "01.0744",
    "04.0103",
    "04.0157",
    "06.0012",
    "06.0073",
    "06.0074",
    "06.0075",
    "06.0076",
    "06.0146",
    "09.0058",
}
# upadha-na-lopa in ashir-lin
lin_nalopa = {
    "01.0044",
    "01.0048",
    "01.0220",
    "01.0228",
    "01.0499",
}
# dvitva for mIMAmsate, etc.
man_badha = {
    "01.1125",
    "01.1126",
    "01.1127",
    "01.1128",
    "01.1149",
    "01.1150",
}
# Issue with SanskritVerb jha -> anta
jha_anta = {
    "02.0009",
    "02.0025",
    "02.0010",
    "02.0003",
    "02.0008",
    "02.0011",
    "02.0013",
    "02.0014",
    "02.0015",
    "02.0016",
    "02.0017",
    "02.0018",
    "02.0019",
    "02.0020",
    "02.0021",
    "02.0022",
    "02.0023",
    "02.0024",
    "02.0026",
    "02.0071",
    "02.0072",
    "02.0076",
    "02.0041",
    "09.0004",
    "03.0007",
    "03.0008",
    "03.0010",
    "03.0012",
    "03.0013",
    "03.0014",
    "07.0001",
    "07.0002",
    "07.0003",
    "07.0004",
    "07.0005",
    "07.0006",
    "07.0007",
    "07.0011",
    "07.0012",
    "09.0001",
    "09.0002",
    "09.0003",
    "09.0005",
    "09.0011",
    "09.0012",
    "09.0013",
    "09.0014",
    "09.0015",
    "09.0016",
    # also Dhva
    "09.0017",
    "09.0018",
    "09.0019",
    "09.0045",
    "09.0071",
}
# Optional ciN-lun for dIpa-jana-...
dipa_jana = {
    "01.1016",
    "01.0561",
    "01.0562",
    "04.0044",
    "04.0045",
    "04.0046",
    "04.0068",
}
# Optional can form with 'a' reduplication
can_ur_rt = {
    "10.0028",
    "10.0228",
    "10.0260",
    "10.0278",
    "10.0312",
    "10.0313",
    "10.0339",
    "10.0344",
    "10.0351",
    "10.0353",
    "10.0355",
    "10.0356",
    "10.0357",
    "10.0358",
    "10.0387",
    "10.0388",
}
can_cha = {
    "10.0352",
    "10.0354",
    "10.0359",
    "10.0359",
    "10.0370",
}
# Issues related to whether something is kutAdi or not.
kutadi = {
    "01.0351",
    "01.0390",
    "01.0500",
    "01.0846",
    "06.0107",
    "06.0110",
    "06.0111",
    "06.0119",
    "06.0120",
    "06.0123",
    "06.0124",
    "06.0130",
    "06.0135",
    "06.0137",
}
# SanskritVerb has a > i which looks like a chaandasa form.
at_it_chandasa = {
    "03.0015",
    "03.0016",
    "03.0018",
    "03.0026",
}
# various roots affected by aglopa
# - dvitva change (i --> a)
# - no hrasva
# - no guna
aglopa = {
    "10.0408",
    "10.0414",
    "10.0430",
    "10.0433",
    "10.0447",
    "10.0460",
    "10.0468",
    "10.0471",
    "10.0473",
    "10.0474",
}
# Curadi vowel length mismatch
curadi_vowel = {
    "10.0018",
    "10.0019",
    "10.0027",
    "10.0063",
    "10.0216",
    "10.0218",
    "10.0240",
    "10.0248",
    "10.0297",
    "10.0360",
    "10.0121",
}
# Atmanepada / parasmaipada disagreement
pada_mismatch = {
    "01.0545",
    "01.1077",
    "01.1164",
    "10.0222",
    "10.0295",
    "04.0159",
    "10.0006",
    "10.0034",
    "10.0041",
    "10.0058",
    "10.0097",
    "10.0189",
    "10.0194",
    "10.0195",
    "10.0204",
    "10.0205",
    "10.0206",
    "10.0208",
    "10.0222",
    "10.0233",
    "10.0249",
    "10.0381",
    "10.0438",
}

# Unclear, needs more thinking
escalate = {
    "02.0034",
    "02.0069",
    "01.0507",
    "01.0508",
    "10.0386",
    "05.0010",
    # curadi optional
    "04.0013",
    "06.0053",
    "04.0127",
    "04.0128",
    "04.0137",
    "08.0002",
    "10.0281",
    "10.0372",
}
tanadi_tathasoh = {
    "08.0001",
    "08.0003",
    "08.0008",
    "08.0009",
}
sr_dr_unknown = {
    "01.0920",
    "03.0004",
    "09.0021",
    "09.0022",
    "09.0026",
}
lit_et = {
    "09.0046",
    "09.0048",
    "09.0049",
}
# Root mismatch, no correspondence found
diff_roots = {
    "01.0621",
    "01.1110",
    "01.0105",
    "01.0730",
    "01.1098",
    "10.0056",
    "10.0108",
    "10.0322",
    "10.0462",
    "10.0487",
    "10.0008",
    "05.0038",
    "01.0922",
    "01.0923",
}
vrdbhyah = {
    "01.0862",
    "01.0863",
    "01.0864",
    "01.1014",
}
multi_gana_roots = {
    "01.0743",  # tanUkaraNe takSaH
    "06.0102",
    "09.0006",
    "09.0007",
    "09.0008",
    "09.0009",
    "09.0010",
}


def stringify(items):
    items = sorted(items)
    return ", ".join(items)


num_mismatches = 0
num_skipped = 0
total = 0
for key in sorted(dhaval.keys()):
    skips = [
        aaya,
        thal_it_rt,
        uudit,
        lin_nalopa,
        man_badha,
        diff_roots,
        lit_et,
        sr_dr_unknown,
        jha_anta,
        multi_gana_roots,
        dipa_jana,
        aglopa,
        escalate,
        pada_mismatch,
        curadi_vowel,
        at_it_chandasa,
        kutadi,
        can_ur_rt,
        can_cha,
        misc_issue,
        rudh_nalopa,
        vrdbhyah,
        tanadi_tathasoh,
    ]

    if any(key in skip for skip in skips):
        num_skipped += 1
        continue

    base = dhaval[key]
    test_key = remap.get(key, key)
    test = padmini.get(test_key, set())
    added = test - base
    label = f"{key}/{test_key}"
    if added:
        print(label, "+", stringify(added))

    removed = base - test
    if removed:
        print(label, "-", stringify(removed))
    if added or removed:
        num_mismatches += 1
        print()

    total += len(added) + len(removed)

num_matches = len(dhaval) - num_mismatches - num_skipped
print(f"{num_matches} roots match.")
print(f"{num_skipped} roots skipped (known error).")
print(f"{num_mismatches} roots do not match.")
print(f"{total} words do not match.")
