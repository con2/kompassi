import Link from "next/link";
import { notFound } from "next/navigation";
import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";

import { submit } from "./actions";
import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { AlsoAvailableInLanguage } from "@/components/forms/AlsoAvailableInLanguage";
import { Field, validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { kompassiBaseUrl } from "@/config";
import {
  getTranslations,
  isSupportedLanguage,
  SupportedLanguage,
} from "@/translations";
import type { Translations } from "@/translations/en";

const query = graphql(`
  query SurveyPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    profile {
      displayName
      email
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
  const { event } = data;
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

  const profile = data.profile ?? {};
  let isSharedProfileFieldsShown = false;
  let sharedProfileFields: Field[] = [];

  // TODO(#402) Improved privacy choices, use profileFieldSelector
  if (data.profile && anonymity == "NAME_AND_EMAIL") {
    isSharedProfileFieldsShown = true;
    sharedProfileFields = [
      {
        slug: "displayName",
        type: "SingleLineText",
        title: translations.Profile.advancedAttributes.displayName.title,
      },
      {
        slug: "email",
        type: "SingleLineText",
        title: translations.Profile.advancedAttributes.email.title,
      },
    ];
  }
  const profileLink = `${kompassiBaseUrl}/profile`;

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
      {isSharedProfileFieldsShown && (
        <Card className="mb-4">
          <CardBody>
            <CardTitle>{t.theseProfileFieldsWillBeShared}</CardTitle>
            <p>{t.correctInYourProfile(profileLink)}</p>
            <SchemaForm
              fields={sharedProfileFields}
              values={profile}
              messages={translations.SchemaForm}
              readOnly={true}
            />
          </CardBody>
        </Card>
      )}
      <form action={submit.bind(null, locale, eventSlug, surveySlug)}>
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
