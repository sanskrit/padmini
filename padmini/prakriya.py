from dataclasses import dataclass
from typing import Dict, Set, List, Tuple, Optional

from padmini.constants import Tag


class VyakaranaException(Exception):
    pass


@dataclass
class Term:

    """A *term* is a generalized version of an *upadesha*. In addition to
    upadeshas, the *term* concept includes abhyāsas and any group of sounds
    that is not aupadeśika.

    :param u: The upadesha form of the term. If this is empty or missing,
        the term is not treated as an upadesha.
    :param text: The "visible" text of the term. At the end of the derivation,
        we join the text of all terms together to create our final word.
    :param tags: Any metadata associated with the term. Usually, this includes
        various samjnas. But it can also include past versions of the term
        (pratyayalope pratyayalakṣaṇam).
    :param gana: For dhātus, this is the gana. Since a given dhātu can appear
        in multiple ganas, we use this parameter to disambiguate.
    """

    #: The upadesha form of the term. If empty, this term is not an upadesha.
    u: str
    #: The "human-readable" form of the term, including any sound changes.
    text: str
    #: Any tags that apply to the term.
    tags: Set[str]
    #: If the :class:`Term` refers to a dhatu, the root's class.
    gana: Optional[int]
    number: Optional[int]

    @staticmethod
    def make_upadesha(upadesha):
        """Make an upadesha."""
        return Term(upadesha, upadesha, set(), None, 0)

    @staticmethod
    def make_dhatu(upadesha, gana, number=0):
        """Make a dhatu."""
        # `Tag.DHATU` will be added later through rule 1.3.1.
        return Term(upadesha, upadesha, set(), int(gana), int(number))

    @staticmethod
    def agama(raw):
        """Make an Agama."""
        # Add `Tag.AGAMA` now because it is not defined by any other rule.
        return Term(raw, raw, {Tag.AGAMA}, None, 0)

    @staticmethod
    def make_term(text):
        """Make a generic term (e.g. for dvitva)."""
        return Term("", text, set(), None, 0)

    @property
    def adi(self) -> Optional[str]:
        """Return the first sound."""
        try:
            return self.text[0]
        except IndexError:
            return None

    @property
    def antya(self) -> Optional[str]:
        """Return the last sound."""
        try:
            return self.text[-1]
        except IndexError:
            return None

    @property
    def upadha(self) -> Optional[str]:
        """Return the penultimate sound."""
        try:
            return self.text[-2]
        except IndexError:
            return None

    def get(self, index: int) -> Optional[str]:
        """Get a letter at the given index.

        We use this method for those rare rules that don't use
        Adi/antya/upadhA.
        """
        try:
            return self.text[index]
        except IndexError:
            return None

    def all(self, *tags) -> bool:
        for t in tags:
            if t not in self.tags:
                return False
        return True

    def any(self, *tags) -> bool:
        for t in tags:
            if t in self.tags:
                return True
        return False

    def add_tags(self, *tags):
        self.tags |= set(tags)

    def remove_tags(self, *tags):
        self.tags -= set(tags)


@dataclass
class Prakriya:

    """A *prakriya* is a derivation within the Paninian system. It adds,
    removes, and modifies various terms until the result is a valid Sanskrit
    word or expression.

    The :class:`Prakriya` object manages all of the state associated with a
    prakriya. When the prakriya is complete, the final result can be accessed
    through the `text` attribute.

    In addition, :class:`Prakriya` manages all of the state related to
    *optional* rules (rules declared with vA, vibhASA, anyatarasyAm, or in the
    opinion of some vaiyAkaraNa). This state makes it easy for calling code to
    try different permutations of options and generate all of the possible
    forms for some given input.

    :param terms: the derivation state. The program modifies this list and its
        members during execution. If you want to preserve the initial state,
        provide a deep copy instead.
    :param tags: any meta information that applies to the prakriya overall.
        This mainly contains semantic information (purusha, vacana) or sets the
        derivation context (chandasi). It is also used to manage "global" state
        that we cannot easily define on :class:`Tag` objects.
    :param history: the derivation history. This is a list of 2-tuples, where
        the first member is the current result and the second member is the
        rule we applied to get that result. If you want to log different
        information in the history, you can override the `step` method of this
        class.
    :param options_override: maps a rule code to whether the rule can be used
        or not. This mapping has meaning only for *optional* rules and is
        ignored for mandatory rules.
    :param options_seen: optional rules seen during the derivation. This is a
        list of 2-tuples, where the first member is the rule and the second is
        whether the rule was accepted or not.
    """

    terms: List[Term]
    tags: Set[str]
    history: List[Tuple[str, str]]
    options_override: Dict[str, bool]
    options_seen: List[Tuple[str, bool]]

    @classmethod
    def make(cls, terms: Optional[List[Term]] = None):
        """Convenience function to define a :class:`Prakriya`.

        :param terms: an optional list of :class:`Term`s.
        """
        return Prakriya(
            terms=terms or [],
            tags=set(),
            history=[],
            options_override={},
            options_seen=[],
        )

    @property
    def text(self):
        return "".join(t.text for t in self.terms)

    def find(self, func):
        """Return all terms that match the test function.

        :param func: the function to apply to each term.
        """
        return [u for u in self.terms if func(u)]

    def find_all(self, tag):
        for i, t in enumerate(self.terms):
            if t.any(tag):
                yield i, t

    def find_first(self, tag) -> Tuple[Optional[int], Optional[Term]]:
        for i, t in self.find_all(tag):
            return i, t
        return (None, None)

    def find_last(self, tag) -> Tuple[Optional[int], Optional[Term]]:
        last = (None, None)
        for pair in self.find_all(tag):
            last = pair
        return last

    def allow(self, code: str) -> bool:
        res = self.options_override.get(code)
        if res:
            self.options_seen.append((code, True))
        return res

    def decline(self, code: str):
        self.options_seen.append((code, False))

    def set_options(self, options):
        self.options_override = options

    def all(self, *tags: List[str]):
        return all(t in self.tags for t in tags)

    def any(self, *tags: List[str]):
        return any(t in self.tags for t in tags)

    def add_tags(self, *tags):
        self.tags |= set(tags)

    def step(self, rule):
        """Log the current derivation state.

        :param rule: the rule that was just applied.
        """
        text = " ".join(u.text or "_" for u in self.terms)
        self.history.append((text, rule))

    def debug(self, *a):
        self.step(a)

    def debug_print(self):
        for t in self.terms:
            print("  ", t)
        for text, rule in self.history:
            print(f"    {text} ({rule})")
        print()
