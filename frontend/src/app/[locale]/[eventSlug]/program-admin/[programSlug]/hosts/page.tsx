import { notFound } from "next/navigation";

import { inviteProgramHost, removeProgramHost } from "./actions";
import { graphql } from "@/__generated__";
import { ProgramAdminDetailHostFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { Column, DataTable } from "@/components/DataTable";
import ModalButton from "@/components/ModalButton";
import ProgramAdminDetailView from "@/components/program/ProgramAdminDetailView";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramAdminDetailHost on LimitedInvolvementType {
    id
    person {
      firstName
      lastName
      nick
      email
      phoneNumber
      discordHandle
    }
  }
`);

const query = graphql(`
  query ProgramAdminDetailHosts(
    $eventSlug: String!
    $programSlug: String! # $locale: String
  ) {
    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        program(slug: $programSlug) {
          slug
          title
          programHosts {
            ...ProgramAdminDetailHost
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
}

export const revalidate = 0;

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

export default async function ProgramAdminDetailPage({ params }: Props) {
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const programT = translations.Program;
  const profileT = translations.Profile;
  const t = translations.Program.ProgramHost;
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

  const columns: Column<ProgramAdminDetailHostFragment>[] = [
    {
      slug: "lastName",
      title: profileT.attributes.lastName.title,
      getCellContents: (row) => row.person.lastName,
    },
    {
      slug: "firstName",
      title: profileT.attributes.firstName.title,
      getCellContents: (row) => row.person.firstName,
    },
    {
      slug: "nick",
      title: profileT.attributes.nick.title,
      getCellContents: (row) => row.person.nick,
    },
    {
      slug: "email",
      title: profileT.attributes.email.title,
      getCellContents: (row) => row.person.email,
    },
    {
      slug: "phoneNumber",
      title: profileT.attributes.phoneNumber.title,
      getCellContents: (row) => row.person.phoneNumber,
    },
    {
      slug: "discordHandle",
      title: profileT.attributes.discordHandle.title,
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
          disabled
          action={removeProgramHost.bind(
            null,
            locale,
            eventSlug,
            programSlug,
            row.id,
          )}
        >
          {t.actions.removeProgramHost.message}
        </ModalButton>
      ),
    },
  ];

  return (
    <ProgramAdminDetailView
      event={event}
      program={program}
      translations={translations}
      active={"programHosts"}
    >
      <DataTable rows={programHosts} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length - 1}>
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
                disabled
              >
                <p>{t.actions.inviteProgramHost.message}</p>
                {/* <SchemaForm
            fields={inviteProgramHostFields}
            messages={translations.SchemaForm}
          /> */}
              </ModalButton>
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminDetailView>
  );
}
