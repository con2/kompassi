import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import SurveyResponseAdminView from "@/components/response/SurveyResponseAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";
import { Alert } from "react-bootstrap";
import { submit } from "./actions";

graphql(`
  fragment EditSurveyResponsePage on FullResponseType {
    ...ResponseHistoryBanner

    id
    language
    values
    form {
      title
      description
      fields
      survey {
        slug
        profileFieldSelector {
          ...FullProfileFieldSelector
        }
      }
    }
    revisionCreatedAt
    originalCreatedBy {
      fullName
    }
    canEdit(mode: ADMIN)
  }
`);

const query = graphql(`
  query EditSurveyResponsePage(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      forms {
        survey(slug: $surveySlug) {
          response(id: $responseId) {
            ...EditSurveyResponsePage
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    surveySlug: string;
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
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Program.ProgramOffer;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const values: Values = data.event.forms.survey.response.values as any;

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
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const t = translations.Survey;

  const response = data.event.forms.survey.response;
  const { event } = data;

  const { revisionCreatedAt, originalCreatedBy, form } = response;
  const { fields, survey, description, title } = form;

  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  return (
    <SurveyResponseAdminView
      translations={translations}
      event={data.event}
      survey={survey}
      searchParams={searchParams}
      actions={
        <Link
          className="btn btn-outline-danger"
          href={`/${event.slug}/surveys/${survey.slug}/responses/${response.id}`}
        >
          ❌ {t.actions.editResponse.cancel}
        </Link>
      }
    >
      <Alert variant="warning" className="mt-4">
        {t.actions.editResponse.editingOthers(
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
    </SurveyResponseAdminView>
  );
}
