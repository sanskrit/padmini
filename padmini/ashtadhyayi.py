from .constants import Tag
from .prakarana import ac_sandhi
from .prakarana import angasya
from .prakarana import ardhadhatuka
from .prakarana import atidesha
from .prakarana import atmanepada
from .prakarana import dhatu_karya
from .prakarana import dvitva
from .prakarana import la_karya
from .prakarana import pratipadika_karya
from .prakarana import samjna
from .prakarana import samprasarana
from .prakarana import sanadyanta
from .prakarana import sup_karya
from .prakarana import tin_pratyaya
from .prakarana import tripadi
from .prakarana import vikarana
from .prakriya import Prakriya


def dhatu_samprasarana_tasks(p: Prakriya):
    """
    Samprasarana of the dhatu is conditioned on several other operations,
    which we must execute first:

        jha_adesha --> it_agama --> atidesha --> samprasarana
    """
    # Needed transitively for dhatu-samprasarana.
    angasya.jha_adesha(p)
    # Depends on jha_adesha since it conditions on the first sound.
    angasya.it_agama.run_before_attva(p)
    # Depends on it_agama for certain rules.
    atidesha.run_before_attva(p)

    # Depends on atidesha (for kit-Nit).
    samprasarana.run_for_dhatu(p)
    # Ad-Adeza and other special tasks for Ardhadhatuka
    ardhadhatuka.run_before_dvitva(p)

    # Now finish it_agama and atidesha
    angasya.it_agama.run_after_attva(p)
    atidesha.run_after_attva(p)


def tinanta(dhatu: str, dhatu_code: str, la: str, tags=None, options=None) -> Prakriya:
    """Generate a tinanta (verb).

    :param dhatu: the dhātu to use. `dhatu` must include any relevant accent
        marks. See ``dhatupatha.tsv`` for examples.
    :param dhatu_code: the number in the Dhatupatha. This help distinguish
        between identical roots in separate ganas.
    :param la: the lakāra to use. This must use a nasal vowel; use ``"la~w"``,
        not ``"law"``.
    :param tags: extra tags to add to the derivation. For details, see
        :class:`~Tag`.
    :param options: enables or disables various optional rules in the
        Ashtadhyayi. For details, see the comments in :class:`~Prakriya`.
    :return: the complete prakriyā.
    """

    # Initialize the prakriya.
    p = Prakriya.make()
    p.add_tags(*(tags or []))
    p.set_options(options or {})

    # TODO: don't hard-code, also allow karmaNi and bhAve.
    p.add_tags(Tag.KARTARI)

    # Create the dhAtu and add any sanAdi pratyayas.
    dhatu_karya.run(p, dhatu, dhatu_code)

    # Rule 3.1.31 ("AyAdaya ArdhadhAtuke vA") makes rules 3.1.28 - 3.1.30
    # optional if ArdhadhAtuka follows. But at this stage in the prakriya, we
    # haven't added any such suffix. The traditional solution is to consider
    # vivakSA and "look ahead" to the suffix we will add in the following
    # steps:
    #
    #    ārdhadhātukaviṣaye ārdhadhātukavivakṣāyām āyādayaḥ pratyayā vā
    #    bhavanti. (kāśikāvṛttiḥ)
    #
    vidhi_lin = la == "li~N" and not p.all(Tag.ASHIH)
    is_sarvadhatuka = vidhi_lin or la in {"la~w", "lo~w", "la~N"}
    sanadyanta.run(p, is_ardhadhatuka=not is_sarvadhatuka)

    # Add the lakāra.
    la_karya.run(p, la)

    # Base substitutions that must run before we choose the pada.
    ardhadhatuka.dhatu_adesha_before_pada(p)

    # Determine the pada.
    atmanepada.run(p)

    # Supply the correct tiN suffix.
    #
    # `adesha` must run before `vikarana` because `vikarana` expects
    # sArvadhAtuka/ArdhatAkuka and these terms cannot be applied to the lakAra
    # directly.
    tin_pratyaya.adesha(p)

    # Apply samjnas for any new suffixes.
    samjna.run(p)

    # Do lit-siddhi and AzIrlin-siddhi first to support the valAdi vArttika for
    # aj>vi.
    lit_ashirlin = la == "li~w" or (la == "li~N" and p.all(Tag.ASHIH))
    if lit_ashirlin:
        tin_pratyaya.siddhi(p)

    # Base substitutions that must run before vikarana, e.g. "lun-sanor ghasl"
    ardhadhatuka.run_before_vikarana(p)

    # Add the vikarana and add samjnas as necessary.
    vikarana.run(p)
    samjna.run(p)

    # --- Code below this line has not been cleaned up. --- #

    if not is_sarvadhatuka:
        dhatu_samprasarana_tasks(p)

    angasya.hacky_before_dvitva(p)

    # Depends on: ardhadhatuka.run_before_siddhi (e.g. for "jagau")
    dvitva.run(p)

    samprasarana.run_for_abhyasa(p)

    # Apply the necessary changes to the tiN suffix above.
    # Depends on: dvitva, vikarana (e.g. 3.4.109 sijabhyastavidibhyazca)
    if not lit_ashirlin:
        tin_pratyaya.siddhi(p)

    if is_sarvadhatuka:
        dhatu_samprasarana_tasks(p)

    angasya.iit_agama(p)

    # Must follow tin-siddhi (for valAdi)
    ardhadhatuka.am_agama(p)
    # Finish the angasya section.
    angasya.run_remainder(p)
    # Apply any remaining sandhi changes.
    ac_sandhi.run(p)
    # Finally, the tripAdi.
    tripadi.run(p)

    return p


def subanta(pratipadika: str, linga: str, tags=None, options=None) -> Prakriya:
    """Generate a subanta (nominal).

    :param pratipadika: the `prAtipadika` to use.
    :param tags: extra tags to add to the derivation. For details, see
        :class:`~Tag`.
    :param options: enables or disables various optional rules in the
        Ashtadhyayi. For details, see the comments in :class:`~Prakriya`.
    :return: the complete prakriyā.
    """
    # Initialize the prakriya.
    p = Prakriya.make()
    p.add_tags(*(tags or []))
    p.set_options(options or {})

    # Introduce the pratipadika
    pratipadika_karya.run(p, pratipadika, linga)

    # Introduce the sup-pratyaya
    sup_karya.run(p)

    # Add various samjnas
    samjna.pratipadika_samjna(p)

    ac_sandhi.sup_sandhi_before_angasya(p)

    # Run the angasya section.
    angasya.run_remainder(p)

    # Apply any remaining sandhi changes.
    ac_sandhi.sup_sandhi_after_angasya(p)
    ac_sandhi.run_common(p)

    # Finally, the tripAdi.
    tripadi.run(p)

    # The prakriya is complete!
    # To read the final result, use `p.text`.
    return p
