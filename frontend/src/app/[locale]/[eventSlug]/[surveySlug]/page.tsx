import Link from "next/link";
import { notFound } from "next/navigation";

import { Fragment, ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import { submit } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
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
import { Translations } from "@/translations/en";

// NOTE SUPPORTED_LANGUAGES
import en from "@/translations/en";
import fi from "@/translations/fi";
import sv from "@/translations/sv";

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
        survey(slug: $surveySlug) {
          loginRequired
          anonymity
          maxResponsesPerUser
          countResponsesByCurrentUser

          form(lang: $locale) {
            title
            description
            fields
            layout
          }

          languages {
            language
          }
        }
      }
    }
  }
`);

// NOTE SUPPORTED_LANGUAGES
// XXX ugly
const alsoAvailableIn: Record<
  SupportedLanguage,
  Translations["Survey"]["attributes"]["alsoAvailableInThisLanguage"]
> = {
  en: en.Survey.attributes.alsoAvailableInThisLanguage,
  fi: fi.Survey.attributes.alsoAvailableInThisLanguage,
  sv: sv.Survey.attributes.alsoAvailableInThisLanguage,
};

interface SurveyPageProps {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export const revalidate = 5;

export async function generateMetadata({ params }: SurveyPageProps) {
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

export default async function SurveyPage({ params }: SurveyPageProps) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  const { event } = data;
  if (!event) {
    notFound();
  }
  const survey = event.forms?.survey;
  if (!survey) {
    notFound();
  }
  const {
    form,
    loginRequired,
    anonymity,
    maxResponsesPerUser,
    countResponsesByCurrentUser,
  } = survey;
  const { title, description, layout, fields } = form!;
  const anonymityMessages = t.attributes.anonymity.secondPerson;

  if (loginRequired) {
    const session = await auth();
    if (!session) {
      return <SignInRequired messages={translations.SignInRequired} />;
    }
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
  if (data.profile && anonymity == "NAME_AND_EMAIL") {
    isSharedProfileFieldsShown = true;
    sharedProfileFields = [
      {
        slug: "displayName",
        type: "SingleLineText",
        title: translations.Profile.attributes.displayName.title,
      },
      {
        slug: "email",
        type: "SingleLineText",
        title: translations.Profile.attributes.email.title,
      },
    ];
  }
  const profileLink = `${kompassiBaseUrl}/profile`;

  const otherLanguages: SupportedLanguage[] = survey.languages
    .map((languageObj) => languageObj.language.toLowerCase())
    .filter((language) => language != locale)
    .filter(isSupportedLanguage);

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>
      {otherLanguages.length > 0 && (
        <div className="alert alert-primary">
          {otherLanguages.map((language) => {
            function LanguageLink({ children }: { children: ReactNode }) {
              return (
                <Link
                  prefetch={false}
                  href={`/${language}/${eventSlug}/${surveySlug}`}
                  lang={language}
                >
                  {children}
                </Link>
              );
            }

            return (
              <div key={language} lang={language}>
                {alsoAvailableIn[language](LanguageLink)}{" "}
              </div>
            );
          })}
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
        <SchemaForm
          fields={fields}
          layout={layout}
          messages={translations.SchemaForm}
        />
        <SubmitButton layout={layout}>{t.actions.submit}</SubmitButton>
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
