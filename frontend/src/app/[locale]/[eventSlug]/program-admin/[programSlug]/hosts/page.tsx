import { notFound } from "next/navigation";

import ProgramAdminDetailView from "../ProgramAdminDetailView";
import { inviteProgramHost, removeProgramHost } from "./actions";
import { graphql } from "@/__generated__";
import { ProgramAdminDetailHostFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { Column, DataTable } from "@/components/DataTable";
import ModalButton from "@/components/ModalButton";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// TODO(Japsu) Deterministic order of dimensions & values
// See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339

graphql(`
  fragment ProgramAdminDetailHost on LimitedInvolvementType {
    id
    firstName
    lastName
    nick
    email
    phoneNumber
    discordHandle
  }
`);

const query = graphql(`
  query ProgramAdminDetailHostsQuery(
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
    },
    {
      slug: "firstName",
      title: profileT.attributes.firstName.title,
    },
    {
      slug: "nick",
      title: profileT.attributes.nick.title,
    },
    {
      slug: "email",
      title: profileT.attributes.email.title,
    },
    {
      slug: "phoneNumber",
      title: profileT.attributes.phoneNumber.title,
    },
    {
      slug: "discordHandle",
      title: profileT.attributes.discordHandle.title,
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
