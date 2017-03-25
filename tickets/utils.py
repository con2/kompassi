# encoding: utf-8


def format_price(cents):
    return "%d,%02d €" % divmod(cents, 100)


def format_date(dt):
    return dt.strftime("%Y-%m-%d")
