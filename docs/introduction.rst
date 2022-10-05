Introduction
============

The Ashtadhyayi is a list of around 4000 grammar rules. Together with the
Dhatupatha and other secondary texts, it defines a formal grammar that
generates valid Sanskrit expressions.

Padmini is an emulator for this grammar that focuses specifically on generating
valid *words*. When feasible, we follow the design and spirit of the
Ashtadhyayi and the rest of the tradition. But we balance this adherence to
tradition with a pragmatic focus on making a clean and maintainable program.


Why We Created Padmini
----------------------

We created Padmini with several goals in mind:

- We want to create a list of Sanskrit verb and nominal forms that is (1)
  freely available, (2) exhaustive, and (3) high-quality. There are various
  datasets floating around online, but as far as we can tell, none meets all
  three criteria.

- We want to be able to explain all verb and nominal forms. This ability
  unlocks powerful new applications. For example, imagine a tool that could
  explain the grammar details of any word you give it.

- We want to create a useful tool for students of Sanskrit grammar. The more
  comprehensive our tool becomes, the more it can serve as a kind of "reference
  implementation" that makes sense of the tradition.

- More personally, we wanted to dive deeper into the tradition and explore the
  connection between traditional grammar and formal systems.

As compared to a predecessor system like SanskritVerb_, Padmini:

- is roughly 10 times faster
- fixes several important bugs
- has better support for optional derivations
- is faster and safer to modify

.. _SanskritVerb: https://github.com/drdhaval2785/SanskritVerb


How We Model Data
-----------------

When grammarians use the Ashtadhyayi, they start with some set of initial
conditions and apply rules one after another to produce a final result. This
derivation is called a **prakriyā**. Here is a simple example of a prakriyā for
the word "bhavati":

| bhū (1.3.1)
| bhū tip (3.4.78)
| bhū ti (1.3.9)
| bhū śap ti (3.1.68)
| bhū a ti ( 1.3.9)
| bho a ti (7.3.84)
| bhav a ti (6.1.78)

Each line of the prakriyā is its own step, and it is the result of applying the
rule that appears in parentheses. In each step of a prakriyā, there are one or
more **terms** (for example, "bho" or "ti") that each have their own labels and
properties. And these terms consist of some number of **sounds** that can be
modified and changed.

.. currentmodule:: padmini.prakriya

Padmini uses a similar approach. We model a list of sounds as a simple string,
and we associate it with metadata in a :class:`~Term` object. And multiple
:class:`~Term` objects are collected in a :class:`~Prakriya` object, which also
maintains a record of all of the rules that have been applied so far.

In general, Padmini's user-facing API receives some basic initial conditions
and returns all prakriyās that satisfy those conditions.


How We Model Rules
------------------

Rules are of various types, but at a high level, we can sort them into three
types:

1. *interpretive* rules, which help us correctly apply other rules. Padmini
   uses interpretive rules to lay out the program, but these rules are rarely
   explicit.

2. *modifying* rules, which cause some change to the prakriyā. This is the most
   common rule type that Padmini uses. These rules directly modify the
   :class:`~Prakriya`.

3. *blocking* rules, which block a modifying rule. These rules are logged on
   the :class:`~Prakriya`, but they don't produce any other changes.

A group of rules with a similar purpose is called a *prakaraṇa*. Based on this
concept, we group rules into functions and modules according to their shared
intent. This is worth stating explicitly because the Ashtadhyayi itself
does *not* make this choice. Instead, the Ashtadhyayi mainly optimizes
for concision and reorders rules if doing so would minimize the total length of
the text.


How We Interpret Rules
----------------------

In general, we follow the interpretations of the standard commentaries,
especially the *Kāśikāvr̥tti* and the *Siddhāntakaumudī*. https://ashtadhyayi.com
has been an enormous help in this regard.

One small exception is that we have tended to prefer more straightforward
interpretations of rules, even if this conflicts with the later tradition. For
example, we do not model *git* in 1.1.5 *kṇiti ca*. For now, the extra
complexity is not necessary.


How We Select Rules for Application
-----------------------------------

Our major departure we make from the tradition is in how we select which rule
to use.

The traditional approach is to choose one rule among all of the ones available
by using various heuristics. For example, we have this rule from the
*Paribhāṣenduśekhara*:

    pūrvaparanityāntaraṅgāpavādānāmuttarottaraṁ balīyaḥ

    Earlier, later, obligatory, internally conditioned, and exceptional --
    these are ordered from lowest to highest priority.

Instead of formalizing the principles of rule selection, we have simply created
an ordering for these rules and apply each rule in order if it has scope to
apply. This ordering is obviously informed by the tradition, but the underlying
mechanics are very different.

Why have we used this approach? Mainly, we've done so because it greatly
simplifies Padmini's execution flow and makes it much easier to debug problems
and create patches. Once Padmini is stable, we might revisit this choice; but
for now, it makes development much faster.

