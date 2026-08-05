import {
  Column,
  DataTable,
  ViewContainer,
  ViewHeading,
  SignInRequired,
  ModalButton,
  FormattedDateTime,
} from "@con2/components";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { DimensionFilters } from "@con2/components";
import { kompassiBaseUrl } from "@/config";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileMessageRow on LimitedMessageType {
    id
    subject
    sentAt
    bodyHtml
    event {
      slug
      name
    }
  }
`);

const query = graphql(`
  query ProfileMessages {
    profile {
      messages {
        ...ProfileMessageRow
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message.profile;

  return {
    title: `${t.title} – Kompassi`,
  };
}

export default async function ProfileMessagesPage(props: Props) {
  const params = await props.params;
  const searchParams = await props.searchParams;
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message.profile;
  const session = await auth();

  if (!session) {
    return (
      <SignInRequired
        messages={translations.SignInRequired}
        providerId="kompassi"
        locale={locale}
      />
    );
  }

  const { data } = await getClient().query({ query });
  const allMessages = data.profile?.messages ?? [];

  // "event" isn't a real dimension of a message, but reusing DimensionFilters gives
  // us a familiar filter dropdown (and URL search param) for free.
  const eventChoicesBySlug = new Map(
    allMessages.map((message) => [
      message.event.slug,
      {
        slug: message.event.slug,
        title: message.event.name,
      },
    ]),
  );
  const eventFilter = {
    slug: "event",
    title: t.attributes.event,
    isMultiValue: false,
    isListFilter: true,
    isKeyDimension: false,
    values: [...eventChoicesBySlug.values()].sort((a, b) =>
      a.title.localeCompare(b.title),
    ),
  };

  const selectedEventSlug = searchParams.event;
  const messages = selectedEventSlug
    ? allMessages.filter((message) => message.event.slug === selectedEventSlug)
    : allMessages;

  const columns: Column<(typeof messages)[number]>[] = [
    {
      slug: "sentAt",
      title: t.attributes.sentAt,
      getCellContents: (message) => (
        <ModalButton
          title={message.subject || t.noSubject}
          messages={translations.Modal}
          label={<FormattedDateTime value={message.sentAt} locale={locale} />}
        >
          <div dangerouslySetInnerHTML={{ __html: message.bodyHtml }} />
        </ModalButton>
      ),
      className: "col-2 align-middle",
    },
    {
      slug: "event",
      title: t.attributes.event,
      getCellContents: (message) => message.event.name,
      className: "col-3 align-middle",
    },
    {
      slug: "subject",
      title: t.attributes.subject,
      className: "col-7 align-middle",
    },
  ];

  const VolunteerMessagesLink = ({
    children,
  }: {
    children: React.ReactNode;
  }) => (
    <a
      href={`${kompassiBaseUrl}/profile/signups`}
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  );

  return (
    <ViewContainer>
      <ViewHeading>{t.title}</ViewHeading>
      {t.description(VolunteerMessagesLink)}
      <DimensionFilters dimensions={[eventFilter]} locale={locale} />
      <DataTable columns={columns} rows={messages}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>{t.tableFooter(messages.length)}</td>
          </tr>
        </tfoot>
      </DataTable>
    </ViewContainer>
  );
}
