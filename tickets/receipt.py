# encoding: utf-8



from contextlib import contextmanager
import os

from django.conf import settings

try:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas

    BASE_INDENT = 25*mm
    DEEP_INDENT = BASE_INDENT + 15*mm
except ImportError:
    from warnings import warn
    warn('Failed to import ReportLab. Generating receipts will fail.')


# XXX hardcoded
LOGO_FILENAME = os.path.join(settings.STATIC_ROOT, "images", "tracon_logo_kuitille.jpg")


@contextmanager
def state_saved(canvas):
    try:
        canvas.saveState()
        yield canvas
    finally:
        canvas.restoreState()


def render_logo(x, y, c):
    # XXX parametrize over event
    with state_saved(c):
        c.translate(x, y)
        c.drawImage(LOGO_FILENAME, 0, 0, 48*mm, 25*mm)


def render_receipt(order, c):
    # render_logo(135*mm, 255*mm, c)

    c.setFont("Times-Roman", 12)
    c.drawString(135*mm, 250*mm, order.event.headline)

    c.drawString(BASE_INDENT, 270*mm, order.customer.name)
    c.drawString(BASE_INDENT, 265*mm, order.customer.address)
    c.drawString(BASE_INDENT, 260*mm, "%s %s" % (order.customer.zip_code, order.customer.city))

    c.drawString(BASE_INDENT, 200*mm, "Hyvä vastaanottaja,")

    c.drawString(BASE_INDENT, 190*mm, "Tässä tilaamanne {0} -pääsyliput:".format(order.event.name))

    ypos = 180*mm

    for op in order.order_product_set.filter(product__requires_shipping=True):
        c.drawString(BASE_INDENT, ypos, "%d kpl" % op.count)
        c.drawString(DEEP_INDENT, ypos, op.product.name)

        ypos -= 10*mm

    non_ship = order.order_product_set.filter(product__requires_shipping=False)
    if non_ship:
        c.drawString(BASE_INDENT, ypos, "Seuraavista tilaamistanne tuotteista saatte lisäohjeita sähköpostitse ennen tapahtumaa:")
        ypos -= 10*mm

        for op in non_ship:
            c.drawString(BASE_INDENT, ypos, "%d kpl" % op.count)
            c.drawString(DEEP_INDENT, ypos, op.product.name)

            ypos -= 10*mm

    c.drawString(BASE_INDENT, ypos, "Mikäli yllä olevassa luettelossa on virheitä tai kuoren sisältö ei vastaa luetteloa, olkaa hyvä ja")
    c.drawString(BASE_INDENT, ypos - 5*mm, "ottakaa viipymättä yhteyttä lipunmyyntivastaavaan sähköpostitse: {0}".format(order.event.tickets_event_meta.plain_contact_email))
    #c.drawString(BASE_INDENT, ypos - 10*mm, u"tai puhelimitse numeroon 0400 464 988 (Janne Forsell, parhaiten tavoittaa klo 10-18).")

    c.drawString(BASE_INDENT, ypos - 15*mm, "Mainitkaa viestissänne tilausnumeronne #%04d." % order.id)

    ypos -= 30*mm

    c.drawString(BASE_INDENT, ypos, "Lisätietoja {0} -tapahtumasta löydätte kotisivuiltamme: {1}".format(order.event.name, order.event.homepage_url))

    ypos -= 15*mm

    c.drawString(BASE_INDENT, ypos, "Ystävällisin terveisin")
    c.drawString(BASE_INDENT, ypos - 10*mm, "{0} järjestäjät".format(order.event.name_genitive))

    c.line(BASE_INDENT, 20*mm, 210*mm - BASE_INDENT, 20*mm)
    c.setFont("Helvetica", 8)
    c.drawString(BASE_INDENT, 16*mm, order.event.tickets_event_meta.receipt_footer)

    c.showPage()


def test():
    class DummyCustomer:
        name = "Essi Esimerkki"
        address = "Animupolunkaarteenrinteentie 5 as. 9"
        zip_code = "33720"
        city = "Tampere"

    class DummyOrder:
        id = 666
        customer = DummyCustomer()

        tickets = 3
        tshirts = 0
        accommodation = 1

    order = DummyOrder()

    c = canvas.Canvas("test.pdf")
    render_receipt(order, c)
    c.save()
