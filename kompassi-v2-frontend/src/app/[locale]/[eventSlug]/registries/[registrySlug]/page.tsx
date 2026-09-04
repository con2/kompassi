import { SignInRequired, SubmitButton, ModalButton } from "@con2/components";
import { notFound } from "next/navigation";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import CardTitle from "react-bootstrap/CardTitle";
import { deleteRegistry, updateRegistry } from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import InvolvementAdminView from "@/components/involvement/InvolvementAdminView";
import getPageTitle from "@/helpers/getPageTitle";
import { supportedLanguages, getTranslations } from "@/translations";

const query = graphql(`
  query AdminRegistryDetailPage(
    $eventSlug: String!
    $registrySlug: String!
    $locale: String!
  ) {
    event(slug: $eventSlug) {
      name
      slug

      involvement {
        registry(slug: $registrySlug) {
          slug
          title(lang: $locale)
          titleEn
          titleFi
          titleSv
          policyUrlEn
          policyUrlFi
          policyUrlSv
          defaultRetentionPeriodDays
          canRemove
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    registrySlug: string;
  }>;
  searchParams: Promise<Record<string, string>>;
}

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, registrySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Registry;

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, registrySlug, locale },
  });

  if (!data.event?.involvement?.registry) {
    notFound();
  }

  const title = getPageTitle({
    event: data.event,
    subject: data.event.involvement.registry.title,
    viewTitle: t.singleTitle,
    translations,
  });

  return {
    title,
  };
}

export const revalidate = 0;

export default async function AdminRegistryDetailPage(props: Props) {
  const searchParams = await props.searchParams;
  const params = await props.params;
  const { locale, eventSlug, registrySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Registry;

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

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, registrySlug, locale },
  });

  if (!data.event?.involvement?.registry) {
    notFound();
  }

  const event = data.event;
  const registry = data.event.involvement.registry;

  const fields: Field[] = [
    {
      slug: "slug",
      title: t.attributes.slug,
      type: "SingleLineText",
      readOnly: true,
    },
    ...supportedLanguages.map(
      (lang) =>
        ({
          slug: `title_${lang}`,
          title: t.attributes.title[lang],
          type: "SingleLineText",
          required: true,
        }) as Field,
    ),
    ...supportedLanguages.map(
      (lang) =>
        ({
          slug: `policy_url_${lang}`,
          title: t.attributes.policyUrl[lang],
          type: "SingleLineText",
        }) as Field,
    ),
    {
      slug: "defaultRetentionPeriodDays",
      title: t.attributes.defaultRetentionPeriodDays.title,
      helpText: t.attributes.defaultRetentionPeriodDays.helpText,
      type: "NumberField",
      minValue: 0,
    },
  ];

  // NOTE SUPPORTED_LANGUAGES
  const values = {
    ...registry,
    title_en: registry.titleEn,
    title_fi: registry.titleFi,
    title_sv: registry.titleSv,
    policy_url_en: registry.policyUrlEn,
    policy_url_fi: registry.policyUrlFi,
    policy_url_sv: registry.policyUrlSv,
  };

  return (
    <InvolvementAdminView
      translations={translations}
      event={event}
      active="registries"
      searchParams={searchParams}
      actions={
        <ModalButton
          title={t.actions.deleteRegistry.title}
          messages={t.actions.deleteRegistry.modalActions}
          action={
            registry.canRemove
              ? deleteRegistry.bind(null, locale, eventSlug, registrySlug)
              : undefined
          }
          className="btn btn-outline-danger"
        >
          {registry.canRemove
            ? t.actions.deleteRegistry.confirmation(registry.title)
            : t.actions.deleteRegistry.cannotDelete}
        </ModalButton>
      }
    >
      <Card className="mb-4">
        <CardBody>
          <CardTitle>{t.actions.editRegistry}</CardTitle>
          <form
            action={updateRegistry.bind(null, locale, eventSlug, registrySlug)}
          >
            <SchemaForm
              fields={fields}
              values={values}
              messages={translations.SchemaForm}
              headingLevel="h5"
            />
            <SubmitButton>{t.actions.saveRegistry}</SubmitButton>
          </form>
        </CardBody>
      </Card>
    </InvolvementAdminView>
  );
}
