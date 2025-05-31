import Link from "next/link";
import { notFound } from "next/navigation";

import Alert from "react-bootstrap/Alert";
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
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProfileSurveyEditResponse($locale: String!, $responseId: String!) {
    userRegistry {
      ...TransferConsentFormRegistry
    }

    profile {
      ...FullOwnProfile

      forms {
        response(id: $responseId) {
          id
          createdAt
          canEdit(mode: OWNER)
          values

          dimensions {
            ...DimensionBadge
          }

          form {
            title
            description
            language
            fields
            event {
              slug
              name
              timezone
            }
            survey {
              slug

              registry {
                ...TransferConsentFormRegistry
              }
              profileFieldSelector {
                ...FullProfileFieldSelector
              }
            }
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    responseId: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;

  return {
    title: `${t.ownResponsesTitle} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function ProfileSurveyEditResponsePage({ params }: Props) {
  const { locale, responseId } = params;
  const translations = getTranslations(locale);
  const session = await auth();
  const t = translations.Survey;

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: {
      responseId,
      locale,
    },
  });

  if (!data.profile?.forms?.response) {
    notFound();
  }

  const response = data.profile.forms.response;
  const { profile, userRegistry } = data;
  const { createdAt, form, canEdit } = response;

  if (!canEdit) {
    return <ViewContainer>{t.actions.editResponse.cannotEdit}</ViewContainer>;
  }

  const language = form.language;
  const { fields, survey, description, event } = form;
  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/profile/responses`}>
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.actions.editResponse.title}
          <ViewHeading.Sub>{form.title}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <Link
            className="btn btn-outline-danger"
            href={`/profile/responses/${response.id}`}
          >
            ❌ {t.actions.editResponse.cancel}
          </Link>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <Alert variant="warning">
        {t.actions.editResponse.editingOwn(
          <FormattedDateTime
            value={createdAt}
            scope={event}
            session={session}
            locale={locale}
          />,
        )}
      </Alert>

      <ParagraphsDangerousHtml html={description} />

      <form
        action={submit.bind(null, locale, event.slug, survey.slug, response.id)}
      >
        {survey.registry && (
          <TransferConsentForm
            profileFieldSelector={survey.profileFieldSelector}
            profile={profile}
            sourceRegistry={userRegistry}
            targetRegistry={survey.registry}
            translations={translations}
            consentGivenAt={response.createdAt}
            scope={event}
            locale={locale}
          />
        )}
        <SchemaForm
          fields={fields}
          messages={translations.SchemaForm}
          values={values}
        />
        <SubmitButton>{t.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
