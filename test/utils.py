from typing import List

from padmini.ashtadhyayi import tinanta, subanta
from padmini.prakriya import Prakriya
from padmini.dhatupatha import load_dhatus


DHATUS = {f"{x.gana}.{x.number}": x for x in load_dhatus()}


class PrakriyaTree:
    """Manages optional derivations.

    During the derivation process, we might encounter *optional* rules that
    create a branch in the prakriya. `PrakriyaTree` manages these branches and
    checks that all possible branches have been generated.
    """

    def __init__(self):
        self.prakriya = None
        self.children = {}

    def add_prakriya(self, p: Prakriya):
        """Add a prakriya to the tree."""
        cur = self
        for option, result in p.options_seen:
            cur.children.setdefault((option, True), PrakriyaTree())
            cur.children.setdefault((option, False), PrakriyaTree())
            cur = cur.children[(option, result)]
        cur.prakriya = p

    def __iter__(self):
        stack = [(self, [])]
        while stack:
            cur, path = stack.pop()
            if not cur.children:
                yield (cur, path)
            for key, child in cur.children.items():
                stack.append((child, path[:] + [key]))

    def debug_print(self, indent=""):
        if self.prakriya:
            print(indent, self.prakriya.text)
        else:
            print(indent, "NONE")
        for k, v in self.children.items():
            print(indent, k)
            if v:
                v.debug_print(indent=indent + "  ")

    def next_missing(self):
        """Get the next options config to try."""
        for node, path in self:
            if not node.children and not node.prakriya:
                return dict(path)
        return None


def run_all_permutations(code, la, tags) -> List[Prakriya]:
    dhatu = DHATUS[code]
    tree = PrakriyaTree()

    p = tinanta(dhatu.upadesha, code, la, tags=tags.copy())
    p_orig = p
    tree.add_prakriya(p)

    next = tree.next_missing()
    loop_counter = 0
    while next:
        loop_counter += 1
        if loop_counter > 10:
            assert False, "infinite loop"
        options = dict(next)
        p = tinanta(dhatu.upadesha, code, la, tags=tags.copy(), options=options)
        assert p.options_seen
        tree.add_prakriya(p)
        next = tree.next_missing()

    return [x[0].prakriya for x in tree]


def all_subantas(stem, linga, tags) -> List[Prakriya]:
    tree = PrakriyaTree()

    p = subanta(stem, linga, tags=tags.copy())
    p_orig = p
    tree.add_prakriya(p)

    next = tree.next_missing()
    loop_counter = 0
    while next:
        loop_counter += 1
        if loop_counter > 10:
            tree.debug_print()
            assert False, "infinite loop"
        options = dict(next)
        p = subanta(stem, linga, tags=tags.copy(), options=options)
        assert p.options_seen
        tree.add_prakriya(p)
        next = tree.next_missing()

    return [x[0].prakriya for x in tree]
