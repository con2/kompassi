# -*- coding: utf-8 -*-

"""
=============
QueryBuilder
=============

1. Write a QueryBuilder subclass for a model.
2. For query UI request, get available fields and views and output them to JS part.
3. When JS does request with POST containing filter and view, parse the request.
4. If the request was acceptable, execute the query and output the results.


----------------------
QueryBuilder subclass
----------------------

A simple example::

    from django.contrib.auth.models import User

    class UserQuery(QueryBuilder):
        model = User
        query_related_exclude = {
            "": ["password"]
        }
        view_related_exclude = {
            "": ["password"]
        }


------------------------
Generate content for JS
------------------------

When processing request::

    import json

    def my_view(request):
        query = UserQuery()
        fields, views = query.get_columns()
        fields, views = json.dumps(fields), json.dumps(views)
        return render(request, "my_view.html", {"fields": fields, "views": views})


-----------------
Process JS query
-----------------

Oversimplified AJAX processing::

    def my_results(request):
        query = UserQuery()
        query.parse(request.POST)
        results = query.exec_query()
        results = json.dumps(results)
        return HttpResponse(results)

"""

import json
from labour.models import Signup
from django.db import models
from django.db.models.fields import related
from django.db.models.query import Q, LOOKUP_SEP


Field2Transport = {
    "CharField": "str",
    "TextField": "text",
    "IntegerField": "int",
    "BooleanField": "bool",
    "DateField": "date",
    "DateTimeField": "datetime",
}


