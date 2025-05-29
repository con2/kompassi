import { notFound } from "next/navigation";

import { submit } from "./actions";
import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { AlsoAvailableInLanguage } from "@/components/forms/AlsoAvailableInLanguage";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";

const query = graphql(`
  query SurveyPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    profile {
      ...FullProfile
    }

    userRegistry {
      ...TransferConsentFormRegistry
    }

    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug, app: null) {
          loginRequired
          anonymity
          maxResponsesPerUser
          countResponsesByCurrentUser
          isActive
          purpose

          profileFieldSelector {
            ...FullProfileFieldSelector
          }

          registry {
            ...TransferConsentFormRegistry
          }

          form(lang: $locale) {
            language
            title
            description
            fields
          }

          languages {
            language
          }
        }
      }
    }
  }
`);

export const revalidate = 5;

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.forms?.survey?.form?.title} – Kompassi`,
    description: data.event?.forms?.survey?.form?.description ?? "",
  };
}

export default async function SurveyPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  const { event, profile, userRegistry } = data;
  if (!event?.forms?.survey?.form) {
    notFound();
  }
  const {
    languages,
    loginRequired,
    anonymity,
    maxResponsesPerUser,
    countResponsesByCurrentUser,
    purpose,
    profileFieldSelector,
    registry: targetRegistry,
  } = event.forms.survey;
  const { isActive } = event.forms.survey;
  const { title, description, fields, language } = event.forms.survey.form;
  const anonymityMessages = t.attributes.anonymity.secondPerson;

  if (loginRequired) {
    const session = await auth();
    if (!session) {
      return <SignInRequired messages={translations.SignInRequired} />;
    }
  }

  if (purpose !== SurveyPurpose.Default) {
    return (
      <ViewContainer>
        <ViewHeading>{t.specialPurposeSurvey.title}</ViewHeading>
        <p>{t.specialPurposeSurvey.defaultMessage}</p>
      </ViewContainer>
    );
  }

  if (maxResponsesPerUser && countResponsesByCurrentUser) {
    if (countResponsesByCurrentUser >= maxResponsesPerUser) {
      return (
        <ViewContainer>
          <ViewHeading>{t.maxResponsesPerUserReached.title}</ViewHeading>
          <p>
            {t.maxResponsesPerUserReached.defaultMessage(
              maxResponsesPerUser,
              countResponsesByCurrentUser,
            )}
          </p>
        </ViewContainer>
      );
    }
  }

  validateFields(fields);

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <AlsoAvailableInLanguage
        language={language}
        languages={languages}
        path={`/${eventSlug}/${surveySlug}`}
      />

      {!isActive && (
        <div className="alert alert-warning">
          <h5>{t.attributes.isActive.adminOverride.title}</h5>
          <p className="mb-0">{t.attributes.isActive.adminOverride.message}</p>
        </div>
      )}

      <ParagraphsDangerousHtml html={description} />
      <form action={submit.bind(null, locale, eventSlug, surveySlug)}>
        {targetRegistry && profile && (
          <TransferConsentForm
            profileFieldSelector={profileFieldSelector}
            profile={profile}
            sourceRegistry={userRegistry}
            targetRegistry={targetRegistry}
            translations={translations}
          />
        )}
        <SchemaForm fields={fields} messages={translations.SchemaForm} />
        <SubmitButton>{t.actions.submit}</SubmitButton>
      </form>
      <p className="mt-3">
        <small>
          <strong>{anonymityMessages.title}: </strong>
          {anonymityMessages.choices[anonymity]}
        </small>
      </p>
    </ViewContainer>
  );
}
