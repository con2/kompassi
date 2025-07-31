import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import DimensionBadge from "@/components/dimensions/DimensionBadge";
import DimensionValues from "@/components/dimensions/DimensionValues";
import DimensionValueSelectionForm, {
  buildDimensionValueSelectionForm,
} from "@/components/dimensions/DimensionValueSelectionForm";
import {
  CachedDimensions,
  validateCachedDimensions,
} from "@/components/dimensions/models";
import SignInRequired from "@/components/errors/SignInRequired";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import { OldVersionAlert } from "@/components/response/OldVersionAlert";
import ResponseHistorySidebar from "@/components/response/ResponseHistorySidebar";
import getPageTitle from "@/helpers/getPageTitle";
import slugify from "@/helpers/slugify";
import { getTranslations } from "@/translations";
import { ButtonGroup } from "react-bootstrap";
import { updateResponseDimensions } from "../../surveys/[surveySlug]/responses/[responseId]/actions";
import { acceptProgramOffer, cancelProgramOffer } from "./actions";

graphql(`
  fragment ProgramOfferDetail on FullResponseType {
    ...ResponseHistorySidebar

    values
    cachedDimensions

    form {
      description
      fields
      survey {
        title(lang: $locale)
        slug
        cachedDefaultResponseDimensions
        cachedDefaultInvolvementDimensions
        profileFieldSelector {
          ...FullProfileFieldSelector
        }
      }
    }

    programs {
      slug
      title
      cachedDimensions
    }

    dimensions {
      ...DimensionBadge
    }

    canEdit(mode: ADMIN)
    canAccept
    canCancel
    canDelete
  }
`);

