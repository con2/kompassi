# -*- coding: utf-8 -*-
import datetime
import json
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_safe
import itertools

from core.utils import url
from labour.models import Signup

from ..helpers import labour_admin_required

__author__ = 'jyrkila'

RFC8601DATETIME = "%Y-%m-%dT%H:%M:%S%z"
RFC8601DATE = "%Y-%m-%d"
TIME = "%H:%M:%S"


def get_query(event):
    """
    Get event signup query class.

    :param event: Target event to get query class from.
    :type event: core.models.Event
    :return: Query class or None if query class was not found.
    :rtype: T <= QueryBuilder
    """
    labour_meta = event.labour_event_meta
    if labour_meta is None:
        return None
    signup_extra = labour_meta.signup_extra_model
    return signup_extra.get_query_class()


def get_query_config(vars, query_builder):
    fields, titles = query_builder.get_columns()

    # Order by case insensitive titles located in 'titles'-dict values.
    ordered_titles = sorted(list(titles.items()), cmp=lambda lhs, rhs: cmp(lhs[1].lower(), rhs[1].lower()))

    # Create ordered list of fields from ordered titles.
    ordered_fields = [(key, fields[key]) for key, _ in ordered_titles if key in fields]

    vars.update(
        query_builder_data_filters=json.dumps(fields),
        query_builder_data_titles=json.dumps(ordered_titles),
        query_builder_filters=ordered_fields,
        query_builder_titles=titles,
        query_builder_default_views=query_builder.default_views,
        query_builder_view_groups=json.dumps(query_builder.view_groups),
    )


@require_safe
@labour_admin_required
def query_index(request, vars, event):
    query_builder_class = get_query(event)
    if query_builder_class is None:
        messages.error(request, "Tapahtumalla ei ole kyselymäärityksiä. Ota yhteys ylläpitäjään.")
        return HttpResponseRedirect(reverse("labour_admin_dashboard_view", args=[event.slug]))

    query_builder = query_builder_class()
    get_query_config(vars, query_builder)

    return render(request, 'labour_query.pug', vars)


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
            for key, val in group.items():
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
            try:
                if isinstance(value, datetime.date):
                    entry[key] = value.strftime(RFC8601DATE)
                elif isinstance(value, datetime.datetime):
                    entry[key] = value.strftime(RFC8601DATETIME)
                elif isinstance(value, datetime.time):
                    entry[key] = value.strftime(TIME)
            except ValueError:
                # Apparently, this works before 1900.
                entry[key] = value.isoformat()


@require_POST
@labour_admin_required
def query_exec(request, vars, event):
    if not request.is_ajax() and not settings.DEBUG:
        # Don't bother with non-ajax requests.
        return HttpResponseRedirect(reverse(query_index, args=[event.slug]))

    query_builder_class = get_query(event)
    if query_builder_class is None:
        return HttpResponseNotFound()

    query_builder = query_builder_class()
    query_builder.parse(request.POST)

    q_results = query_builder.exec_query()
    m_results = merge_values(list(q_results))
    for result in m_results:
        # NB signup link uses person.pk, not signup.pk
        signup = Signup.objects.get(pk=result["pk"])

        result["__url"] = url("labour_admin_signup_view", event.slug, signup.person.pk)

    convert_datetimes(m_results)
    j_results = json.dumps(m_results)

    if request.is_ajax():
        # Normal ajax-request.
        return HttpResponse(j_results)
    else:
        # Debug emitted standard POST-request.
        get_query_config(vars, query_builder)
        vars.update(
            query_builder_results=j_results,
            query_builder_views=json.dumps(query_builder.views),
        )
        return render(request, 'labour_query.pug', vars)
