import { notFound } from "next/navigation";

import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import { acceptInvitation } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import SignInRequired from "@/components/errors/SignInRequired";
import { AlsoAvailableInLanguage } from "@/components/forms/AlsoAvailableInLanguage";
import { validateFields } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import SubmitButton from "@/components/forms/SubmitButton";
import Linebreaks from "@/components/helpers/Linebreaks";
import ParagraphsDangerousHtml from "@/components/helpers/ParagraphsDangerousHtml";
import TransferConsentForm from "@/components/involvement/TransferConsentForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

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
      ...FullOwnProfile
    }

    userRegistry {
      ...TransferConsentFormRegistry
    }

    event(slug: $eventSlug) {
      slug
      name
      timezone

      involvement {
        invitation(invitationId: $invitationId) {
          isUsed

          program {
            slug
            title
            description
          }

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

  const session = await auth();
  if (!session) {
    return t.SignInRequired.metadata;
  }

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

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, invitationId, locale },
  });

  const { event, profile } = data;
  if (!event?.involvement?.invitation?.survey?.form) {
    notFound();
  }

  if (!profile) {
    throw new Error("Null profile for signed-in user");
  }

  const { survey, isUsed, program } = event.involvement.invitation;
  if (isUsed) {
    return (
      <ViewContainer>
        <ViewHeading>{t.errors.alreadyUsed.title}</ViewHeading>
        <p>{t.errors.alreadyUsed.message}</p>
      </ViewContainer>
    );
  }

  const { languages, isActive } = event.involvement.invitation.survey;
  if (!languages || languages.length === 0) {
    return (
      <ViewContainer>
        <ViewHeading>{surveyT.errors.noLanguageVersions.title}</ViewHeading>
        <p>{surveyT.errors.noLanguageVersions.message}</p>
      </ViewContainer>
    );
  }
  if (!isActive) {
    return (
      <ViewContainer>
        <ViewHeading>{surveyT.errors.surveyNotActive.title}</ViewHeading>
        <p>{surveyT.errors.surveyNotActive.message}</p>
      </ViewContainer>
    );
  }

  const { title, description, fields, language } =
    event.involvement.invitation.survey.form;

  const userRegistry = data.userRegistry;
  const targetRegistry = survey.registry;
  if (!targetRegistry) {
    throw new Error("Survey used for accepting invitation has no registry");
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

      {program && (
        <Card>
          <CardBody>
            <CardTitle>{t.attributes.program.title}</CardTitle>
            {(["title", "description"] as const).map((field) => (
              <div key={field} className="mt-2">
                <div>
                  <strong>{translations.Program.attributes[field]}</strong>
                </div>
                <Linebreaks text={program[field]} />
              </div>
            ))}
            <div className="mt-2 form-text">
              {t.attributes.program.editLater}
            </div>
          </CardBody>
        </Card>
      )}

      <form
        action={acceptInvitation.bind(
          null,
          locale,
          eventSlug,
          survey.slug,
          invitationId,
        )}
      >
        <TransferConsentForm
          profileFieldSelector={survey.profileFieldSelector}
          profile={profile}
          sourceRegistry={userRegistry}
          targetRegistry={targetRegistry}
          translations={translations}
          scope={event}
          locale={locale}
        />

        <SchemaForm fields={fields} messages={translations.SchemaForm} />
        <SubmitButton>{surveyT.actions.submit}</SubmitButton>
      </form>
    </ViewContainer>
  );
}