const query = graphql(`
  query ProgramOfferPage(
    $eventSlug: String!
    $responseId: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      involvement {
        dimensions(publicOnly: false) {
          ...DimensionValueSelect
        }
      }

      program {
        dimensions(publicOnly: false) {
          ...DimensionValueSelect
        }

        programOffer(id: $responseId) {
          ...ProgramOfferDetail
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    responseId: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

interface Values {
  title?: string;
  description?: string;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, responseId } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Program.ProgramOffer;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, responseId },
  });

  if (!data.event?.program?.programOffer) {
    notFound();
  }

  const values: Values = data.event.program.programOffer.values as any;

  const title = getPageTitle({
    viewTitle: t.singleTitle,
    subject: values.title || "",
    event: data.event,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ProgramOfferPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale, responseId },
  });

  if (!data.event?.program?.programOffer) {
    notFound();
  }

  const surveyT = translations.Survey;
  const programT = translations.Program;
  const programHosT = translations.Program.ProgramHost;
  const t = translations.Program.ProgramOffer;

  const response = data.event.program.programOffer;
  const { event } = data;
  const { form, supersededBy, canEdit } = response;
  const { fields, survey } = form;

  const values: Record<string, any> = response.values ?? {};
  const { canAccept, canCancel, canDelete } = response;

  validateFields(fields);

  validateCachedDimensions(response.cachedDimensions);
  const programDimensions = data.event.program.dimensions;
  const defaultProgramDimensions =
    response.form.survey.cachedDefaultResponseDimensions ?? {};
  validateCachedDimensions(defaultProgramDimensions);
  const { fields: programDimensionFields, values: programDimensionValues } =
    buildDimensionValueSelectionForm(
      programDimensions,
      {
        ...defaultProgramDimensions,
        ...response.cachedDimensions,
      },
      "omit",
      "program_dimensions",
    );

  const involvementDimensions = data.event.involvement?.dimensions ?? [];
  const defaultInvolvementDimensions =
    response.form.survey.cachedDefaultInvolvementDimensions ?? {};
  validateCachedDimensions(defaultInvolvementDimensions);
  const {
    fields: involvementDimensionFields,
    values: involvementDimensionValues,
  } = buildDimensionValueSelectionForm(
    involvementDimensions,
    defaultInvolvementDimensions,
    "omit",
    "involvement_dimensions",
  );

  const acceptProgramOfferFields: Field[] = [
    {
      slug: "slug",
      type: "SingleLineText",
      required: true,
      ...programT.attributes.slug,
    },
    {
      slug: "title",
      type: "SingleLineText",
      required: true,
      title: programT.attributes.title,
    },
  ];

  if (
    involvementDimensions.filter((dimension) => !dimension.isTechnical).length >
    0
  ) {
    acceptProgramOfferFields.push(
      {
        slug: "involvementDimensionsHeader",
        type: "StaticText",
        title: programHosT.attributes.dimensions,
      },
      ...involvementDimensionFields,
    );
  }

  if (
    programDimensions.filter((dimension) => !dimension.isTechnical).length > 0
  ) {
    acceptProgramOfferFields.push(
      {
        slug: "programDimensionsHeader",
        type: "StaticText",
        title: programT.attributes.dimensions,
      },
      ...programDimensionFields,
    );
  }

  const cancelProgramOfferFields: Field[] = [
    {
      slug: "resolution",
      type: "SingleSelect",
      title: t.actions.cancel.attributes.resolution.title,
      required: true,
      choices: [
        {
          slug: "CANCEL",
          title: t.actions.cancel.attributes.resolution.choices.CANCEL,
          disabled: !canCancel,
        },
        {
          slug: "REJECT",
          title: t.actions.cancel.attributes.resolution.choices.REJECT,
          disabled: !canCancel,
        },
        {
          slug: "DELETE",
          title: t.actions.cancel.attributes.resolution.choices.DELETE,
          disabled: !canDelete,
        },
      ],
    },
  ];

  const uniquenessInsurance =
    response.programs.length > 0 ? `-${response.programs.length}` : "";
  const acceptProgramOfferValues: Record<string, any> = {
    slug: slugify(values.title || "") + uniquenessInsurance,
    title: values.title,
    description: values.description,
    ...programDimensionValues,
    ...involvementDimensionValues,
  };

  const surveySlug = response.form.survey!.slug;
  const dimensionsReadOnly = !!supersededBy;

  const stateDimension = programDimensions.find((d) => d.slug === "state");
  const responseStateDimensionValue = response.dimensions.find(
    (d) => d.dimension.slug === "state",
  );

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programOffers"
      searchParams={searchParams}
      actions={
        supersededBy ? undefined : (
          <ButtonGroup>
            <ModalButton
              className="btn btn-outline-success"
              label={t.actions.accept.label + "…"}
              title={t.actions.accept.title}
              messages={t.actions.accept.modalActions}
              disabled={!canAccept}
              action={acceptProgramOffer.bind(
                null,
                locale,
                eventSlug,
                responseId,
              )}
            >
              {response.programs.length > 0 && (
                <div className="alert alert-warning">
                  <p>
                    {t.attributes.programs.acceptAgainWarning(
                      response.programs.length,
                    )}
                  </p>
                  {response.programs.map((program) => (
                    <div key={program.slug}>
                      <Link
                        className="link-subtle"
                        href={`/${eventSlug}/program-admin/${program.slug}`}
                        title={program.title}
                        target="_blank"
                      >
                        {program.title}
                      </Link>
                    </div>
                  ))}
                </div>
              )}
              <p>{t.actions.accept.message}</p>
              <SchemaForm
                fields={acceptProgramOfferFields}
                values={acceptProgramOfferValues}
                messages={translations.SchemaForm}
                headingLevel="h4"
                idPrefix="accept-program-offer"
              />
            </ModalButton>

            <ModalButton
              className="btn btn-outline-danger"
              label={t.actions.cancel.label + "…"}
              title={t.actions.cancel.title}
              messages={t.actions.cancel.modalActions}
              disabled={!canCancel && !canDelete}
              action={cancelProgramOffer.bind(
                null,
                locale,
                eventSlug,
                responseId,
              )}
            >
              {t.actions.cancel.message}
              <SchemaForm
                fields={cancelProgramOfferFields}
                messages={translations.SchemaForm}
              />
            </ModalButton>

            <Link
              className={`btn btn-outline-primary ${canEdit ? "" : "disabled"}`}
              href={`/${locale}/${eventSlug}/program-offers/${responseId}/edit`}
              title={t.actions.edit.title}
            >
              {t.actions.edit.label}
            </Link>
          </ButtonGroup>
        )
      }
    >
      <h3 className="mt-4">
        {values.title ?? t.singleTitle}{" "}
        {responseStateDimensionValue && (
          <DimensionBadge subjectDimensionValue={responseStateDimensionValue} />
        )}
      </h3>

      {response.programs.length > 0 && (
        <div className="alert alert-primary mt-4 mb-4">
          <p>{t.attributes.programs.message(response.programs.length)}</p>
          {response.programs.map((program) => (
            <div key={program.slug}>
              <Link
                className="link-subtle"
                href={`/${eventSlug}/program-admin/${program.slug}`}
                title={program.title}
              >
                {program.title}
              </Link>{" "}
              {stateDimension && (
                <>
                  {"("}
                  <DimensionValues
                    dimension={stateDimension}
                    cachedDimensions={
                      program.cachedDimensions as CachedDimensions
                    }
                  />
                  {")"}
                </>
              )}
            </div>
          ))}
          <p className="mt-3 mb-0">
            {t.attributes.programs.dimensionsWillNotBeUpdatedOnProgramItem(
              response.programs.length,
            )}
          </p>
        </div>
      )}

      {supersededBy ? (
        <OldVersionAlert
          supersededBy={supersededBy}
          basePath={`/${eventSlug}/program-offers`}
          messages={t.OldVersionAlert}
          className="mt-4 mb-4"
        />
      ) : (
        <>
          <div className="row mb-5 mt-4">
            {!!programDimensions?.length && (
              <div className="col-md-8">
                <div className="card mb-3 h-100">
                  <div className="card-body">
                    <h5 className="card-title mb-3">
                      {surveyT.attributes.dimensions}
                    </h5>
                    {/* TODO improve feedback of successful save */}
                    <DimensionValueSelectionForm
                      dimensions={programDimensions}
                      cachedDimensions={response.cachedDimensions}
                      translations={translations}
                      technicalDimensions="readonly"
                      readOnly={dimensionsReadOnly}
                      idPrefix="response-dimensions"
                      onChange={updateResponseDimensions.bind(
                        null,
                        eventSlug,
                        surveySlug,
                        responseId,
                      )}
                    />
                  </div>
                </div>
              </div>
            )}
            <div className="col">
              <ResponseHistorySidebar
                event={event}
                response={response}
                locale={locale}
                responsesBaseUrl={`/${event.slug}/program-offers`}
                session={session}
                messages={translations}
              />
            </div>
          </div>
        </>
      )}

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ProgramAdminView>
  );
}
