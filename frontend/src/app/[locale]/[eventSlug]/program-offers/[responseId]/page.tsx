import Link from "next/link";
import { notFound } from "next/navigation";

import { Fragment } from "react";
import { ButtonGroup } from "react-bootstrap";
import { updateResponseDimensions } from "../../surveys/[surveySlug]/responses/[responseId]/actions";
import { acceptProgramOffer, cancelProgramOffer } from "./actions";
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
  Dimension,
  validateCachedDimensions,
} from "@/components/dimensions/models";
import Messages from "@/components/errors/Messages";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field, validateFields } from "@/components/forms/models";
import { OldVersionAlert } from "@/components/forms/OldVersionAlert";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import { ProfileFields } from "@/components/profile/ProfileFields";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import slugify from "@/helpers/slugify";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramOfferDetail on FullResponseType {
    id
    sequenceNumber
    originalCreatedAt
    originalCreatedBy {
      fullName
      ...FullSelectedProfile
    }
    revisionCreatedAt
    revisionCreatedBy {
      fullName
    }
    language
    values
    form {
      description
      fields
      survey {
        title(lang: $locale)
        slug
        cachedDefaultResponseDimensions
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
    cachedDimensions
    supersededBy {
      ...ResponseRevision
    }
    oldVersions {
      ...ResponseRevision
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

      program {
        dimensions(publicOnly: false) {
          slug
          title(lang: $locale)
          isTechnical
          isMultiValue

          values(lang: $locale) {
            slug
            title(lang: $locale)
          }
        }

        programOffer(id: $responseId) {
          ...ProgramOfferDetail
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    responseId: string;
  };
  searchParams: Record<string, string>;
}

interface Values {
  title?: string;
  description?: string;
}

export async function generateMetadata({ params }: Props) {
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

export default async function ProgramOfferPage({
  params,
  searchParams,
}: Props) {
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
  const t = translations.Program.ProgramOffer;

  const programOffer = data.event.program.programOffer;
  const { event } = data;
  const {
    originalCreatedAt,
    originalCreatedBy,
    revisionCreatedAt,
    revisionCreatedBy,
    form,
    supersededBy,
    oldVersions,
    canEdit,
  } = programOffer;
  const { fields, survey: programForm } = form;

  const values: Record<string, any> = programOffer.values ?? {};
  const { canAccept, canCancel, canDelete } = programOffer;

  validateFields(fields);

  validateCachedDimensions(programOffer.cachedDimensions);
  const dimensions: Dimension[] = data.event.program.dimensions;
  const defaultDimensions =
    programOffer.form.survey.cachedDefaultResponseDimensions ?? {};
  const { fields: dimensionFields, values: dimensionValues } =
    buildDimensionValueSelectionForm(dimensions, {
      ...defaultDimensions,
      ...programOffer.cachedDimensions,
    });

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

  if (dimensions.filter((dimension) => !dimension.isTechnical).length > 0) {
    acceptProgramOfferFields.push(
      {
        slug: "dimensionsHeader",
        type: "StaticText",
        title: surveyT.attributes.dimensions,
      },
      ...dimensionFields,
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
    programOffer.programs.length > 0 ? `-${programOffer.programs.length}` : "";
  const acceptProgramOfferValues: Record<string, any> = {
    slug: slugify(values.title || "") + uniquenessInsurance,
    title: values.title,
    description: values.description,
    ...dimensionValues,
  };

  const surveySlug = programOffer.form.survey!.slug;
  const dimensionsReadOnly = !!supersededBy;

  const stateDimension = dimensions.find((d) => d.slug === "state");
  const responseStateDimensionValue = programOffer.dimensions.find(
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
              {programOffer.programs.length > 0 && (
                <div className="alert alert-warning">
                  <p>
                    {t.attributes.programs.acceptAgainWarning(
                      programOffer.programs.length,
                    )}
                  </p>
                  {programOffer.programs.map((program) => (
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
              <p>{t.actions.cancel.message}</p>
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

      <Messages messages={t.messages} searchParams={searchParams} />

      {programOffer.programs.length > 0 && (
        <div className="alert alert-primary mt-4 mb-4">
          <p>{t.attributes.programs.message(programOffer.programs.length)}</p>
          {programOffer.programs.map((program) => (
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
              programOffer.programs.length,
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
            {!!dimensions?.length && (
              <div className="col-md-8">
                <div className="card mb-3 h-100">
                  <div className="card-body">
                    <h5 className="card-title mb-3">
                      {surveyT.attributes.dimensions}
                    </h5>
                    {/* TODO improve feedback of successful save */}
                    <DimensionValueSelectionForm
                      dimensions={dimensions}
                      cachedDimensions={programOffer.cachedDimensions}
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
              <div className="card mb-3 h-100">
                <div className="card-body">
                  <h5 className="card-title mb-3">
                    {surveyT.attributes.technicalDetails}
                  </h5>

                  <div className="mb-4">
                    <label className="form-label fw-bold">
                      {surveyT.attributes.originalCreatedAt}
                    </label>
                    <div>
                      <FormattedDateTime
                        value={originalCreatedAt}
                        locale={locale}
                        scope={event}
                        session={session}
                      />
                    </div>
                  </div>

                  {originalCreatedBy && (
                    <div className="mb-4">
                      <label className="form-label fw-bold">
                        {surveyT.attributes.originalCreatedBy}
                      </label>
                      <div>
                        <ModalButton
                          className="btn btn-link p-0 link-subtle"
                          label={originalCreatedBy.fullName + "…"}
                          title={surveyT.actions.viewProfile.title}
                          messages={surveyT.actions.viewProfile.modalActions}
                        >
                          <ProfileFields
                            profileFieldSelector={
                              programForm.profileFieldSelector
                            }
                            profile={originalCreatedBy}
                            messages={translations.Profile}
                          />
                        </ModalButton>
                      </div>
                    </div>
                  )}

                  {oldVersions.length > 0 && (
                    <>
                      <div className="mb-4">
                        <label className="form-label fw-bold">
                          {surveyT.attributes.currentVersionCreatedAt}
                        </label>
                        <div>
                          <FormattedDateTime
                            value={revisionCreatedAt}
                            locale={locale}
                            scope={event}
                            session={session}
                          />
                        </div>
                      </div>

                      {revisionCreatedBy && (
                        <div className="mb-4">
                          <label className="form-label fw-bold">
                            {surveyT.attributes.currentVersionCreatedBy}
                          </label>
                          <div>{revisionCreatedBy.fullName}</div>
                        </div>
                      )}

                      <div className="mb-4">
                        <label className="form-label fw-bold">
                          {surveyT.ResponseHistory.title}
                        </label>
                        <ul className="list-unstyled m-0">
                          {oldVersions.map((version) => (
                            <li key={version.id}>
                              <Link
                                href={`/${event.slug}/program-offers/${version.id}`}
                                className="link-subtle"
                              >
                                <FormattedDateTime
                                  value={version.revisionCreatedAt}
                                  locale={locale}
                                  scope={event}
                                  session={session}
                                />
                                {version.revisionCreatedBy && (
                                  <>
                                    {" "}
                                    ({version.revisionCreatedBy?.displayName})
                                  </>
                                )}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </>
                  )}
                </div>
              </div>
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
