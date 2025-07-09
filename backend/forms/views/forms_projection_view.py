from __future__ import annotations

from typing import Literal

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from access.cbac import graphql_check_instance
from dimensions.filters import DimensionFilters
from graphql_api.language import DEFAULT_LANGUAGE, to_supported_language

from ..excel_export import write_projection_as_excel
from ..models.projection import Projection


def forms_projection_view(
    request: HttpRequest,
    scope_slug: str,
    projection_slug: str,
    format: Literal["json", "xlsx"] = "json",
):
    projection = get_object_or_404(Projection, scope__slug=scope_slug, slug=projection_slug)

    if not projection.is_public:
        graphql_check_instance(
            projection,  # type: ignore
            request,
            app=projection.app.value,
        )

    user_filters = DimensionFilters.from_query_dict(request.GET)
    lang_values = user_filters.filters.pop("lang", [])
    lang = to_supported_language(lang_values[0]) if lang_values else DEFAULT_LANGUAGE
    projected = projection.project(user_filters=user_filters, lang=lang)

    if format == "json":
        response = JsonResponse(projected, safe=False)
    elif format == "xlsx":
        timestamp = now().strftime("%Y%m%d%H%M%S")
        filename = f"{projection.scope.slug}_{projection.slug}_{timestamp}.xlsx"

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        write_projection_as_excel(
            projection,
            projected,
            response,
        )
    else:
        raise NotImplementedError(f"Format '{format}' is not supported.")

    return response
