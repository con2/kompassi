import Link from "next/link";
import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { validateFields } from "@/components/forms/models";
import { ResponseHistory } from "@/components/forms/ResponseHistory";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

const query = graphql(`
  query ProfileSurveyResponsePage($locale: String!, $responseId: String!) {
    userRegistry {
      ...TransferConsentFormRegistry
    }

    profile {
      ...FullOwnProfile

      forms {
        response(id: $responseId) {
          id
          revisionCreatedAt
          canEdit(mode: OWNER)
          values

          supersededBy {
            id
            revisionCreatedAt
          }

          dimensions {
            ...DimensionBadge
          }

          oldVersions {
            ...ResponseRevision
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
              profileFieldSelector {
                ...FullProfileFieldSelector
              }
              registry {
                ...TransferConsentFormRegistry
              }
            }
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    responseId: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;

  return {
    title: `${t.ownResponsesTitle} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function ProfileSurveyResponsePage(props: Props) {
  const params = await props.params;
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
  const { form, canEdit, oldVersions, supersededBy } = response;
  const { survey, event } = form;

  const { fields } = form;
  const values: Record<string, any> = response.values ?? {};

  validateFields(fields);

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/profile/responses`}>
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.responseDetailTitle}
          <ViewHeading.Sub>{form.title}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          {canEdit && (
            <Link
              className="btn btn-outline-primary"
              href={`/profile/responses/${responseId}/edit`}
            >
              ✏️ {t.actions.editResponse.title}
            </Link>
          )}
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <ResponseHistory
        basePath="/profile/responses"
        supersededBy={supersededBy}
        oldVersions={oldVersions}
        messages={translations.Survey}
        locale={locale}
        scope={event}
      />

      <ParagraphsDangerousHtml html={form.description} />

      {survey.registry && (
        <TransferConsentForm
          profileFieldSelector={survey.profileFieldSelector}
          profile={profile}
          sourceRegistry={userRegistry}
          targetRegistry={survey.registry}
          translations={translations}
          consentGivenAt={response.revisionCreatedAt}
          scope={event}
          locale={locale}
        />
      )}

      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly
      />
    </ViewContainer>
  );
}
