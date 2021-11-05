Reading the Code
================

.. currentmodule:: padmini.prakriya

Padmini has a simple architecture. If you understand the core :class:`Term` and
:class:`Prakriya` data types, then all Padmini does is mutate these data
structures through ordinary Python code. That said, Padmini will be much easier
to read if you are familiar with the Ashtadhyayi and know how to create
prakriyās.


How the Code Is Organized
-------------------------

.. currentmodule:: padmini.ashtadhyayi

Generally, we apply rules in an order consistent with the tradition.

Most rules are implemented in the `padmini.prakarana` submodules, and the
user-facing API is in `padmini.ashtadhyayi`, which contains the :func:`tinanta`
and :func:`subanta` functions. If you look at these functions in your favorite
code editor, you can see that all these functions do is pass a
:class:`~padmini.prakriya.Prakriya` object into various submodules according to
the operation that needs to be applied.

We group rules into functions and module if they seem to have the same
functional intent. Usually, rules that are next to each other in the
Ashtadhyayi have the same functional intent, but this is not always the case.

For example, most of the rules that modify the abhyāsa are in a contiguous
block at the end of 7.4, and we simply moved these rules into their module
(:mod:`padmini.prakarana.abhyasya`). In contrast, the rules that introduce a
specific lakāra are scattered among sections 3.2, 3.3, and 3.4.

When in doubt, we recommend grepping for a specific rule, e.g. ``3.1.68``, to
see where it used. From there, you can trace back the call stack.


Notes on Style
--------------

Since we have thousands of rules to implement, we apply a few conventions to
keep our code concise and readable:

- ``p`` generally refers to the prakriyā.
- ``c`` generally refers to the current term, i.e. the term that would be
  modified by the rule.
- ``n`` generally refers to the next term.
- ``prev`` generally refers to the previous term. We wanted to use ``p`` for
  consistency, but few rules condition on the previous term, and it seemed more
  useful to reserve ``p`` for the prakriyā.
- On a term, ``u`` refers to the upadeśa. Rules frequently refer to the
  upadeśa, so we chose ``u`` as the attribute name because it is evocative and
  short.
- ``f`` is the :mod:`~padmini.filters` module.
- ``op`` is the :mod:`~padmini.operations` module.
- ``T`` is the :class:`~padmini.constants.Tag` class, which we refer to
  frequently.
- ``s`` is the :func:`~padmini.sounds.s` function, which lets us define groups
  of Sanskrit sounds.
