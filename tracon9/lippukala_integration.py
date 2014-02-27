# encoding: utf-8

# https://docs.google.com/spreadsheet/ccc?key=0Annwjrq9JeBldGQ3aEFRakpJeGtISUVpTnpJRl92dUE&usp=drive_web#gid=0
KEYSPACE = list(set(u"""
ahma    arkki   ääni    höyry   kulta   aita    piano   hylly   hame    kahvi   viiva
ahven   hihna   aika    ilma    kumi    muuri   rumpu   kuori   huppu   maito   kaari
eläin   johto   aste    päivä   lanka   talo    torvi   kynä    kenkä   liha    käyrä
hauki   kirja   avain   pilvi   muovi   torni   viulu   mappi   mekko   kaali   suora
    kivi    jakso   pouta   nahka   kokko   sello   tasku   paita   jauho   pallo
hylje   lakki   jalka   sade    naru    salko       vihko   sukka   riisi   pinta
ilves   lappu   kanta   sähkö   pahvi   maja        kirje       hillo   taso
kettu   lasi    katu    tuuli   rauta   katos                  jana
karhu   lehti   kausi   valo    teräs                   puuro   piste
    levy    kesto   aalto   hiili
kala    mitta   kone        rikki
    nauha   kuva        tina
kotka   noppa   laulu
kuha    nuoli   lause
lahna   pannu   lento
näätä   pullo   lista
närhi       meemi
rotta       melu
varis       mieli
heppa       muoto
siika       pohja
        posti
        raha
        raita
        sana
        taide
        vaara
        väri
        vesi
        viesti
        vuosi
        ihme
        voima
        hissi
""".split()))

class Queue:
    SINGLE_WEEKEND_TICKET = '91'
    TWO_WEEKEND_TICKETS = '92'
    EVERYONE_ELSE = '95'

PREFIXES = {
    Queue.SINGLE_WEEKEND_TICKET: "kissa",
    Queue.TWO_WEEKEND_TICKETS: "koira",
    Queue.EVERYONE_ELSE: "hiiri",
}

KEYSPACES = {
    Queue.SINGLE_WEEKEND_TICKET: KEYSPACE,
    Queue.TWO_WEEKEND_TICKETS: KEYSPACE,
    Queue.EVERYONE_ELSE: KEYSPACE,
}

def select_queue(order):
    """
    Orders with single weekend e-ticket (and no other e-tickets) go to the "kissa" queue.
    Orders with two weekend e-tickets (and no other e-tickets) go to the "koira" queue.
    All other orders go to the "hiiri" queue.
    """

    from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

    from core.models import Event
    from tickets.models import Product

    try:
        event = Event.objects.get(name='Tracon 9')
        product = Product.objects.get(event=event, name__icontains='viikonlop', electronic_ticket=True)
        op = order.order_product_set.filter(product__electronic_ticket=True).get()
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return Queue.EVERYONE_ELSE

    if op.count == 1:
        return Queue.SINGLE_WEEKEND_TICKET

    elif op.count == 2:
        return Queue.TWO_WEEKEND_TICKETS

    else:
        return Queue.EVERYONE_ELSE
