import { notFound } from "next/navigation";

import { graphql } from "@/__generated__";
import { SurveyPurpose } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { AlsoAvailableInLanguage } from "@/components/forms/AlsoAvailableInLanguage";
import { validateFields } from "@/components/forms/models";
import processFormData from "@/components/forms/processFormData";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import searchParamsToFormData from "@/helpers/searchParamsToFormData";
import { getTranslations } from "@/translations";
import { submit } from "./actions";

const query = graphql(`
  query SurveyPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    profile {
      ...FullOwnProfile
    }

    userRegistry {
      ...TransferConsentFormRegistry
    }

    event(slug: $eventSlug) {
      slug
      name
      timezone

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

export const revalidate = 0;

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    surveySlug: string;
  }>;
  searchParams: Promise<{
    [key: string]: string;
  }>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  if (data?.event?.forms?.survey?.loginRequired) {
    const session = await auth();
    if (!session) {
      return t.SignInRequired.metadata;
    }
  }

  return {
    title: `${data.event?.name}: ${data.event?.forms?.survey?.form?.title} – Kompassi`,
    description: data.event?.forms?.survey?.form?.description ?? "",
  };
}

export default async function SurveyPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });
  const { event, profile, userRegistry } = data;

  if (!event?.forms?.survey) {
    notFound();
  }

  if (!event.forms.survey.form) {
    return (
      <ViewContainer>
        <ViewHeading>{t.errors.noLanguageVersions.title}</ViewHeading>
        <p>{t.errors.noLanguageVersions.message}</p>
      </ViewContainer>
    );
  }

  const {
    languages,
    loginRequired,
    maxResponsesPerUser,
    countResponsesByCurrentUser,
    purpose,
    profileFieldSelector,
    isActive,
    registry: targetRegistry,
  } = event.forms.survey;
  if (!isActive) {
    return (
      <ViewContainer>
        <ViewHeading>{t.errors.surveyNotActive.title}</ViewHeading>
        <p>{t.errors.surveyNotActive.message}</p>
      </ViewContainer>
    );
  }

  const { title, description, fields, language } = event.forms.survey.form;

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

  const searchParams = await props.searchParams;
  const urlSearchParams = new URLSearchParams(searchParams);
  const formData = searchParamsToFormData(urlSearchParams);
  const values = processFormData(
    fields.filter((field) => field.type != "FileUpload"),
    formData,
  );
  let queryString = urlSearchParams.toString();
  if (queryString) {
    queryString = `?${queryString}`;
  }

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <AlsoAvailableInLanguage
        language={language}
        languages={languages}
        path={`/${eventSlug}/${surveySlug}${queryString}`}
      />

      {/* TODO No good way currently to separate "not logged in" and "not active and not admin" from "not active and admin override" */}
      {/* {!isActive && (
        <div className="alert alert-warning">
          <h5>{t.attributes.isActive.adminOverride.title}</h5>
          <p className="mb-0">{t.attributes.isActive.adminOverride.message}</p>
        </div>
      )} */}

      <ParagraphsDangerousHtml html={description} />
      <form action={submit.bind(null, locale, eventSlug, surveySlug)}>
        {targetRegistry && profile && (
          <TransferConsentForm
            profileFieldSelector={profileFieldSelector}
            profile={profile}
            sourceRegistry={userRegistry}
            targetRegistry={targetRegistry}
            translations={translations}
            scope={event}
            locale={locale}
          />
        )}
        <SchemaForm
          fields={fields}
          values={values}
          messages={translations.SchemaForm}
        />
        <SubmitButton>{t.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
