import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime from "@/components/FormattedDateTime";
import ModalButton from "@/components/ModalButton";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
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
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Program.Message.profile;
  const session = await auth();

  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query });
  const messages = data.profile?.messages ?? [];

  const columns: Column<(typeof messages)[number]>[] = [
    {
      slug: "sentAt",
      title: t.attributes.sentAt,
      getCellContents: (message) => (
        <ModalButton
          title={message.subject || t.noSubject}
          messages={translations.Modal}
          label={
            <FormattedDateTime
              value={message.sentAt}
              locale={locale}
              scope={undefined}
              session={session}
            />
          }
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

  return (
    <ViewContainer>
      <ViewHeading>{t.title}</ViewHeading>
      <DataTable columns={columns} rows={messages} />
    </ViewContainer>
  );
}
