import Link from "next/link";
import { notFound } from "next/navigation";

import { updateResponseDimensions } from "../../surveys/[surveySlug]/responses/[responseId]/actions";
import { acceptProgramOffer } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import AutoSubmitForm from "@/components/AutoSubmitForm";
import { buildDimensionForm } from "@/components/dimensions/helpers";
import { Dimension } from "@/components/dimensions/models";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import slugify from "@/helpers/slugify";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramOfferDetail on FullResponseType {
    id
    sequenceNumber
    createdAt
    createdBy {
      displayName
      email
    }
    language
    values
    form {
      fields
      survey {
        title(lang: $locale)
        slug
      }
    }
    cachedDimensions
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
      program {
        dimensions(publicOnly: false) {
          slug
          title(lang: $locale)

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
  const queryString = new URLSearchParams(searchParams).toString();

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

  const { sequenceNumber, createdAt, form } = data.event.program.programOffer;
  const { fields } = form;

  const programOffer = data.event.program.programOffer;
  const values: Record<string, any> = programOffer.values ?? {};

  validateFields(fields);

  // TODO using synthetic form fields for presentation is a hack
  // but it shall suffice until someone comes up with a Design Vision™
  const technicalFields: Field[] = [
    {
      slug: "sequenceNumber",
      type: "SingleLineText",
      title: surveyT.attributes.sequenceNumber,
    },
    {
      slug: "createdAt",
      // TODO(#438) use DateTimeField
      type: "SingleLineText",
      title: surveyT.attributes.createdAt,
    },
    {
      slug: "createdBy",
      type: "SingleLineText",
      title: surveyT.attributes.createdBy,
    },
  ];

  // TODO(#438) use DateTimeField
  const formattedCreatedAt = createdAt ? formatDateTime(createdAt, locale) : "";
  const createdBy = programOffer.createdBy;
  const formattedCreatedBy = createdBy
    ? `${createdBy.displayName} <${createdBy.email}>`
    : "-";

  const technicalValues = {
    sequenceNumber,
    createdAt: formattedCreatedAt,
    createdBy: formattedCreatedBy,
  };

  const dimensions: Dimension[] = data.event.program.dimensions;
  const { fields: dimensionFields, values: dimensionValues } =
    buildDimensionForm(dimensions, programOffer.cachedDimensions);

  const acceptProgramOfferFields: Field[] = [
    {
      slug: "message",
      type: "StaticText",
      helpText: t.actions.accept.message,
    },
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
    {
      slug: "dimensionsHeader",
      type: "StaticText",
      title: surveyT.attributes.dimensions,
    },
    ...dimensionFields,
  ];

  const acceptProgramOfferValues: Record<string, any> = {
    slug: slugify(values.title || ""),
    title: values.title,
    description: values.description,
    ...dimensionValues,
  };

  // XXX specialized updateProgramOfferDimensions instead of generic updateResponseDimensions
  const surveySlug = programOffer.form.survey!.slug;

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programOffers"
      queryString={queryString}
      actions={
        <ModalButton
          className="btn btn-outline-primary"
          label={t.actions.accept.title + "…"}
          title={t.actions.accept.title}
          messages={t.actions.accept.modalActions}
          action={acceptProgramOffer.bind(null, locale, eventSlug, responseId)}
        >
          <SchemaForm
            fields={acceptProgramOfferFields}
            values={acceptProgramOfferValues}
            messages={translations.SchemaForm}
            headingLevel="h4"
          />
        </ModalButton>
      }
    >
      <div className="row mb-5 mt-3">
        {!!dimensions?.length && (
          <div className="col-md-8">
            <div className="card mb-3 h-100">
              <div className="card-body">
                <h5 className="card-title mb-3">
                  {surveyT.attributes.dimensions}
                </h5>
                {/* TODO improve feedback of successful save */}
                <AutoSubmitForm
                  action={updateResponseDimensions.bind(
                    null,
                    eventSlug,
                    surveySlug,
                    responseId,
                  )}
                >
                  <SchemaForm
                    fields={dimensionFields}
                    values={dimensionValues}
                    messages={translations.SchemaForm}
                  />
                  <noscript>
                    <SubmitButton>
                      {surveyT.actions.saveDimensions}
                    </SubmitButton>
                  </noscript>
                </AutoSubmitForm>
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
              <SchemaForm
                fields={technicalFields}
                values={technicalValues}
                messages={translations.SchemaForm}
                readOnly
              />
            </div>
          </div>
        </div>
      </div>

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ProgramAdminView>
  );
}
