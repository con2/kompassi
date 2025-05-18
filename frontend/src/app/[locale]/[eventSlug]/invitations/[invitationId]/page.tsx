import { notFound } from "next/navigation";

import { acceptInvitation } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { AlsoAvailableInLanguage } from "@/components/forms/AlsoAvailableInLanguage";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

graphql(`
  fragment FullProfile on ProfileType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

graphql(`
  fragment FullProfileFieldSelector on ProfileFieldSelectorType {
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

graphql(`
  fragment TransferConsentFormRegistry on LimitedRegistryType {
    organization {
      slug
      name
    }
    slug
    title(lang: $locale)
    policyUrl(lang: $locale)
  }
`);

const query = graphql(`
  query AcceptInvitationPage(
    $eventSlug: String!
    $invitationId: String!
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

      involvement {
        invitation(invitationId: $invitationId) {
          isUsed
          survey {
            slug
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
  }
`);

export const revalidate = 5;

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    invitationId: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, invitationId } = params;
  const t = getTranslations(locale);
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, invitationId, locale },
  });
  return {
    title: `${data.event?.name}: ${data.event?.involvement?.invitation?.survey?.form?.title} – Kompassi`,
    description:
      data.event?.involvement?.invitation?.survey?.form?.description ?? "",
  };
}

export default async function SurveyPage({ params }: Props) {
  const { locale, eventSlug, invitationId } = params;
  const translations = getTranslations(locale);
  const surveyT = translations.Survey;
  const t = translations.Invitation;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, invitationId, locale },
  });

  const { event, profile } = data;
  if (!event?.involvement?.invitation?.survey?.form || !profile) {
    notFound();
  }

  const { survey, isUsed } = event.involvement.invitation;
  if (isUsed) {
    return (
      <ViewContainer>
        <ViewHeading>{t.errors.alreadyUsed.title}</ViewHeading>
        <p>{t.errors.alreadyUsed.message}</p>
      </ViewContainer>
    );
  }

  const { languages, isActive } = event.involvement.invitation.survey;
  const { title, description, fields, language } =
    event.involvement.invitation.survey.form;

  const userRegistry = data.userRegistry;
  const targetRegistry = survey.registry;
  if (!targetRegistry) {
    throw new Error("Survey used for accepting invitation has no registry");
  }

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  validateFields(fields);

  return (
    <ViewContainer>
      <ViewHeading>
        {title}
        <ViewHeading.Sub>{surveyT.forEvent(event.name)}</ViewHeading.Sub>
      </ViewHeading>

      <AlsoAvailableInLanguage
        language={language}
        languages={languages}
        path={`/${eventSlug}/invitations/${invitationId}`}
      />

      {!isActive && (
        <div className="alert alert-warning">
          <h5>{surveyT.attributes.isActive.adminOverride.title}</h5>
          <p className="mb-0">
            {surveyT.attributes.isActive.adminOverride.message}
          </p>
        </div>
      )}

      <ParagraphsDangerousHtml html={description} />

      <TransferConsentForm
        profileFieldSelector={survey.profileFieldSelector}
        profile={profile}
        sourceRegistry={userRegistry}
        targetRegistry={targetRegistry}
        translations={translations}
      />

      <form
        action={acceptInvitation.bind(
          null,
          locale,
          eventSlug,
          survey.slug,
          invitationId,
        )}
      >
        <SchemaForm fields={fields} messages={translations.SchemaForm} />
        <SubmitButton>{surveyT.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
