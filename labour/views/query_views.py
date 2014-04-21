import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from labour.helpers import labour_admin_required
from labour.querybuilder import Signup9

__author__ = 'jyrkila'


@require_http_methods(['GET'])
@labour_admin_required
def query_index(request, vars, event):
    query_builder = Signup9()
    fields, titles = query_builder.get_columns()

    # Order by case insensitive titles located in 'titles'-dict values.
    ordered_titles = sorted(titles.items(), cmp=lambda lhs, rhs: cmp(lhs[1].lower(), rhs[1].lower()))

    # Create ordered list of fields from ordered titles.
    ordered_fields = [(key, fields[key]) for key, _ in ordered_titles]

    vars.update(
        query_builder_data_filters=json.dumps(fields),
        query_builder_data_titles=json.dumps(titles),
        query_builder_filters=ordered_fields,
        query_builder_titles=titles,
    )

    return render(request, 'labour_query.jade', vars)
