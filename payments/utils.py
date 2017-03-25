import hashlib

from django.conf import settings

ENCODING = 'UTF-8'


def u(s):
    return s.encode(ENCODING)


def compute_payment_request_mac(request, order):
    meta = order.event.payments_event_meta

    mac = hashlib.md5()
    mac.update(u(settings.CHECKOUT_PARAMS['VERSION']))
    mac.update(b'+')
    mac.update(u(str(order.checkout_stamp)))
    mac.update(b'+')
    mac.update(u(str(order.price_cents)))
    mac.update(b'+')
    mac.update(u(order.reference_number))
    mac.update(b'+')
    mac.update(u(order.checkout_message))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['LANGUAGE']))
    mac.update(b'+')
    mac.update(u(meta.checkout_merchant))
    mac.update(b'+')
    mac.update(u(order.checkout_return_url(request)))
    mac.update(b'+')
    mac.update(b'')
    mac.update(b'+')
    mac.update(b'')
    mac.update(b'+')
    mac.update(b'')
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['COUNTRY']))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['CURRENCY']))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['DEVICE']))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['CONTENT']))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['TYPE']))
    mac.update(b'+')
    mac.update(u(settings.CHECKOUT_PARAMS['ALGORITHM']))
    mac.update(b'+')
    mac.update(u(meta.checkout_delivery_date))
    mac.update(b'+')
    mac.update(u(order.customer.first_name))
    mac.update(b'+')
    mac.update(u(order.customer.last_name))
    mac.update(b'+')
    mac.update(u(order.customer.address))
    mac.update(b'+')
    mac.update(u(order.customer.zip_code))
    mac.update(b'+')
    mac.update(u(order.customer.city))
    mac.update(b'+')
    mac.update(u(meta.checkout_password))

    return mac.hexdigest().upper()
