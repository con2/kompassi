def format_price(cents):
    return "%d,%02d €" % divmod(cents, 100)


def format_date(dt):
    return dt.strftime("%Y-%m-%d")


def append_reference_number_checksum(s):
    return s + str(-sum(int(x) * [7, 3, 1][i % 3] for i, x in enumerate(s[::-1])) % 10)
