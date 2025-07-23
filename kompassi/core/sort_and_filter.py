from collections import OrderedDict
from dataclasses import dataclass

from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from kompassi.core.utils import mutate_query_params


@dataclass
class Definition:
    slug: str
    name: str
    definition: str
    owner: str | None = None

    @property
    def qs_add(self):
        """
        A request string that turns this definition on.
        :return: str
        """
        return mutate_query_params(self.owner.request, {self.owner.request_param: self.slug})

    @property
    def qs_del(self):
        """
        A request string that turns this definition off.
        :return: str
        """
        return mutate_query_params(self.owner.request, {self.owner.request_param: None})


class SortAndFilterBase:
    default_to_first_added = False

    def __init__(self, request, request_param, default=None):
        """
        :param request: HTTP request to bind the sorter/filter to. May be None.
        :type request: django.http.HttpRequest|None
        :param request_param: Request parameter to read when querying `selected`
        :param default: Default slug when nothing otherwise specified.
        """
        self.request = request
        self.request_param = request_param
        self.definitions = OrderedDict()
        self.default = default

    def add(self, slug, name, definition):
        """
        Add a definition to the object.

        :param slug: Slug (used in request params, etc.)
        :param name: User-readable name
        :param definition: Definition
        :return: This object, for chaining fun
        """
        self.definitions[slug] = Definition(slug, name, definition, owner=self)
        if self.default_to_first_added and not self.default:
            self.default = slug
        return self

    @property
    def selected_slug(self):
        if not self.request:
            return None
        slug = self.request.GET.get(self.request_param, self.default)
        if slug not in self.definitions:
            slug = self.default
        return slug

    @property
    def selected_definition(self):
        return self.definitions.get(self.selected_slug)

    def __iter__(self):
        """
        Iterate over (definition, active) pairs in this object.
        :rtype: Iterable[tuple[dict, bool]]
        """
        selected_slug = self.selected_slug
        for defn in self.definitions.values():
            yield (defn, defn.slug == selected_slug)


class Sorter(SortAndFilterBase):
    default_to_first_added = True

    def order_queryset(self, queryset):
        """
        Order the given queryset by the currently selected ordering.

        :param queryset: A queryset.
        :return: A sorted clone of the queryset.
        """
        defn = self.selected_definition
        return queryset.order_by(*defn.definition)


class Filter(SortAndFilterBase):
    def filter_queryset(self, queryset):
        """
        Filter the given queryset by the currently selected filtering.

        If the filtering's definition is a callable, the queryset is iterated
        and the return value is a filtered list.

        :param queryset: A queryset.
        :return: The queryset itself, or a filtered version of the queryset.
        """
        defn = self.selected_definition
        if defn:
            if callable(defn.definition):
                return [o for o in queryset if defn.definition(o)]
            else:
                return queryset.filter(**defn.definition)
        else:
            return queryset

    def add_objects(self, filter_field, object_list):
        """
        Add the given objects as definitions; the filter expression is <filter_field>=<object_slug>.

        :param filter_field: Field name on the target queryset
        :param object_list: Objects to add
        :return: Self, for chaining
        """
        for obj in object_list:
            self.add(slug=obj.slug, name=force_str(obj), definition={filter_field: obj.slug})
        return self

    def add_choices(self, filter_field, choices):
        """
        Add a 'choices' list (as accepted by model and form fields) as definitions.

        :param filter_field: Field name on the target queryset
        :param choices: Choices to add
        :return: Self, for chaining
        """
        for slug, name in choices:
            self.add(slug=slug, name=name, definition={filter_field: slug})
        return self

    def add_booleans(self, filter_field):
        return self.add_choices(filter_field, [("1", _("Yes")), ("0", _("No"))])
