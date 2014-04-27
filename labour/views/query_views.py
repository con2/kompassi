import json
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
import itertools
from labour.helpers import labour_admin_required
from labour.querybuilder import Signup9

__author__ = 'jyrkila'

RFC2822TIME = "%a, %d %b %Y %H:%M:%S %z"


@require_GET
@labour_admin_required
def query_index(request, vars, event):
    query_builder = Signup9()
    fields, titles = query_builder.get_columns()

    # Order by case insensitive titles located in 'titles'-dict values.
    ordered_titles = sorted(titles.items(), cmp=lambda lhs, rhs: cmp(lhs[1].lower(), rhs[1].lower()))

    # Create ordered list of fields from ordered titles.
    ordered_fields = [(key, fields[key]) for key, _ in ordered_titles if key in fields]

    vars.update(
        query_builder_data_filters=json.dumps(fields),
        query_builder_data_titles=json.dumps(ordered_titles),
        query_builder_filters=ordered_fields,
        query_builder_titles=titles,
    )

    return render(request, 'labour_query.jade', vars)


def merge_values(values):
    """
    When you call values() on a queryset where the Model has a ManyToManyField
    and there are multiple related items, it returns a separate dictionary for each
    related item. This function merges the dictionaries so that there is only
    one dictionary per id at the end, with lists of related items for each.
    """
    grouped_results = itertools.groupby(values, key=lambda value: value['pk'])

    merged_values = []
    for k, g in grouped_results:
        groups = list(g)
        merged_value = {}
        for group in groups:
            for key, val in group.iteritems():
                if not merged_value.get(key):
                    merged_value[key] = val
                elif val != merged_value[key]:
                    if isinstance(merged_value[key], list):
                        if val not in merged_value[key]:
                            merged_value[key].append(val)
                    else:
                        old_val = merged_value[key]
                        merged_value[key] = [old_val, val]
        merged_values.append(merged_value)
    return merged_values


def convert_datetimes(values):
    """
    Format all date/datetime-like values to strings.
    """
    for entry in values:
        for key, value in entry.items():
            if "strftime" in dir(value):
                entry[key] = value.strftime(RFC2822TIME)


@require_POST
@labour_admin_required
def query_exec(request, vars, event):
    if not request.is_ajax():
        # Don't bother with non-ajax requests.
        return HttpResponseRedirect(reverse(query_index, args=[event.slug]))

    query_builder = Signup9()
    query_builder.parse(request.POST)

    q_results = query_builder.exec_query()
    m_results = merge_values(list(q_results))
    convert_datetimes(m_results)

    return HttpResponse(json.dumps(m_results))
