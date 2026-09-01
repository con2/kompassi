import {
  Markdown,
  SignInRequired,
  SubmitButton,
  FormattedDateTime,
} from "@con2/components";
import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { Alert } from "react-bootstrap";
import { submit } from "../../../../../surveys/[surveySlug]/responses/[responseId]/edit/actions";
import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramFormResponseEdit on FullResponseType {
    id
    revisionCreatedAt
    originalCreatedBy {
      fullName
    }
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
  }
`);

const query = graphql(`
  query ProgramFormResponseEditPage(
    $eventSlug: String!
    $surveySlug: String!
    $responseId: String!
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      forms {
        survey(slug: $surveySlug, app: PROGRAM) {
          purpose

          response(id: $responseId) {
            ...ProgramFormResponseEdit
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

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const values: Values = data.event.forms.survey.response.values as any;

  const title = getPageTitle({
    viewTitle: t.responseDetailTitle,
    subject: values.title || "",
    event: data.event,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function ProgramFormResponseEditPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, surveySlug, responseId } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const session = await auth();

  // TODO encap
  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, responseId },
  });

  if (!data.event?.forms?.survey?.response) {
    notFound();
  }

  const survey = data.event.forms.survey;

  if (survey.purpose === SurveyPurpose.Default) {
    redirect(`/${eventSlug}/program-offers/${responseId}/edit`);
  }

  const response = survey.response;
  if (!response) {
    notFound();
  }

  const { event } = data;
  const { revisionCreatedAt, originalCreatedBy, form } = response;
  const { fields, survey: formSurvey, description, title } = form;

  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programForms"
      searchParams={searchParams}
      actions={
        <Link
          className="btn btn-outline-danger"
          href={`/${eventSlug}/program-forms/${surveySlug}/responses/${responseId}`}
        >
          ❌ {t.actions.editResponse.cancel}
        </Link>
      }
    >
      <Alert variant="warning" className="mt-4">
        {t.actions.editResponse.editingOthers(
          <FormattedDateTime value={revisionCreatedAt} locale={locale} />,
          originalCreatedBy?.fullName,
        )}
      </Alert>

      <h3 className="mb-3 mt-3">{title}</h3>
      <Markdown input={description} />

      <form
        action={submit.bind(
          null,
          locale,
          event.slug,
          formSurvey.slug,
          response.id,
          `${eventSlug}/program-forms/${surveySlug}/responses`,
        )}
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
