"""
verb_lists
~~~~~~~~~~

Miscellaneous verb lists that are used by various rules.
"""


CUR_MIT = {
    "jYapa~",
    "yama~",
    "caha~",
    "capa~",
    "raha~",
    "bala~",
    "ciY",
}

KUSMADI = {
    "cita~",
    "daSi~",
    "dasi~",
    "dasa~",
    "qapa~",
    "qipa~",
    "tatri~",
    "matri~",
    "spaSa~",
    "tarja~",
    "Bartsa~",
    "basta~",
    "ganDa~",
    "vasta~",
    "hasta~",
    "vizka~",
    "hizka~",
    "nizka~",
    "lala~",
    "kURa~",
    "tURa~",
    "BrURa~",
    "SaWa~",
    "yakza~",
    "syama~",
    "gUra~",
    "Sama~",
    "lakza~",
    "kutsa~",
    "truwa~",
    "kuwa~",
    "gala~",
    "Bala~",
    "kUwa~",
    "kuwwa~",
    "vancu~",
    "vfza~",
    "mada~",
    "divu~",
    "gf",
    "vida~",
    "mana~",
    "mAna~",
    "yu",
    "kusma~",
}

GARVADI = {
    "pada",
    "gfha",
    "mfga",
    "kuha",
    "SUra",
    "vIra",
    "sTUla",
    "arTa",
    "satra",
    "garva",
}

#: Suffixes that follow the kuṭādi roots are treated as ṅit, which means that
#: they will not cause guṇa changes. The term kuṭādi refers to roots in the
#: tud-gaṇa starting with kuṭ and ending with kuṅ:
#:
#:     kuṭādayo'pi 'kuṭa kauṭilye' (tudādigaṇaḥ) ityetadārabhya yāvat
#:     kuṅ śabde (tudādigaṇaḥ) iti.
#:
#:     - kāśikā on 1.2.1 (via ashtadhyayi.com)
#:
#: I haven't found a full enumeration of this list, so I created the one below
#: by copying the items from ``dhatupatha.tsv``. But it seems that this list is
#: overspecified and includes some roots that shouldn't be. I've commented
#: these out as I've noticed them, but I'm sure there are more that should be.
#:
#: For usage, see 1.2.1.
KUT_ADI = {
    "kuwa~",
    "puwa~",
    "kuca~",
    "guja~",
    "guqa~",
    "qipa~",
    "Cura~",
    "sPuwa~",
    "muwa~",
    "truwa~",
    "tuwa~",
    "cuwa~",
    "Cuwa~",
    "juqa~",
    "juwa~",
    "kaqa~",
    "luwa~",
    "luWa~",
    "luqa~",
    "kfqa~",
    "kuqa~",
    "puqa~",
    "Guwa~",
    "tuqa~",
    "Tuqa~",
    "sTuqa~",
    "Kuqa~",
    "Cuqa~",
    "sPura~",
    "sPula~",
    "sPara~",
    "sPala~",
    "sPuqa~",
    "cuqa~",
    "vruqa~",
    "kruqa~",
    "Bfqa~",
    "huqa~",
    "gurI~\\",
    "RU",
    "DU",
    "gu\\",
    "Dru\\",
    "ku\\N",
    "kUN",
}

#: Roots from dyuta~ to kfpU~ in bhU-gaNa:
#:
#:     dyutādayastu kṛpū sāmarthye ityevaṃparyantāḥ (nyAsa)
#
#:     - nyāsa on 3.1.55 (via ashtadhyayi.com)
#:
#: For usage, see 1.3.91 and 3.1.55.
DYUT_ADI = {
    "dyuta~\\",
    "SvitA~\\",
    "YimidA~\\",
    "YizvidA~\\",
    "YikzvidA~\\",
    "ruca~\\",
    "Guwa~\\",
    "ruwa~\\",
    "luwa~\\",
    "luWa~\\",
    "uWa~\\",
    "SuBa~\\",
    "kzuBa~\\",
    "RaBa~\\",
    "tuBa~\\",
    "sransu~\\",
    "Dvansu~\\",
    "Bransu~\\",
    "BranSu~\\",
    "sranBu~\\",
    "vftu~\\",
    "vfDu~\\",
    "SfDu~\\",
    "syandU~\\",
    "kfpU~\\",
}

#: For usage, see 2.4.79 and 6.4.37.
TAN_ADI = {
    "tanu~^",
    "zanu~^",
    "kzaRu~^",
    "kziRu~^",
    "fRu~^",
    "tfRu~^",
    "GfRu~^",
    "vanu~\\",
    "manu~\\",
    "qukf\\Y",
}

