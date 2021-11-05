Prakaraṇa API
=============

.. module:: padmini.prakarana

.. currentmodule:: padmini.prakriya

Conceptually, the rules of the Ashtadhyayi are organized into functional areas
called **prakaraṇas**. Whereas a prakriyā is like the specific execution of
some program, a prakaraṇa is like the program itself.

All of Padmini's rules are in the `padmini.prakarana` module, which splits the
Ashtadhyayi's rule into smaller modules and functions. Each prakaraṇa module
typically has a `run` function that accepts a :class:`Prakriya` and performs
some operations on it:

.. code-block:: python

    def run(p: Prakriya):
        ...

Below, we share the major prakaraṇa modules.

.. automodule:: padmini.prakarana.it_samjna

.. automodule:: padmini.prakarana.vikarana

.. automodule:: padmini.prakarana.la_karya

.. automodule:: padmini.prakarana.tin_pratyaya

.. automodule:: padmini.prakarana.it_agama

.. automodule:: padmini.prakarana.dvitva

.. automodule:: padmini.prakarana.abhyasasya

.. automodule:: padmini.prakarana.ac_sandhi

.. automodule:: padmini.prakarana.tripadi
