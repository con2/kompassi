from django.template import Library

__all__ = ["programme_list_heading_should_be_rendered"]
register = Library()


@register.filter
def programme_list_heading_should_be_rendered(programmes):
    """
    Used by programme_schedule_list.pug alone.

    A horribly convoluted way of hiding empty headings in the programme listings
    such as the one below the programme schedule table.

    The listing is implemented by using the same programme data as the table does.
    Due to this, the data contains all kinds of elements unnecessary to the flat
    listing:

    [(start_time, incontinuity, programmes)]

    where `programmes` is a list of (programme, rowspan).

    The list of (programme, rowspan) contains (None, None) for each empty cell
    in the schedule. This is why a simple `if programmes` will not do to hide
    the heading.

    The correct condition is `any(prog for (prog, rowspan) in programmes)` which,
    unfortunately, Django templates will not let us embed in the template code
    itself due to Hitler and the Nazis.

    So we use a filter with `if`, computing the aforementioned condition
    safely here in the Python code for the template to simply `if` on it.
    """
    return any(prog for (prog, rowspan) in programmes)
