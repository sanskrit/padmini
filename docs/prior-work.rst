Prior Work
----------

There have been many attempts to model the Ashtadhyayi in code, but Padmini is
especially influenced by SanskritVerb_ and Vyakarana_.

Padmini owes an immense debt to SanskritVerb for providing a solid reference
implementation, which we used for debugging. Even knowing that a solid
implementation was possible and feasible was a great source of encouragement
during the more difficult parts of the implementation work.

In terms of technical design, Padmini is a direct successor to our older
Vyakarana project and adopts many of the same concepts and philosophies.

.. _Vyakarana: https://vyakarana.readthedocs.io
.. _SanskritVerb: https://github.com/drdhaval2785/SanskritVerb

The major difference between Vyakarana and Padmini is that Vyakarana explicitly
models rule selection using traditional mechanisms. In order to enable this,
Vyakarana wraps most of its code in classes and first-order functions and
introduces a quasi-DSL for transforming and combining these rules. For example,
two filters could be combined with Vyakarana's ``&`` operator to create a
boolean *and*. This allows easier inspection on the filters and operators
involved in each rule, which in turns allows ranking in a priority queue.

In comparison, Padmini does not model rule selection and instead uses a fixed
rule order that turns the Ashtadhyayi into a normal iterative program. While
this decision is less true to the spirit of the Ashtadhyayi, it creates a
program that is substantially easier to read and maintain.

To illustrate the effect this has on ordinary code, here is how Vyakarana would
model a rule where we apply vr̥ddhi if the term starts with a consonant and ends
with a vowel:

.. code-block:: python

    class adi(AlFilter):
        def body(self, term):
            return term.adi in self.domain

    class antya(AlFilter):
        def body(self, term):
            return term.antya in self.domain
   
    @Operator.no_params
    def vrddhi(state, index, locus=None):
        ...


    RULES = [
        ('some_rule', None, adi('hal') & antya ('ac'), None, vrddhi)
    ]


And how Padmini would do it:

.. code-block:: python

    from padmini.sounds import s

    def vrddhi(term):
        ...

    def run(p: Prakriya, i):
        c = p.terms[i]
        if c.adi in s('hal') and c.antya in s('ac'):
            vrddhi(c)

While the Vyakarana code has interesting properties that the Padmini code does
not, the Padmini code is substantially more readable and accessible.
