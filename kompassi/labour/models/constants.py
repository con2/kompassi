# FIXME this shit must die

SIGNUP_STATE_NAMES = dict(
    new="Uusi",
    accepted="Hyväksytty, odottaa vuoroja",
    confirmation="Hyväksytty, odottaa vahvistusta",
    finished="Hyväksytty, vuorot lähetetty",
    complained="Hyväksytty, vuoroista reklamoitu",
    rejected="Hylätty",
    cancelled="Peruutettu",
    arrived="Saapunut tapahtumaan",
    honr_discharged="Työpanos suoritettu hyväksytysti",
    dish_discharged="Työpanoksessa moitittavaa",
    no_show="Jätti saapumatta paikalle",
    relieved="Vapautettu tehtävästään",
    beyond_logic="Perätilassa",
    archived="Arkistoitu",
)

NUM_FIRST_CATEGORIES = 8

SIGNUP_STATE_CLASSES = dict(
    new="default",
    accepted="info",
    confirmation="warning",
    finished="success",
    complained="warning",
    rejected="danger",
    cancelled="danger",
    arrived="success",
    honr_discharged="success",
    dish_discharged="danger",
    no_show="danger",
    beyond_logic="danger",
    relieved="danger",
    archived="default",
)

SIGNUP_STATE_LABEL_CLASSES = {
    state_name: f"label-{generic_class}" for (state_name, generic_class) in SIGNUP_STATE_CLASSES.items()
}

SIGNUP_STATE_BUTTON_CLASSES = {
    state_name: f"btn-{generic_class}" for (state_name, generic_class) in SIGNUP_STATE_CLASSES.items()
}

SIGNUP_STATE_DESCRIPTIONS = dict(
    new="Hakemuksesi on vastaanotettu, ja työvoimavastaavat käsittelevät sen lähiaikoina. Saat tiedon hakemuksesi hyväksymisestä tai hylkäämisestä sähköpostitse.",
    accepted="Työvoimavastaavat ovat alustavasti hyväksyneet sinut vapaaehtoistyöhön tähän tapahtumaan, mutta sinulle ei ole vielä määritelty työvuoroja. Saat tiedon työvuoroistasi myöhemmin sähköpostitse.",
    confirmation="Sinua pyydetään vahvistamaan osallistumisesi tapahtumaan. Mikäli et vahvista osallistumistasi määräaikaan mennessä, ilmoittautumisesi perutaan ja tilallesi otetaan toinen hakija.",
)

SIGNUP_STATE_IMPERATIVES = dict(
    new="Palauta tilaan Uusi",
    accepted="Hyväksy hakemus",
    confirmation="Vaadi vahvistusta",
    finished="Lähetä vuorot",
    arrived="Merkitse saapuneeksi",
    complained="Kirjaa reklamaatio vuoroista",
    honr_discharged="Teki työnsä hyväksytysti",
    dish_discharged="Teki työnsä moitittavasti",
    no_show="Ei saapunut paikalle",
    relieved="Vapauta tehtävästään",
    rejected="Hylkää",
    cancelled="Merkitse peruutetuksi",
    beyond_logic="Aseta perätilaan",
)

# Flags need to be in the Grand Order
STATE_FLAGS_BY_NAME = dict(
    #                active accept confir ready  compla arrive workac reprim reject cancel
    new=(True, False, False, False, False, False, False, False, False, False),
    accepted=(True, True, False, False, False, False, False, False, False, False),
    confirmation=(True, True, True, False, False, False, False, False, False, False),
    finished=(True, True, False, True, False, False, False, False, False, False),
    complained=(True, True, False, True, True, False, False, False, False, False),
    arrived=(True, True, False, True, False, True, False, False, False, False),
    honr_discharged=(True, True, False, True, False, True, True, False, False, False),
    dish_discharged=(True, True, False, True, False, True, False, True, False, False),
    no_show=(True, True, False, True, False, False, False, True, False, False),
    rejected=(False, False, False, False, False, False, False, False, True, False),
    relieved=(False, True, False, False, False, False, False, False, False, True),
    cancelled=(False, False, False, False, False, False, False, False, False, True),
    beyond_logic=(False, False, False, False, False, False, False, False, False, False),
)

STATE_NAME_BY_FLAGS = {flags: name for (name, flags) in STATE_FLAGS_BY_NAME.items()}

# These need to be in the Grand Order (with created_at substituted for is_active)
STATE_TIME_FIELDS = [
    "created_at",
    "time_accepted",
    "time_confirmation_requested",
    "time_finished",
    "time_complained",
    "time_arrived",
    "time_work_accepted",
    "time_reprimanded",
    "time_rejected",
    "time_cancelled",
]

GROUP_VERBOSE_NAMES_BY_SUFFIX = dict(
    admins="Työvoimavastaavat",
    applicants="Aktiiviset",
    new="Uudet hakijat",
    processed="Käsitellyt",
    accepted="Hyväksytyt",
    confirmation="Vahvistusta odottavat",
    finished="Työvuorotetut",
    complained="Reklamoidut",
    cancelled="Peruutetut",
    rejected="Hylätyt",
    arrived="Saapuneet",
    workaccepted="Työnsä hyväksytysti suorittaneet",
    reprimanded="Työnsä moitittavasti suorittaneet",
    spam="Potentiaaliset hakijat",
    afterparty="Kaatajaisten osallistujat",
    afterparteh="Kaatajaisiin oikeutetut",
)

SIGNUP_STATE_GROUPS = [
    "applicants",
    "new",
    "processed",
    "accepted",
    "confirmation",
    "finished",
    "complained",
    "cancelled",
    "rejected",
    "arrived",
    "workaccepted",
    "reprimanded",
]

JOB_TITLE_LENGTH = 63