class QueryBuilder(object):
    """
    --------------------------
    Selected fields in a model
    --------------------------

     * By default, i.e. if filter is not set or it is "*", all fields are included in the filter set.
       AutoField is never considered a valid field.
       Related fields are added for selection by id if their full name is not a key in the filter.
     * If filter value is a list, only string names from that list are included.
     * If related field full name is as a filter key, the related model is added for filtering (instead of selection).
       The field must also be considered as a valid field, i.e. not excluded and the model field list contains the
       field name.
     * If exclude is a list, string names from that list are excluded from the field set.
     * A field that has been marked in filter and exclude, is excluded.

     * All fields included in filtering are included in views. Additional views can be added to view_related_filter.
    """

    query_related_filter = {}
    """
    Extra FK fields available for filtering.
    FK name or empty string for root model : field names from foreign model in a tuple,
    or a single string "*" (instead of the tuple) for all fields from foreign model.
    """

    query_related_exclude = {}
    """
    Excluded keys. These are absolute and always override filters.
    FK name or empty string for root model : field names from foreign model in a tuple.
    """

    field_mapping = None

    view_related_filter = {}
    """
    Extra fields from FK to allow in output.
    FK name or empty string for root model : field names from foreign model in a tuple.
    """

    view_related_exclude = {}
    """
    Excluded views. These are absolute and always override filters.
    FK name or empty string for root model : field names from foreign model in a tuple.
    """

    model = None
    """
    Django Model to create QueryBuilder on.
    """

    # Adapted from https://djangosnippets.org/snippets/676/
    def build_query_filter_from_spec(self, spec):
        """
        Assemble a django "Q" query filter object from a specification that consists
        of a possibly-nested list of query filter descriptions.  These descriptions
        themselves specify Django primitive query filters, along with boolean
        "and", "or", and "not" operators.  This format can be serialized and
        deserialized, allowing django queries to be composed client-side and
        sent across the wire using JSON.

        Each filter description is a list.  The first element of the list is always
        the filter operator name. This name is one of either django's filter
        operators, "eq" (a synonym for "exact"), or the boolean operators
        "and", "or", and "not".

        Primitive query filters have three elements:

        [filteroperator, fieldname, queryarg]

        "filteroperator" is a string name like "in", "range", "icontains", etc.
        "fieldname" is the django field being queried.  Any name that django
        accepts is allowed, including references to fields in foreign keys
        using the "__" syntax described in the django API reference.
        "queryarg" is the argument you'd pass to the `filter()` method in
        the Django database API.

        "and" and "or" query filters are lists that begin with the appropriate
        operator name, and include subfilters as additional list elements:

        ['or', [subfilter], ...]
        ['and', [subfilter], ...]

        "not" query filters consist of exactly two elements:

        ['not', [subfilter]]

        As a special case, the empty list "[]" or None return all elements.

        If field_mapping is specified, the field name provided in the spec
        is looked up in the field_mapping dictionary.  If there's a match,
        the result is subsitituted. Otherwise, the field name is used unchanged
        to form the query. This feature allows client-side programs to use
        "nice" names that can be mapped to more complex django names. If
        you decide to use this feature, you'll probably want to do a similar
        mapping on the field names being returned to the client.

        This function returns a Q object that can be used anywhere you'd like
        in the django query machinery.

        This function raises ValueError in case the query is malformed, or
        perhaps other errors from the underlying DB code.

        Example queries:

        ['and', ['contains', 'name', 'Django'], ['range', 'apps', [1, 4]]]
        ['not', ['in', 'tags', ['colors', 'shapes', 'animals']]]
        ['or', ['eq', 'id', 2], ['icontains', 'city', 'Boston']]
        """
        if spec is None or len(spec) == 0:
            return Q()
        cmd = spec[0]
        result_q = None

        if cmd == 'and' or cmd == 'or':
            # ["or",  [filter],[filter],[filter],...]
            # ["and", [filter],[filter],[filter],...]
            if len(spec) < 2:
                raise ValueError('"and" or "or" filters must have at least one subfilter')

            if cmd == 'and':
                q_op = lambda l, r: l & r
            else:
                q_op = lambda l, r: l | r

            for arg in spec[1:]:
                q_part = self.build_query_filter_from_spec(arg)
                if q_part is not None:
                    if result_q is None:
                        result_q = q_part
                    else:
                        result_q = q_op(result_q, q_part)

        elif cmd == 'not':
            # ["not", [query]]
            if len(spec) != 2:
                raise ValueError('"not" filters must have exactly one subfilter')
            q_part = self.build_query_filter_from_spec(spec[1])
            if q_part is not None:
                result_q = ~q_part

        else:
            # some other query, will be validated in the query machinery
            # ["cmd", "fieldname", "arg"]

            # provide an intuitive alias for exact field equality
            if cmd == 'eq':
                cmd = 'exact'

            if len(spec) != 3:
                raise ValueError('primitive filters must have two arguments (fieldname and query arg)')

            field_name = spec[1]
            if self.field_mapping is not None:
                # see if the mapping contains an entry for the field_name
                # (for example, if you're mapping an external database name
                # to an internal django one).  If not, use the existing name.
                field_name = self.field_mapping.get(field_name, field_name)

            if field_name not in self._fields:  # "in self._query_excludes:
                # The field is excluded.
                raise ValueError("querybuilder: Trying to include an excluded field in query: {0!r}".format(field_name))

            # Q(lhs=kwarg) --> Q(field_name__cmd=kwarg)
            lhs = LOOKUP_SEP.join((field_name, cmd))  # str("%s%s%s" % (field_name, LOOKUP_SEP, cmd))
            kwarg = {lhs: spec[2]}
            result_q = Q(**kwarg)

        return result_q

    def build_views(self, views):
        for field in views:
            if LOOKUP_SEP in field:
                prefix, tail = field.rsplit(LOOKUP_SEP, 1)
            else:
                prefix, tail = "", field

            if field in self._view_excludes or (prefix in self._view_filter and tail not in self._view_filter[prefix]):
                raise ValueError("querybuilder: Trying to include an excluded field in views: {0!r}".format(field))
        return views

    @staticmethod
    def join_related(items):
        """
        Join dictionary keys to their value tuples.
        :type items: dict
        :return: list
        """
        output = []
        for key, value in items.items():
            if key is not "":
                output.extend([LOOKUP_SEP.join((key, field)) for field in value])
            else:
                output.extend(value)

        return output

    def __init__(self):

        self._query_excludes = self.join_related(self.query_related_exclude)
        """Joined list of excluded fields full names."""
        self._query_filter = self.query_related_filter

        self._view_excludes = self.join_related(self.view_related_exclude)
        self._view_filter = self.view_related_filter

        self._query = None
        self._views = None

        self._fields = None
        """:type: dict[str, str | dict[str, str | dict | list]]"""

        self._field_titles = {}
        """:type: dict[str, str]"""

    def parse(self, data):
        """
        Parse request data from js-generator.

        :param data: Request data from POST.
        :type data: dict
        :raises ValueError: If some part of request was not allowed or invalid.
        """

        if self._fields is None:
            self.get_columns()

        query_string = data.get("filter", "[]")
        query = json.loads(query_string)
        self._query = self.build_query_filter_from_spec(query)

        view_string = data.get("view", "[]")
        views = json.loads(view_string)
        self._views = self.build_views(views)

    @property
    def query(self):
        """
        Parsed query from js-generator as a Q-clause.
        :rtype: Q
        """
        return self._query

    @property
    def views(self):
        """
        Parsed view settings from js-generator.
        :rtype: list[str]
        """
        return self._views

    def get_columns(self):
        """
        Used generic transport types: int, str, text, bool.
        Custom transport type (dict) lists available choices, primary key as key, display name as value.

        :return: Transport type for each filter; Title for each view.
        :rtype: dict[str, str | dict[str, str | dict | list]], dict[str, str]
        """
        self._fields = {}
        self._find_columns(self.model)
        return self._fields, self._field_titles

    def exec_query(self):
        """
        Exec the query that has been parsed.

        :return: Data from the query.
        :rtype: list[dict]
        """
        assert self._query is not None and self._views is not None

        # These two lines do filtering AND result views fetching in one query even as the pk-ids are
        # supplied to "the second query" as filter argument, and the "pk__in" does not actually
        # generate an "IN" -filter to the SQL WHERE.
        pks = self.model.objects.filter(self.query).only("pk").values_list("pk", flat=True)
        results = self.model.objects.values("pk", *self.views).filter(pk__in=pks)

        return results

    # noinspection PyProtectedMember
    def _find_columns(self, model, prefix=None):
        """
        Find columns in the given model. Used to create the JS filter generator.

        :param model: The model to find stuff for.
        :param prefix: Query path prefix.
        :type prefix: str
        :return: Transport type for each filter; Title for each view.
        :rtype: dict[str, str | dict[int, str]], dict[str, str]
        """
        model_meta = model._meta
        prefix_non_empty = prefix if prefix is not None else ""
        extra_views = set()

        use_default_filter = prefix_non_empty not in self.query_related_filter\
            or self.query_related_filter[prefix_non_empty] == "*"

        if use_default_filter:
            # Default, i.e. everything available. This includes all possible filter fields, and view fields.
            fields = model_meta.get_all_field_names()
        else:
            # Only certain set of filter fields.
            # View fields are stored in extra_views, and added to the iterable set to get their titles.
            fields = self.query_related_filter[prefix_non_empty]

            # If view includes are defined, use them.
            if prefix_non_empty in self.view_related_filter:
                extra_views = set(self.view_related_filter[prefix_non_empty])

        # Convert to set, as fields should not be iterated twice, and extra_views may contain same names.
        fields = set(fields)

        # Iterate over union of fields and views.
        for field in fields | extra_views:
            if prefix is not None:
                full_name = LOOKUP_SEP.join((prefix, field))
            else:
                full_name = field

            field_object, mdl, direct, m2m = model_meta.get_field_by_name(field)

            if not field in fields:
                # Field is not defined in fields, it must be in views then.
                # Only the view title is added to title container.
                self._object_title(full_name, field_object)
                continue

            if isinstance(field_object, models.AutoField) or \
                    self._is_excluded(full_name, prefix_non_empty, field):
                self._add_title(field_object, prefix_non_empty, full_name)
                continue

            is_related = isinstance(field_object, related.RelatedField)
            if is_related:
                # FK, M2M, O2O
                self._find_related(field_object, full_name)
                continue

            is_reverse = isinstance(field_object, related.RelatedObject)
            if is_reverse:
                # TODO: No support for related objects (i.e. the related_name_set-things at other end of FK)
                continue

            self._add_column(field_object, full_name)

    def _is_excluded(self, full_name, prefix, field_name):
        # If full_name is excluded, always exclude.
        if full_name in self._query_excludes:
            return True

        # Field is included only if...
        # ... Using default filter set, or the filter for the prefix is "*"
        dm = (prefix not in self._query_filter or self._query_filter[prefix] == "*")

        # ... or the field is marked to be included
        dm = dm or field_name in self._query_filter[prefix]

        # ... or it is further filtered
        dm = dm or full_name in self._query_filter

        # So other cases are excluded; DeMorgan
        return not dm

    def _find_related(self, field, full_name):
        if full_name in self.query_related_filter or isinstance(field, related.OneToOneField):
            # * FK: Filter by related field (unknown)
            # This field was used
            self._find_columns(field.rel.to, full_name)
        else:
            # * FK: Select-one
            self._find_sub_selection(field, field.rel.to, full_name)

    def _add_column(self, field_object, full_name):
        if field_object.choices is not None and len(field_object.choices) > 0:
            # Add choices as tuples to preserve ordering
            select_def = dict(
                multiple="or",
                order=list(map(lambda entry: entry[0], field_object.choices)),
                values=dict(field_object.choices),
            )
            self._fields[full_name] = select_def
            self._object_title(full_name, field_object)
            return

        class_name = field_object.__class__.__name__
        if class_name not in Field2Transport:
            return

        self._fields[full_name] = Field2Transport[class_name]
        self._object_title(full_name, field_object)

    def _add_title(self, field_object, prefix, full_name):
        """
        Adds field title to titles conditionally.
        Title is added only if the field is explicitly defined in view filter.

        :param field_object: Field object being inspected.
        :param prefix: Current prefix before the field.
        :type prefix: str
        :param full_name: Full name of the field, i.e. with prefix.
        :type full_name: str
        """
        if prefix in self.view_related_filter and field_object.name in self.view_related_filter[prefix]:
            self._object_title(full_name, field_object)

    def _object_title(self, key, obj):
        # Verbose_name may be a string, or translation proxy which need to be converted.
        self._field_titles[key] = unicode(obj.verbose_name)

    # noinspection PyProtectedMember
    def _find_sub_selection(self, field_object, model, prefix):
        """
        Find related choices for selecting in filtering.
        The choices are read from each available related pk and their unicode string value.

        :type prefix: str
        """
        primary_key = model._meta.pk
        primary_key_name = primary_key.name
        related_results = model.objects.all()

        if isinstance(field_object.rel, related.ManyToManyRel):
            select_def = dict(multiple="and")
        else:
            assert not isinstance(field_object.rel, related.OneToOneRel)
            select_def = dict(multiple="or")

        order = []
        values = {}
        for value in related_results:
            value_pk = getattr(value, primary_key_name)
            order.append(value_pk)
            values[value_pk] = unicode(value)

        select_def["values"] = values
        select_def["order"] = order

        title_source = field_object
        if field_object.verbose_name is None:
            # TODO: verbose_name is actually never None?
            title_source = model._meta

        prefix = "{0}__pk".format(prefix)
        self._fields[prefix] = select_def
        self._object_title(prefix, title_source)

    @property
    def fields(self):
        return self._fields


class Signup2(QueryBuilder):
    model = Signup
    query_related_filter = {
        "person": ("birth_date",),
    }
    query_related_exclude = {
        "": ("event",),
    }
    view_related_filter = {
        "person": ("first_name", "surname", "nick", "birth_date", "email", "phone",)
    }

