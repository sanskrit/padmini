class Tag:

    """:class:`Tag` combines two concepts: saṃjñā and semantic conditions.
    These tags are then attached to a :class:`Term` or :class:`Prakriya`.

    In addition to the tags below, a :class:`Term` or :class:`Prakriya` might
    also contain various *it* letters.
    """

    # Morpheme types
    UPASARGA = "upasarga"
    DHATU = "dhatu"
    GHU = "ghu"
    AGAMA = "Agama"
    PRATYAYA = "pratyaya"
    PRATIPADIKA = "prAtipadika"
    VIBHAKTI = "vibhakti"
    SARVANAMA = "sarvanama"
    SARVANAMASTHANA = "sarvanamasthAna"
    TIN = "tiN"
    NISTHA = "nistha"
    KRT = "krt"
    KRTYA = "krtya"
    SUP = "sup"
    TADDHITA = "taddhita"
    VIKARANA = "vikarana"

    # Lopa
    LUK = "luk"
    SLU = "Slu"
    LUP = "lup"

    # Accent
    ANUDATTA = "anudAtta"
    SVARITA = "svarita"
    ANUDATTET = "anudAttet"
    SVARITET = "svaritet"

    # Pada
    PARASMAIPADA = "parasmaipada"
    ATMANEPADA = "Atmanepada"

    # Artha (semantic conditions)
    ASHIH = "ashih"
    SANARTHA = "san-artha"
    YANARTHA = "yan-artha"

    # Dialect conditions
    CHANDASI = "chandasi"

    # Prayoga
    KARTARI = "kartari"
    BHAVE = "bhave"
    KARMANI = "karmani"

    # Purusha
    PRATHAMA = "prathama"
    MADHYAMA = "madhyama"
    UTTAMA = "uttama"

    # Vacana
    EKAVACANA = "ekavacana"
    DVIVACANA = "dvivacana"
    BAHUVACANA = "bahuvacana"

    # Vibhakti (subanta)
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"
    V4 = "v4"
    V5 = "v5"
    V6 = "v6"
    V7 = "v7"

    # Linga (subanta)
    PUM = "pum"
    STRI = "strI"
    NAPUMSAKA = "napuMsaka"

    # Stem types
    NADI = "nadi"
    GHI = "ghi"

    SAMBODHANA = "sambodhana"
    AMANTRITA = "Amantrita"
    SAMBUDDHI = "sambuddhi"

    # Dvitva
    ABHYASA = "abhyAsa"
    ABHYASTA = "abhyasta"

    # Dhatuka
    ARDHADHATUKA = "ardhadhatuka"
    SARVADHATUKA = "sarvadhatuka"

    # Other flags
    #
    # Certain conditions cross prakaranas in a way that is difficult to track.
    # Since these conditions are limited, we just keep track of them with
    # these flags.

    # Flags on the `Term`:
    F_GUNA_APAVADA = "guna-apavada"
    F_GUNA = "guna"

    # Flags on the `Prakriya`.
    F_ADESHA_ADI = "adesha_adi"
    F_NO_ARDHADHATUKA = "no-ardha"
    F_ANIT_KSA = "anit-ksa"
    F_SET_SIC = "set-sic"
    F_AT_AGAMA = "at-agama"
    F_AT_LOPA = "at-lopa"

    SAT = "zat"
