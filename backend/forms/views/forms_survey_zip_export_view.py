from zipfile import ZipFile

import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from access.cbac import graphql_check_instance
from dimensions.models.scope import Scope

from ..excel_export import write_responses_as_excel
from ..models.survey import Survey
from ..utils.filename_utils import truncate_filename


def forms_survey_zip_export_view(
    request: HttpRequest,
    scope_slug: str,
    survey_slug: str,
):
    timestamp = now().strftime("%Y%m%d%H%M%S")
    scope = get_object_or_404(Scope, slug=scope_slug)
    # TODO survey.scope instead of survey.event
    if scope.event is None:
        raise NotImplementedError("non-event scope")
    survey = get_object_or_404(Survey, event=scope.event, slug=survey_slug)
    basename = f"{scope.slug}_{survey.slug}_responses_{timestamp}"
    zip_filename = truncate_filename(f"{basename}.zip")
    excel_filename = truncate_filename(f"{basename}.xlsx")

    # TODO(#324): Failed check causes 500 now, turn it to 403 (middleware?)
    graphql_check_instance(
        survey,
        request,
        app=survey.app,
        field="responses",
        operation="query",
    )

    http_response = HttpResponse(content_type="application/zip")
    http_response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'

    fields = survey.get_combined_fields()
    session = requests.Session()

    with ZipFile(http_response, "w") as zip:  # type: ignore
        with zip.open(excel_filename, "w") as excel_file:
            write_responses_as_excel(
                survey.dimensions.order_by("order"),
                survey.combined_fields,
                survey.responses.order_by("created_at").only("form_data"),
                excel_file,  # type: ignore
            )

        for form_response in survey.responses.all():
            for attachment in form_response.get_attachments(fields):
                attachment_bytes = attachment.download(session=session)
                attachment_filename = truncate_filename(
                    "-".join(
                        [
                            format(form_response.sequence_number, "04d"),
                            attachment.field_slug,
                            attachment.basename,
                        ]
                    )
                )

                with zip.open(attachment_filename, "w") as attachment_file:
                    attachment_file.write(attachment_bytes)

    return http_response
