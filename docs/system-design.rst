System Design
=============

Philosophy
----------

Padmini follows the principles of the tradition as much as possible, but we
break with the traditional model of rule selection, since doing so greatly
simplifies the program.


Data Types
----------

.. currentmodule: padmini.prakriya

Padmini's main data structure is the :class:`Prakriya`, which models the
derivation state. Its most important data is a list of :class:`Term` objects,
each of which contains a string of sounds and any metadata associated with
those sounds. For detail, see the :doc:`core-api` page.


Filters and Operators
---------------------

We model a rule as having two parts: a **filter** that checks if the rule can
apply, and an **operation** that makes the necessary change. Filters and
operations are allowed to work on :class:`Prakriya` objects, directly, but
usually they work on a :class:`Term` object instead. For example, most rules
are written in the following format:

.. code-block:: python

    if filter(term):
        op(term)

Filters might be actual Python functions, but they are usually simple
expressions that take advantage of :class:`Term`'s rich API:

.. code-block:: python

    if term.antya == 'a':
        op(prakriya)

Operations, meanwhile, are usually standardized functions from the
:mod:`~padmini.operations` module. By centralizing operation code in one place,
we make it easy to refactor or modify operation behavior across the system if
future needs demand it.

To better illustrate the points above, here is an example of a simple rule from
Padmini. This rule creates verbs like *tasthau* and *jagau*:

.. code-block:: python

    if prev.antya == "A" and tin.u == "Ral":
        op.upadesha("7.1.34", p, tin, "O")

Here the rule uses :func:`~padmini.operations.upadesha` to replace the upadeśa
value of the final tiṅ suffix.


Creating a Prakriyā
-------------------

.. currentmodule: padmini.ashtadhyayi

Generally, Padmini groups related rules into functions and related functions
into modules. Then the main Padmini code just calls these functions one after
another. For example, here is a version of the :func:`subanta` function with
comments removed:

.. code-block:: python

    def subanta(pratipadika: str, linga: str, tags=None, options=None) -> Prakriya:
        p = Prakriya.make()
        p.add_tags(*(tags or []))
        p.set_options(options or {})

        pratipadika_karya.run(p, pratipadika, linga)
        sup_karya.run(p)
        samjna.pratipadika_samjna(p)
        ac_sandhi.sup_sandhi_before_angasya(p)
        angasya.run_remainder(p)
        ac_sandhi.sup_sandhi_after_angasya(p)
        ac_sandhi.run_common(p)
        tripadi.run(p)
        return p

Roughly, this function has two steps. First, we create the prakriyā and add any
metadata associated with the derivation. Then, we apply functions one after
another until the derivation is complete.
