import {
  DataTable,
  FormattedDateTime,
  ModalButton,
  SignInRequired,
} from "@con2/components";
import { notFound } from "next/navigation";

import SurveyEditorView from "../edit/SurveyEditorView";
import {
  grantSurveyAccess,
  revokeSurveyAccess,
  searchGrantablePeople,
} from "./actions";
import { graphql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import PersonAutocomplete from "@/components/involvement/PersonAutocomplete";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment SurveyAccessPage on FullSurveyType {
    slug
    title(lang: $locale)
    canRemove
    canGrantAccess
    purpose

    languages {
      language
    }

    accessGrants {
      person {
        id
        fullName
        email
      }
      validUntil
      createdAt
    }
  }
`);

const query = graphql(`
  query SurveyAccessPageQuery(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String
  ) {
    event(slug: $eventSlug) {
      name

      forms {
        survey(slug: $surveySlug, app: FORMS) {
          ...SurveyAccessPage
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    surveySlug: string;
  }>;
}

export const revalidate = 0;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey?.canGrantAccess) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.accessPage.title,
  });

  return { title };
}

export default async function SurveyAccessPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;
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
    variables: { eventSlug, surveySlug, locale },
  });

  if (!data.event?.forms?.survey?.canGrantAccess) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const grants = survey.accessGrants;

  return (
    <SurveyEditorView params={params} survey={survey} activeTab="access">
      <p className="form-text">{t.accessPage.description}</p>

      {grants.length === 0 ? (
        <p>{t.accessPage.noGrants}</p>
      ) : (
        <DataTable
          rows={grants}
          columns={[
            {
              slug: "person",
              title: t.accessPage.attributes.person,
              getCellContents: (row) => row.person.fullName,
            },
            {
              slug: "email",
              title: t.accessPage.attributes.email,
              getCellContents: (row) => row.person.email,
            },
            {
              slug: "validUntil",
              title: t.accessPage.attributes.validUntil,
              getCellContents: (row) => (
                <FormattedDateTime value={row.validUntil} locale={locale} />
              ),
            },
            {
              slug: "createdAt",
              title: t.accessPage.attributes.grantedAt,
              getCellContents: (row) => (
                <FormattedDateTime value={row.createdAt} locale={locale} />
              ),
            },
            {
              slug: "actions",
              title: t.attributes.actions,
              getCellContents: (row) => (
                <ModalButton
                  title={t.accessPage.actions.revoke.title}
                  messages={t.accessPage.actions.revoke.modalActions}
                  submitButtonVariant="danger"
                  className="btn btn-outline-danger btn-sm"
                  action={revokeSurveyAccess.bind(
                    null,
                    locale,
                    eventSlug,
                    surveySlug,
                    parseInt(row.person.id, 10),
                  )}
                >
                  {t.accessPage.actions.revoke.confirmation(
                    row.person.fullName,
                  )}
                </ModalButton>
              ),
            },
          ]}
          getTotalMessage={t.accessPage.tableFooter}
        />
      )}

      <form
        className="mt-4"
        action={grantSurveyAccess.bind(null, locale, eventSlug, surveySlug)}
      >
        <h5>{t.accessPage.grantForm.title}</h5>
        <PersonAutocomplete
          search={searchGrantablePeople.bind(null, eventSlug, surveySlug)}
          messages={{
            placeholder: t.accessPage.grantForm.personPlaceholder,
            searching: t.accessPage.grantForm.searching,
            noResults: t.accessPage.grantForm.noResults,
            clear: t.accessPage.grantForm.clear,
          }}
          submitLabel={t.accessPage.grantForm.submit}
        />
      </form>
    </SurveyEditorView>
  );
}
