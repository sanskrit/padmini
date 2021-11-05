import functools

from enum import Enum
from typing import Dict


#: The Ashtadhyayi uses a special ordering of sounds that is optimized for the
#: needs of the grammar. The rules that define this ordering are popularly
#: called the Shiva Sutras.
#:
#: We use ``SHIVA_SUTRAS`` to interpret and create pratyāhāras. For details,
#: see :func:`pratyahara`.
SHIVA_SUTRAS = [
    ["a", "i", "u", "R"],
    ["f", "x", "k"],
    ["e", "o", "N"],
    ["E", "O", "c"],
    ["ha", "ya", "va", "ra", "w"],
    ["la", "R"],
    ["Ya", "ma", "Na", "Ra", "na", "m"],
    ["Ja", "Ba", "Y"],
    ["Ga", "Qa", "Da", "z"],
    ["ja", "ba", "ga", "qa", "da", "S"],
    ["Ka", "Pa", "Ca", "Wa", "Ta", "ca", "wa", "ta", "v"],
    ["ka", "pa", "y"],
    ["Sa", "za", "sa", "r"],
    ["ha", "l"],
]


class Sthana(Enum):

    """Defines the point of articulation of a sound."""

    #: Soft palate
    KANTHA = "kantha"
    #: Hard palate
    TALU = "talu"
    #: Alveolar ridge
    MURDHA = "murdha"
    #: Base of the teeth
    DANTA = "danta"
    #: Lips
    OSTHA = "ostha"
    #: Nose
    NASIKA = "nasika"
    #: Soft palate and hard palate
    KANTHA_TALU = "kantha-talu"
    #: Soft palate and lips
    KANTHA_OSTHA = "kantha-ostha"
    #: Teeth and lips
    DANTOSTHA = "dantostha"


class Ghosha(Enum):

    """Defines the voicing property of a sound."""

    #: Voiced
    GHOSHAVAT = "ghoshavat"
    #: Unvoiced
    AGHOSHA = "aghosha"


class Prana(Enum):

    """Defines the aspiration property of a sound."""

    #: Aspirated
    MAHAPRANA = "mahaprana"
    #: Unaspirated
    ALPAPRANA = "alpaprana"


class Prayatna(Enum):

    """Defines the articulatory effort of a sound."""

    #: Uncontacted
    VIVRTA = "vivrta"
    #: Slight contact
    ISHAT = "ishat"
    #: Full contact
    SPRSHTA = "sprshta"


class OrderedSet(set):

    """An ordered set of sounds."""

    def __init__(self, items):
        set.__init__(self, items)
        self.items = items
        self._regex = None

    def __repr__(self):
        return "OrderedSet({})".format(self.items)

    @property
    def regex(self):
        if not self._regex:
            self._regex = "[{}]".format("".join(self.items))
        return self._regex


@functools.cache
def _pratyahara(s: str, use_second_n=False) -> OrderedSet:
    """Internal function that defines a pratyāhāra.

    Each rule of the Shiva Sutras contains a list of sounds followed by a
    meta letter (*it*). The combination of initial letter and *it* letter,
    called a pratyāhāra, defines a sound class that includes the first sound
    and all sounds up to the *it* letter. For example, the ac-pratyāhāra
    defines all vowels.

    :func:`_pratyahara` receives the string definition of a pratyāhāra and
    returns the sounds it contains as an :class:`OrderedSet`.

    Client code should use the :func:`s` function, which is more general.

    Some examples::

        ac = _pratyahara('ac')
        assert all(vowel in ac for vowel in "aAiIuUfFxXeEoO")

        hal = _pratyahara('hal')
        assert all(cons in ac for cons in "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh")

    :param s: the pratyāhāra to create.
    :param use_second_n: if set, use the second ``R`` sound when forming
        the pratyāhāra.
    :return: an :class:`OrderedSet` of sounds
    """
    first, it = s[:-1], s[-1]

    started = False
    saw_first_n = False
    res = []
    for row in SHIVA_SUTRAS:
        for sound in row[:-1]:
            if first == sound:
                started = True
            if started:
                L = sound[0]
                res.append(L)

                # Add long vowels, which are not explictly included in the
                # Shiva Sutras.
                if L in "aiufx":
                    res.append(L.upper())

        if started and it == row[-1]:
            if use_second_n and not saw_first_n:
                saw_first_n = True
            else:
                break

    assert res, f'Pratyahara "{s}" is empty.'
    return OrderedSet(res)


@functools.cache
def savarna(s: str) -> OrderedSet[str]:
    """Defines a group of similar sounds.

    savarṇa sounds are defined and specified through the following rules:

    1.1.9 tulyāsyaprayatnaṃ savarṇam
    Sounds with the same oral articulation and effort are called savarṇa;

    1.1.10 nājjhalau
    But vowels and consonants are not (savarṇa to each other).

    1.1.60 aṇudit savarṇasya cāpratyayaḥ
    Vowels, semivowels, and (other consonants) with *u* as an *it* refer to
    all of their savarṇa sounds, if they are not *pratyaya*s.

    Example usage::

        ku = savarna('ku~')
        assert all(cons in ku for vowel in "kKgGN")

        a = savarna('a')
        assert all(vowel in a for vowel in "aA")

    :param s: the sound to use as a reference point
    :return: an :class:`OrderedSet` of sounds
    """

    groups = [
        "aA",
        "iI",
        "uU",
        "fFxX",
        "kKgGN",
        "cCjJY",
        "wWqQR",
        "tTdDn",
        "pPbBm",
    ]
    groups = [OrderedSet(g) for g in groups]
    mapping = {x: group for group in groups for x in group}
    return mapping.get(s, s)


