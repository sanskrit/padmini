from padmini.prakriya import Prakriya, VyakaranaException
from padmini.constants import Tag


class TermView:

    """A *view* groups multiple terms into a convenient unit so that they can
    be used together in rules. For example, consider the partial derivation
    below:

        dviz + (luk) yAs + s + t

    If `dviz` is the anga, we may wish to condition on the following sound from
    ``yAs``; on the presence or absence of ``luk``; on the semantics of `t`; or
    on various other properties. So we generalize this behavior into a single
    :class:`TermView`:

        dviz + [(luk) yAs + s + t]

    A :class:`TermView` and a :class:`Term` offer similar APIs. But whereas a
    :class:`Term` can be freely modified, a :class:`TermView` is generally
    read-only.

    If needed, we can always access its `terms` attribute to modify the
    specific terms. But if you want to add or remove terms, create a new
    :class:`TermView` instead.
    """

    def __init__(self, terms):
        assert terms
        self.terms = terms

    @staticmethod
    def make(p: Prakriya, index: int):
        terms = p.terms[index + 1 :]
        if not terms:
            return None
        if terms[0].any(Tag.DHATU):
            return TermView.make_dhatu(p, index + 1)
        elif terms[0].any(Tag.AGAMA, Tag.PRATYAYA):
            return TermView.make_pratyaya(p, index)
        elif terms[0].any(Tag.ABHYASA):
            return TermView.make_abhyasa(p, index)
        elif terms[0].any(Tag.UPASARGA):
            return TermView.make_upasarga(p, index)
        else:
            raise VyakaranaException(f"Unsupported term {terms[0]}")

    @staticmethod
    def make_views(p: Prakriya):
        """Partition all terms into views.

        :param p: the prakriya
        """
        i = 0
        terms = p.terms
        buf = []
        while i < len(terms):
            term = terms[i]
            buf.append(term)

            if term.any(Tag.AGAMA):
                pass

            elif term.any(Tag.PRATYAYA, Tag.ABHYASA):
                yield TermView(buf)
                buf = []

            elif term.any(Tag.DHATU):
                # Look ahead for next Agama (e.g. vu~k)
                try:
                    next = terms[i + 1]
                    if next.all(Tag.AGAMA, "k"):
                        buf.append(next)
                        i += 1
                except IndexError:
                    pass
                yield TermView(buf)
                buf = []
            else:
                raise VyakaranaException(f"Unknown type: {term}")
            i += 1

    @staticmethod
    def make_dhatu(p: Prakriya, index: int):
        buf = []
        for t in p.terms[index:]:
            if t.any(Tag.DHATU):
                buf.append(t)
            # Include Agamas
            elif buf and t.all(Tag.AGAMA, "k"):
                buf.append(t)
            else:
                break
        if buf:
            return TermView(buf)
        else:
            return None

    @staticmethod
    def make_abhyasa(p: Prakriya, index: int):
        return TermView([p.terms[index]])

    @staticmethod
    def make_upasarga(p: Prakriya, index: int):
        return TermView([p.terms[index]])

    @staticmethod
    def make_pratyaya(p: Prakriya, index: int):
        """Make a pratyaya :class:`View` by using the terms after `index`."""
        buf = []
        for t in p.terms[index + 1 :]:
            if t.any(Tag.AGAMA):
                buf.append(t)
            elif t.any(Tag.PRATYAYA):
                buf.append(t)
                if t.text:
                    return TermView(buf)
            else:
                return None
        return None

    @staticmethod
    def pratyaya2(p: Prakriya, index: int):
        """Make a pratyaya :class:`View` by using the terms after `index`."""
        buf = []
        for t in p.terms[index + 1 :]:
            if t.any(Tag.AGAMA):
                buf.append(t)
            elif t.any(Tag.PRATYAYA):
                buf.append(t)
                if t.text:
                    return TermView(buf)
            else:
                return None
        return None

    def __repr__(self):
        text_str = ", ".join(f"{t.text}:{t.u}" for t in self.terms)
        return f"TermView({text_str})"

    @property
    def adi(self):
        for t in self.terms:
            if t.text:
                return t.text[0]
        raise VyakaranaException("Empty view", self.terms)

    @property
    def antya(self):
        for t in self.terms[::-1]:
            if t.text:
                return t.text[-1]
        raise VyakaranaException("Empty view", self.terms)

    @property
    def text(self):
        return "".join(x.text for x in self.terms)

    @property
    def first_non_empty(self):
        for t in self.terms:
            if t.text:
                return t
        return None

    def all(self, *tags) -> bool:
        # Only check non-empty terms.
        for tag in tags:
            if any(t.all(tag) for t in self.terms if t.text):
                continue
            return False
        return True

    def any(self, *tags) -> bool:
        """Return whether any of the terms in this view has any of the tags in `tags`.

        :param tags: a list of tags
        :return:
        """
        for t in self.terms:
            if t.text and t.any(*tags):
                return True
        return False


class StringView:

    """Helper class that treats a prakriya like one string."""

    def __init__(self, terms):
        self.terms = terms

    @property
    def text(self):
        return "".join(x.text for x in self.terms)

    def delete_span(self, start, end):
        # Given:
        # - `start` is (before, in, after) the term.
        # - `end` is (before, in, after) the term.
        # - `end` always comes after `start`
        # We have six cases:
        # - (before, before)
        # - (before, in)
        # - (before, after)
        # - (in, in)
        # - (in, after)
        # - (after, after)
        terms = self.terms
        offset = 0
        for t in terms:
            len_t = len(t.text)
            # Clamp to prevent loop around to negative indices
            t_s = max(start - offset, 0)
            t_e = end - offset

            if t_s < len_t and t_e > 0:
                t.text = t.text[:t_s] + t.text[t_e:]

            offset += len_t

    def __getitem__(self, index):
        return self.text[index]

    def __setitem__(self, index, substitute):
        cur = 0
        for u in self.terms:
            delta = len(u.text)
            if cur <= index < cur + delta:
                offset = index - cur
                u.text = u.text[:offset] + substitute + u.text[offset + 1 :]
                return
            else:
                cur += delta

    def term_for_index(self, index):
        cur = 0
        for u in self.terms:
            delta = len(u.text)
            if cur <= index < cur + delta:
                return u
            else:
                cur += delta
        return None
