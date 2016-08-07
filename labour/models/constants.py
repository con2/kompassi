# encoding: utf-8

# FIXME this shit must die

SIGNUP_STATE_NAMES = dict(
    new=u'Uusi',
    accepted=u'Hyväksytty, odottaa vuoroja',
    confirmation=u'Hyväksytty, odottaa vahvistusta',
    finished=u'Hyväksytty, vuorot lähetetty',
    complained=u'Hyväksytty, vuoroista reklamoitu',

    rejected=u'Hylätty',
    cancelled=u'Peruutettu',

    arrived=u'Saapunut tapahtumaan',

    honr_discharged=u'Työpanos suoritettu hyväksytysti',
    dish_discharged=u'Työpanoksessa moitittavaa',
    no_show=u'Jätti saapumatta paikalle',
    relieved=u'Vapautettu tehtävästään',

    beyond_logic=u'Perätilassa',
)

NUM_FIRST_CATEGORIES = 8

SIGNUP_STATE_CLASSES = dict(
    new=u'default',
    accepted=u'info',
    confirmation=u'warning',
    finished=u'success',
    complained=u'warning',
    rejected=u'danger',
    cancelled=u'danger',
    arrived=u'success',
    honr_discharged=u'success',
    dish_discharged=u'danger',
    no_show=u'danger',
    beyond_logic=u'danger',
    relieved=u'danger',
)

SIGNUP_STATE_LABEL_CLASSES = dict(
    (state_name, "label-{generic_class}".format(generic_class=generic_class))
    for (state_name, generic_class) in SIGNUP_STATE_CLASSES.iteritems()
)

SIGNUP_STATE_BUTTON_CLASSES = dict(
    (state_name, "btn-{generic_class}".format(generic_class=generic_class))
    for (state_name, generic_class) in SIGNUP_STATE_CLASSES.iteritems()
)

SIGNUP_STATE_DESCRIPTIONS = dict(
    new=u'Hakemuksesi on vastaanotettu, ja työvoimavastaavat käsittelevät sen lähiaikoina. Saat tiedon hakemuksesi hyväksymisestä tai hylkäämisestä sähköpostitse.',
    accepted=u'Työvoimavastaavat ovat alustavasti hyväksyneet sinut vapaaehtoistyöhön tähän tapahtumaan, mutta sinulle ei ole vielä määritelty työvuoroja. Saat tiedon työvuoroistasi myöhemmin sähköpostitse.',
    confirmation=u'Sinua pyydetään vahvistamaan osallistumisesi tapahtumaan. Mikäli et vahvista osallistumistasi määräaikaan mennessä, ilmoittautumisesi perutaan ja tilallesi otetaan toinen hakija.',
)

SIGNUP_STATE_IMPERATIVES = dict(
    new=u'Palauta tilaan Uusi',
    accepted=u'Hyväksy hakemus',
    confirmation=u'Vaadi vahvistusta',
    finished=u'Lähetä vuorot',
    arrived=u'Merkitse saapuneeksi',
    complained=u'Kirjaa reklamaatio vuoroista',
    honr_discharged=u'Teki työnsä hyväksytysti',
    dish_discharged=u'Teki työnsä moitittavasti',
    no_show=u'Ei saapunut paikalle',
    relieved=u'Vapauta tehtävästään',
    rejected=u'Hylkää',
    cancelled=u'Merkitse peruutetuksi',
    beyond_logic=u'Aseta perätilaan',
)

# Flags need to be in the Grand Order
STATE_FLAGS_BY_NAME = dict(
    #                active accept confir ready  compla arrive workac reprim reject cancel
    new=            (True,  False, False, False, False, False, False, False, False, False),
    accepted=       (True,  True,  False, False, False, False, False, False, False, False),
    confirmation=   (True,  True,  True,  False, False, False, False, False, False, False),
    finished=       (True,  True,  False, True,  False, False, False, False, False, False),
    complained=     (True,  True,  False, True,  True,  False, False, False, False, False),
    arrived=        (True,  True,  False, True,  False, True,  False, False, False, False),
    honr_discharged=(True,  True,  False, True,  False, True,  True,  False, False, False),
    dish_discharged=(True,  True,  False, True,  False, True,  False, True,  False, False),
    no_show=        (True,  True,  False, True,  False, False, False, True,  False, False),
    rejected=       (False, False, False, False, False, False, False, False, True,  False),
    relieved=       (False, True,  False, False, False, False, False, False, False, True ),
    cancelled=      (False, False, False, False, False, False, False, False, False, True ),
    beyond_logic=   (False, False, False, False, False, False, False, False, False, False),
)

STATE_NAME_BY_FLAGS = dict((flags, name) for (name, flags) in STATE_FLAGS_BY_NAME.iteritems())

# These need to be in the Grand Order (with created_at substituted for is_active)
STATE_TIME_FIELDS = [
    'created_at',
    'time_accepted',
    'time_confirmation_requested',
    'time_finished',
    'time_complained',
    'time_arrived',
    'time_work_accepted',
    'time_reprimanded',
    'time_rejected',
    'time_cancelled',
]

GROUP_VERBOSE_NAMES_BY_SUFFIX = dict(
    admins=u'Työvoimavastaavat',
    applicants=u'Aktiiviset',
    new=u'Uudet hakijat',
    processed=u'Käsitellyt',
    accepted=u'Hyväksytyt',
    confirmation=u'Vahvistusta odottavat',
    finished=u'Työvuorotetut',
    complained=u'Reklamoidut',
    cancelled=u'Peruutetut',
    rejected=u'Hylätyt',
    arrived=u'Saapuneet',
    workaccepted=u'Työnsä hyväksytysti suorittaneet',
    reprimanded=u'Työnsä moitittavasti suorittaneet',
)

SIGNUP_STATE_GROUPS = [
    'applicants',
    'new',
    'processed',
    'accepted',
    'confirmation',
    'finished',
    'complained',
    'cancelled',
    'rejected',
    'arrived',
    'workaccepted',
    'reprimanded',
]
