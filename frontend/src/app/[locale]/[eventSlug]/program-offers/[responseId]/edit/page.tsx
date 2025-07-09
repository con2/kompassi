import Link from "next/link";
import { notFound } from "next/navigation";

import { Alert } from "react-bootstrap";
import { submit } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramOfferEdit on FullResponseType {
    id
    revisionCreatedAt
    originalCreatedBy {
      fullName
      ...FullSelectedProfile
    }
    language
    values
    form {
      title
      description
      fields
      survey {
        slug
        cachedDefaultResponseDimensions
        profileFieldSelector {
          ...FullProfileFieldSelector
        }
      }
    }
    cachedDimensions
    supersededBy {
      ...ResponseRevision
    }
    oldVersions {
      ...ResponseRevision
    }
    canEdit(mode: ADMIN)
  }
`);

const query = graphql(`
  query ProgramOfferEditPage($eventSlug: String!, $responseId: String!) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        programOffer(id: $responseId) {
          ...ProgramOfferEdit
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
    variables: { eventSlug, responseId },
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
    variables: { eventSlug, responseId },
  });

  if (!data.event?.program?.programOffer) {
    notFound();
  }

  const t = translations.Program.ProgramOffer;

  const response = data.event.program.programOffer;
  const { event } = data;

  const { revisionCreatedAt, originalCreatedBy, form } = response;
  const { fields, survey, description, title } = form;

  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programOffers"
      searchParams={searchParams}
      actions={
        <Link
          className="btn btn-outline-danger"
          href={`/${event.slug}/program-offers/${response.id}`}
        >
          ❌ {t.actions.edit.cancel}
        </Link>
      }
    >
      <Alert variant="warning" className="mt-4">
        {t.actions.edit.editingOthers(
          <FormattedDateTime
            value={revisionCreatedAt}
            scope={event}
            session={session}
            locale={locale}
          />,
          originalCreatedBy?.fullName,
        )}
      </Alert>

      <h3 className="mb-3 mt-3">{title}</h3>
      <ParagraphsDangerousHtml html={description} />

      <form
        action={submit.bind(null, locale, event.slug, survey.slug, response.id)}
      >
        <SchemaForm
          fields={fields}
          messages={translations.SchemaForm}
          values={values}
        />
        <SubmitButton>{translations.Common.submit}</SubmitButton>
      </form>
    </ProgramAdminView>
  );
}
