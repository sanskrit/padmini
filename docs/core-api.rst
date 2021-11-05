Core API
========

.. module:: padmini

This section of the documentation covers all of Padmini's core interfaces. In
order, we cover:

- the main user-facing API
- Padmini's core data structures
- the internal APIs that modify these data structures

For the implementation of specific rules, see the :doc:`prakarana-api`.


High-level API
--------------

.. currentmodule:: padmini.ashtadhyayi

.. autofunction:: tinanta

.. autofunction:: subanta


Data Structures
---------------

.. currentmodule:: padmini.prakriya

Padmini stores its data in three main data structures:

- an ordinary :class:`str`, which denotes a sequence of sounds in SLP1
  transliteration. We use SLP1 because it represents each sound with exactly
  one character, which greatly simplifies the code. (For example, a string's
  last sound is just ``s[-1]``.)

- a :class:`Term`, which is a :class:`str` with extra metadata. Metadata
  includes any saṁjñās associated with the string, the string's substitution
  history, and other minor information.

- a :class:`Prakriya`, which is a list of :class:`~Term` and extra metadata.
  Metadata includes the derivation history, saṁjñās that apply to the prakriyā
  as a whole, and other minor information.

.. autoclass:: Term

.. autoclass:: Prakriya


Constants
---------

.. autoclass:: padmini.constants.Tag


Views
-----

.. autoclass:: padmini.term_views.TermView


Sounds
------

.. currentmodule:: padmini.sounds

Sounds in the Ashtadhyayi have two main functions:

- They *condition* operations by their presence or absence.
- They *transform* according specific rules.

To handle these two use cases, this module exposes two primary functions:

.. autofunction:: s

.. autofunction:: map_sounds


Filters
-------

Before we apply a rule, we must first test if it meets the necessary
conditions. Many conditions are simple or adhoc (e.g. ``t.antya in s('ac')`` to
test if a term ends in a vowel). More complex conditions are specified below:

.. automodule:: padmini.filters
   :members:


Operations
----------

The Ashtadhyayi modifies the derivation state with three types of rules:

- *vidhi* (transformation), which change the sounds in a prakriyā.
- *saṃjñā* (designation), which adds new saṁjñās to a prakriyā.
- *atideśa* (analogy), which usually extends an it-saṁjñā to a prakriyā.

More abstractly, all of these rule types modify the prakriyā by changing its
sounds and designations. We call this abstract category the **operation**.

As much as possible, any changes to the :class:`~Prakriya` are applied through
this module (as opposed to ad-hoc logic). By doing so, we keep the code DRY and
concise.

Most operations apply to a single term and have this basic structure::

    def some_operation(rule: str, p: Prakriya, t: Term, *args):
        # Modify the term in some way
        t.text = [...]
        # Record which rule was applied
        p.step(rule)

.. automodule:: padmini.operations
   :members:
