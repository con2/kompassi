import { notFound } from "next/navigation";

import ButtonGroup from "react-bootstrap/ButtonGroup";
import {
  inviteProgramHost,
  deleteProgramHost,
  revokeInvitation,
  resendInvitation,
} from "./actions";
import { graphql } from "@/__generated__";
import {
  ProgramAdminDetailHostFragment,
  ProgramAdminDetailInvitationFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import AlertNavigateOnClose from "@/components/AlertNavigateOnClose";
import { Column, DataTable } from "@/components/DataTable";
import FormattedDateTime from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations, SupportedLanguage } from "@/translations";

graphql(`
  fragment ProgramAdminDetailHost on LimitedInvolvementType {
    id
    person {
      fullName
      firstName
      lastName
      nick
      email
      phoneNumber
      discordHandle
    }
  }
`);

graphql(`
  fragment ProgramAdminDetailInvitation on LimitedInvitationType {
    id
    email
    createdAt
  }
`);

const query = graphql(`
  query ProgramAdminDetailHosts(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      forms {
        inviteForms: surveys(
          includeInactive: true
          app: PROGRAM_V2
          purpose: INVITE
        ) {
          slug
          title(lang: $locale)
        }
      }

      program {
        program(slug: $programSlug) {
          slug
          title
          programHosts {
            ...ProgramAdminDetailHost
          }
          invitations {
            ...ProgramAdminDetailInvitation
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    programSlug: string;
  };
  searchParams: {
    resent?: string;
  };
}

export const revalidate = 0;

// must be in sync with the supported languages in Invitation.send in backend
const supportedInviteLanguages: SupportedLanguage[] = ["fi", "en"];

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.ProgramHost.listTitle,
    subject: data?.event?.program?.program?.title,
  });
  return { title };
}

export default async function ProgramAdminDetailPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const profileT = translations.Profile;
  const inviT = translations.Invitation;
  const t = translations.Program.ProgramHost;

  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  if (!data.event?.program?.program) {
    notFound();
  }

  const event = data.event;
  const program = data.event.program.program;
  const programHosts = data.event.program.program.programHosts;
  const invitations = data.event.program.program.invitations;

  const programHostColumns: Column<ProgramAdminDetailHostFragment>[] = [
    {
      slug: "lastName",
      title: profileT.advancedAttributes.lastName.title,
      getCellContents: (row) => row.person.lastName,
    },
    {
      slug: "firstName",
      title: profileT.advancedAttributes.firstName.title,
      getCellContents: (row) => row.person.firstName,
    },
    {
      slug: "nick",
      title: profileT.advancedAttributes.nick.title,
      getCellContents: (row) => row.person.nick,
    },
    {
      slug: "email",
      title: profileT.advancedAttributes.email.title,
      getCellContents: (row) => row.person.email,
    },
    {
      slug: "phoneNumber",
      title: profileT.advancedAttributes.phoneNumber.title,
      getCellContents: (row) => row.person.phoneNumber,
    },
    {
      slug: "discordHandle",
      title: profileT.advancedAttributes.discordHandle.title,
      getCellContents: (row) => row.person.discordHandle,
    },
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => (
        <ModalButton
          className="btn btn-outline-danger btn-sm"
          label={t.actions.removeProgramHost.label + "…"}
          title={t.actions.removeProgramHost.title}
          messages={t.actions.removeProgramHost.modalActions}
          submitButtonVariant="danger"
          action={deleteProgramHost.bind(
            null,
            locale,
            eventSlug,
            programSlug,
            row.id,
          )}
        >
          {t.actions.removeProgramHost.message(
            row.person.fullName,
            program.title,
          )}
        </ModalButton>
      ),
    },
  ];

  const invitationColumns: Column<ProgramAdminDetailInvitationFragment>[] = [
    {
      slug: "createdAt",
      title: inviT.attributes.createdAt,
      getCellContents: (row) => (
        <FormattedDateTime
          locale={locale}
          value={row.createdAt}
          scope={event}
          session={session}
        />
      ),
    },
    {
      slug: "email",
      title: inviT.attributes.email,
    },
    {
      slug: "actions",
      title: "",
      className: "text-end",
      getCellContents: (row) => (
        <ButtonGroup>
          <ModalButton
            className="btn btn-outline-primary btn-sm"
            label={inviT.actions.resend.label + "…"}
            title={inviT.actions.resend.title}
            messages={inviT.actions.resend.modalActions}
            submitButtonVariant="primary"
            action={resendInvitation.bind(
              null,
              locale,
              eventSlug,
              program.slug,
              row.id,
            )}
          >
            {inviT.actions.resend.message(row.email)}
          </ModalButton>
          <ModalButton
            className="btn btn-outline-danger btn-sm"
            label={inviT.actions.revoke.label + "…"}
            title={inviT.actions.revoke.title}
            messages={inviT.actions.revoke.modalActions}
            submitButtonVariant="danger"
            action={revokeInvitation.bind(
              null,
              locale,
              eventSlug,
              program.slug,
              row.id,
            )}
          >
            {inviT.actions.revoke.message(row.email)}
          </ModalButton>
        </ButtonGroup>
      ),
    },
  ];

  const inviteProgramHostFields: Field[] = [
    {
      slug: "email",
      type: "SingleLineText",
      htmlType: "email",
      required: true,
      ...t.actions.inviteProgramHost.attributes.email,
    },
    {
      slug: "surveySlug",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      choices:
        data.event.forms?.inviteForms.map(({ slug, title }) => ({
          slug,
          title: `${slug}: ${title}`,
        })) ?? [],
      ...t.actions.inviteProgramHost.attributes.survey,
    },
    {
      slug: "language",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      choices: supportedInviteLanguages.map((languageCode) => ({
        slug: languageCode,
        title: translations.LanguageSwitcher.supportedLanguages[languageCode],
      })),
      ...t.actions.inviteProgramHost.attributes.language,
    },
  ];

  const inviteProgramHostDefaults = {
    surveySlug: data.event.forms?.inviteForms[0]?.slug,
    language: locale,
  };

  const resentEmail =
    searchParams.resent &&
    invitations.find((invitation) => invitation.id === searchParams.resent)
      ?.email;

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"programHosts"}
    >
      <DataTable rows={programHosts} columns={programHostColumns}>
        <tfoot>
          <tr>
            <td colSpan={programHostColumns.length - 1}>
              {t.attributes.count(programHosts.length)}
            </td>
            <td className="text-end">
              <ModalButton
                className="btn btn-outline-primary btn-sm"
                label={t.actions.inviteProgramHost.title + "…"}
                title={t.actions.inviteProgramHost.title}
                messages={t.actions.inviteProgramHost.modalActions}
                action={inviteProgramHost.bind(
                  null,
                  locale,
                  eventSlug,
                  programSlug,
                )}
              >
                <p>{t.actions.inviteProgramHost.message}</p>
                <SchemaForm
                  fields={inviteProgramHostFields}
                  values={inviteProgramHostDefaults}
                  messages={translations.SchemaForm}
                />
              </ModalButton>
            </td>
          </tr>
        </tfoot>
      </DataTable>

      {invitations.length > 0 && (
        <>
          <h4 className="mt-5">{inviT.listTitle}</h4>
          <p>{inviT.listDescription}</p>
          {resentEmail && (
            <AlertNavigateOnClose
              variant="success"
              href={`/${eventSlug}/program-admin/${programSlug}/hosts`}
            >
              {inviT.actions.resend.success(resentEmail)}
            </AlertNavigateOnClose>
          )}
          <DataTable rows={invitations} columns={invitationColumns}>
            <tfoot>
              <tr>
                <td colSpan={invitationColumns.length - 1}>
                  {inviT.attributes.count(invitations.length)}
                </td>
              </tr>
            </tfoot>
          </DataTable>
        </>
      )}
    </ProgramAdminDetailView>
  );
}