#: Roots from puza~ to the end of div-Adi. This list refers specifically to
# ; the roots in divAdi:
#:
#:     puṣādirdivādyantargaṇo gṛhyate, na bhvādikryādyantargaṇaḥ
#
#:     - kāśikā on 3.1.55 (via ashtadhyayi.com)
#:
#: For usage, see 3.1.55.
PUSH_ADI = {
    "pu\\za~",
    "Su\\za~",
    "tu\\za~",
    "du\\za~",
    "Sli\\za~",
    "Sa\\ka~^",
    "zvi\\dA~",
    "kru\\Da~",
    "kzu\\Da~",
    "Su\\Da~",
    "zi\\Du~",
    "ra\\Da~",
    "Ra\\Sa~",
    "tf\\pa~",
    "df\\pa~",
    "dru\\ha~",
    "mu\\ha~",
    "zRu\\ha~",
    "zRi\\ha~",
    "Samu~",
    "tamu~",
    "damu~",
    "Sramu~",
    "Bramu~",
    "kzamU~",
    "klamu~",
    "madI~",
    "asu~",
    "yasu~",
    "jasu~",
    "tasu~",
    "dasu~",
    "vasu~",
    "basu~",
    "Basu~",
    "vyuza~",
    "vyusa~",
    "byusa~",
    "busa~",
    "vusa~",
    "pyuza~",
    "pyusa~",
    "puza~",
    "pluza~",
    "visa~",
    "bisa~",
    "kusa~",
    "kuSa~",
    "YizvidA~",
    "kzamU~z",
    "busa~",
    "musa~",
    "masI~",
    "samI~",
    "luwa~",
    "luWa~",
    "uca~",
    "BfSu~",
    "stima~",
    "BranSu~",
    "vfSa~",
    "kfSa~",
    "Yitfza~",
    "hfza~",
    "ruza~",
    "riza~",
    "qipa~",
    "kupa~",
    "gupa~",
    "yupa~",
    "rupa~",
    "lupa~",
    "zwupa~",
    "zwUpa~",
    "luBa~",
    "kzuBa~",
    "RaBa~",
    "tuBa~",
    "klidU~",
    "YimidA~",
    "YikzvidA~",
    "fDu~",
    "gfDu~",
}

#: Roots from yaja~ to the end of bhU-gaNa. These roots, along with vaca~ and
#: Yizvapa~, use samprasAraNa when followed by kit.
#:
#: For usage, see 6.1.15.
YAJ_ADI = {
    "ya\\ja~^",
    "quva\\pa~^",
    "va\\ha~^",
    "va\\sa~",
    "ve\\Y",
    "vye\\Y",
    "hve\\Y",
    "vada~",
    "wuo~Svi",
}

#: For usage, see 6.4.124.
PHAN_ADI = {
    "PaRa~",
    "rAjf~^",
    "wuBrAjf~\\",
    "wuBrASf~\\",
    "wuBlASf~\\",
    "syamu~",
    "svana~",
}

#: Roots from mucx~ to the end of the gaNa. These roots take num-Agama when
#: followed by Sa.
#:
#: For usage, see 7.1.59.
MUC_ADI = {
    "mu\\cx~^",
    "lu\\px~^",
    "vidx~^",
    "li\\pa~^",
    "zi\\ca~^",
    "kftI~",
    "Ki\\da~",
    "piSa~",
    # TODO: include Pul?
    # "Pula~",
}

#: For usage, see 7.1.59.v1.
TRMPH_ADI = {
    # TODO: exclude tfnpa?
    "tfnpa~",
    "tfnPa~",
    "tunpa~",
    "tunPa~",
    "dfnpa~",
    "dfnPa~",
    "fnPa~",
    "gunPa~",
    "unBa~",
    "SunBa~",
    "tfnhU~",
}

#: Roots from raDa~ to zRiha~. These roots use iT optionally in certain
#: circumstances:
#:
#:     radh naś tṛp dṛp druh muh ṣṇuh ṣṇih ebhyo valādyārdhadhātukasya veṭ syāt
#:
#:     - laghu kaumudI on 7.2.45 (via ashtadhyayi.com)
#:
#: For usage, see 7.2.45.
RADH_ADI = {
    "ra\\Da~",
    "Ra\\Sa~",
    "tf\\pa~",
    "df\\pa~",
    "dru\\ha~",
    "mu\\ha~",
    "zRu\\ha~",
    "zRi\\ha~",
}

#: Roots from pUY to plI:
#:
#:     pūñ-lūñ-stṝñ-kṝñ-vṝñ-dhūñ-śṝ-pṝ-vṝ-bhṝ-mṝ-dṝ-jṝ-jhṝ-dhṝ-nṝ-kṝ-ṝ-
#:     gṝ-jyā-rī-lī-vlī-plīnāṃ caturviṃśateḥ śiti hrasvaḥ
#:
#:     - laghu kaumudI on 7.3.80 (via ashtadhyayi.com)
#:
#: For usage, see 7.3.80.
PU_ADI = {
    "pUY",
    "lUY",
    "stFY",
    "kFY",
    "vFY",
    "DUY",
    "SF",
    "pF",
    "vF",
    "BF",
    "mF",
    "dF",
    "jF",
    "JF",
    "DF",
    "nF",
    "kF",
    "F",
    "gF",
    "jyA\\",
    "rI\\",
    "lI\\",
    "vlI\\",
    "vlI\\",
    "plI\\",
    # TODO: include blI?
    "blI\\",
}
