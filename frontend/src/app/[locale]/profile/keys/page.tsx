import ModalButton from "../../../../components/ModalButton";
import { generateKeyPair, revokeKeyPair } from "./actions";
import { graphql } from "@/__generated__";
import { ProfileEncryptionKeysFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import FormattedDateTime, {
  formatDateTime,
} from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProfileEncryptionKeys on KeyPairType {
    id
    createdAt
  }
`);

const query = graphql(`
  query ProfileEncryptionKeys {
    profile {
      keypairs {
        ...ProfileEncryptionKeys
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const t = translations.Profile.keysView;

  return {
    title: getPageTitle({ viewTitle: t.title, translations }),
  };
}

export const revalidate = 0;

export default async function OwnResponsesPage({ params }: Props) {
  const { locale } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({ query });

  const t = translations.Profile.keysView;
  const columns: Column<ProfileEncryptionKeysFragment>[] = [
    {
      slug: "id",
      title: t.attributes.id.title,
    },
    {
      slug: "createdAt",
      title: t.attributes.createdAt.title,
      getCellContents: (row) => (
        <FormattedDateTime
          value={row.createdAt}
          locale={locale}
          scope={undefined}
          session={session}
        />
      ),
    },
    {
      slug: "actions",
      title: t.attributes.actions.title,
      getCellContents: (keyPair) => (
        <>
          <ModalButton
            className="btn btn-outline-danger btn-sm"
            label={t.actions.revoke.title + "…"}
            title={t.actions.revoke.title}
            messages={t.actions.revoke.modalActions}
            action={revokeKeyPair.bind(null, locale, keyPair.id)}
            submitButtonVariant="danger"
          >
            {t.actions.revoke.confirmation(
              formatDateTime(keyPair.createdAt, locale),
            )}
          </ModalButton>
        </>
      ),
    },
  ];

  const keypairs = data.profile?.keypairs ?? [];
  const generateKeyFields: Field[] = [
    {
      slug: "password",
      type: "SingleLineText",
      htmlType: "password",
      required: true,
      ...t.attributes.password,
    },
  ];

  return (
    <ViewContainer>
      <ViewHeading>{t.title}</ViewHeading>
      <p>{t.description}</p>
      <p className="alert alert-danger">{t.resetPasswordWarning}</p>
      {keypairs.length === 0 ? (
        <ModalButton
          className="btn btn-outline-primary"
          label={t.actions.generate.title + "…"}
          title={t.actions.generate.title}
          messages={t.actions.generate.modalActions}
          action={generateKeyPair.bind(null, locale)}
        >
          <SchemaForm
            fields={generateKeyFields}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      ) : (
        <DataTable rows={keypairs} columns={columns} />
      )}
    </ViewContainer>
  );
}
