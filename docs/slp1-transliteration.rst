SLP1 Transliteration
====================

Padmini uses SLP1 transliteration internally. We use SLP1 for the following
reasons: 

- Each sound is represented by exactly one character, which means we can more
  easily check a string's sounds. Thus a string's first sound is ``s[0]``, its
  last sound with ``s[-1]``, its penultimate sound is ``s[-2]``, and so on.

- Each sound is represented in ASCII, which makes it faster and easier to write
  different sounds in a standard text editor. As illustration, Devanagari in
  particular renders horribly in my copy of Vim.

The full spec can be found `here`_, but we repeat it below for convenience::

    a A i I u U f F x X e E o O
    aM aH
    ka Ka ga Ga Na
    ca Ca ja Ja Ya
    wa Wa qa Qa Ra
    ta Ta da Da na
    pa Pa ba Ba ma
    ya ra la va
    Sa za sa ha

.. _here: https://www.sanskrit-lexicon.uni-koeln.de/talkMay2008/SLP1.pdf

SLP1 also supports anudātta (``\``), udātta (``/``), and svarita (``^``)
accents. For example, the first line of the Purusha Sukta is as follows in
SLP1::

    sa\ha/sra^SI/rzA\ pu/ru^z/aH

But because udātta accents are so frequent in the Ashtadhyayi, we do not write
them down, since doing so would just make the derivation state harder to read.
That is, we use only the ``\`` (anudātta) and ``^`` (svarita) marks, and if a
vowel does not have an explicit accent, it is udātta.
