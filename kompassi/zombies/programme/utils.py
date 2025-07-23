from itertools import islice


# from http://docs.python.org/release/2.3.5/lib/itertools-example.html
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = (*result[1:], elem)
        yield result


def next_full_hour(t):
    if (t.minute, t.second, t.microsecond) == (0, 0, 0):
        return t
    else:
        return t.replace(hour=t.hour + 1, minute=0, second=0, microsecond=0)