@functools.cache
def s(terms: str) -> OrderedSet[str]:
    """Create an ordered set of Sanskrit sounds.

    The function understands the following sounds:

    - bare vowels (`"a i u"`)
    - udit (`"ku~"`)
    - pratyāhāras (`"ac hal"`)

    For convenience, all arguments can be passed in one string.

    The return value is a set so that membership checks are constant-time, and
    it is an :class:`OrderedSet` per *yathāsaṁkhyam anudeśaḥ samānām* (i.e.
    list substitution is done in 1:1 correspondence).

    Example usage::

        ik = s("ik")
        cavarga = s("cu~")
        kanthya = s("a ku~ h H")

    To use the second ``R`` of the pratyāhāra, use the following syntax::

        first_n = s("iR")
        second_n = s("iR2")

    :param terms: a string of upadeshas.
    :return: an :class:`OrderedSet` of sounds
    """
    ret = []
    for term in terms.split():
        if term.endswith("u~"):
            ret.extend(savarna(term[:-2]).items)
        elif term in "aiufxAIUFX":
            ret.extend(savarna(term).items)
        elif len(term) == 1:
            ret.append(term)
        elif term.endswith("2"):
            ret.extend(_pratyahara(term[:-1], use_second_n=True).items)
        else:
            ret.extend(_pratyahara(term).items)
    return OrderedSet(ret)


def guna(s: str) -> str:
    # 1.1.2 adeGguNaH
    # 1.1.3 iko guNavRddhI
    mapping = {
        "i": "e",
        "I": "e",
        "u": "o",
        "U": "o",
        "f": "ar",
        "F": "ar",
    }
    return mapping[s]


def vrddhi(s: str) -> str:
    # 1.1.1 vRddhidAdaic
    # 1.1.3 iko guNavRddhI
    mapping = {
        "a": "A",
        "A": "A",
        "I": "A",
        "i": "E",
        "I": "E",
        "u": "O",
        "U": "O",
        "f": "Ar",
        "F": "Ar",
        "x": "Ar",
        "X": "Ar",
        "e": "E",
        "E": "E",
        "o": "O",
        "O": "O",
    }
    return mapping[s]


def hrasva(s: str) -> str:
    # 1.1.48 UkAlojjhrasvadIrghaplutaH
    mapping = {
        "A": "a",
        "I": "i",
        "U": "u",
        "F": "f",
        "e": "i",
        "E": "i",
        "o": "u",
        "O": "u",
    }
    return mapping.get(s, s)


def dirgha(s: str) -> str:
    # 1.1.48 UkAlojjhrasvadIrghaplutaH
    mapping = {
        "a": "A",
        "i": "I",
        "u": "U",
        "f": "F",
        "x": "X",
    }
    return mapping.get(s, s)


def can_guna(sound: str) -> bool:
    return sound in s("ik")


HRASVA = set("aiufx")
DIRGHA = set("AIUFXeEoO")
GUNA = set("aeo")
VRDDHI = set("AEO")
MAHAPRANA = set("KGCJWQTDPBh")


def invert(d):
    ret = {}
    for k, vs in d.items():
        for v in vs:
            if v not in ret:
                ret[v] = set()
            ret[v].add(k)
    return ret


STHANA = invert(
    {
        Sthana.KANTHA: s("a ku~ h H"),
        Sthana.TALU: s("i cu~ y S"),
        Sthana.MURDHA: s("f wu~ r z"),
        Sthana.DANTA: s("x tu~ l s"),
        Sthana.OSTHA: s("u pu~"),
        Sthana.NASIKA: s("Yam M"),
        Sthana.KANTHA_TALU: s("e E"),
        Sthana.KANTHA_OSTHA: s("o O"),
        Sthana.DANTOSTHA: s("v"),
    }
)
GHOSHA = invert({Ghosha.GHOSHAVAT: s("ac") | s("haS"), Ghosha.AGHOSHA: s("Kar")})
PRANA = invert({Prana.MAHAPRANA: "KGCJWQTDPBh", Prana.ALPAPRANA: s("ac yam jaS car")})
PRAYATNA = invert(
    {
        Prayatna.ISHAT: s("yaR Sar"),
        Prayatna.VIVRTA: s("ac h"),
        Prayatna.SPRSHTA: s("Yay"),
    }
)
del invert


@functools.cache
def map_sounds_s(left: str, right: str) -> Dict[str, str]:
    return map_sounds(s(left), s(right))


def map_sounds(left: OrderedSet, right: OrderedSet) -> Dict[str, str]:
    """Map one sound group to another.

    Every Sanskrit sound has various properties, e.g.:

    - sthāna (point of articulation)
    - prayatna (articulatory effort)
    - ghoṣa (voicing)
    - prāṇa (aspiration),

    This function maps the sounds in `left` to their closest counterpart in
    `right`, per rule 1.1.50:

        1.1.50 *sthāne'ntaratamaḥ*

    :param left: the "input" side of the mapping.
    :param right: the "output" side of the mapping.
    :return: a mapping from each sound in `left` to its closest sound in
        `right`.
    """
    right_qs = []
    for r in right.items:
        right_q = GHOSHA[r] | PRANA[r] | STHANA[r] | PRAYATNA[r]
        right_qs.append((r, right_q))

    mapping = {}
    for L in left.items:
        left_q = GHOSHA[L] | PRANA[L] | STHANA[L] | PRAYATNA[L]

        best = None
        best_score = 999
        for r, right_q in right_qs:
            # The most similar sound is the one that is the least different.
            score = len(right_q - left_q) + len(left_q - right_q)
            if score < best_score:
                best = r
                best_score = score

        assert best
        mapping[L] = best
    return mapping
