import { Temporal } from "@js-temporal/polyfill";
import Link from "next/link";
import { notFound } from "next/navigation";

import ModalButton from "../../../../components/ModalButton";
import { createProgramForm } from "./actions";
import { graphql } from "@/__generated__";
import { OfferFormFragment, SurveyFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import CopyButton from "@/components/CopyButton";
import { Column, DataTable } from "@/components/DataTable";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ProgramAdminTabs from "@/components/program/ProgramAdminTabs";
import ProgramAdminView from "@/components/program/ProgramAdminView";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import { publicUrl } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
graphql(`
  fragment OfferForm on FullSurveyType {
    slug
    title(lang: $locale)
    isActive
    activeFrom
    activeUntil
    countResponses

    languages {
      language
    }
  }
`);

const query = graphql(`
  query ProgramFormsPage($eventSlug: String!, $locale: String) {
    event(slug: $eventSlug) {
      slug
      name

      forms {
        surveys(includeInactive: true, app: PROGRAM_V2) {
          ...OfferForm
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
  };
  searchParams: Record<string, string>;
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Program.ProgramForm;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.forms?.surveys) {
    notFound();
  }

  const event = data.event;

  const title = getPageTitle({
    event,
    translations,
    viewTitle: t.listTitle,
  });

  return { title };
}

export const revalidate = 0;

export default async function ProgramFormsPage({
  params,
  searchParams,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const session = await auth();

  // TODO encap
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.forms?.surveys) {
    notFound();
  }

  const surveyT = translations.Survey;
  const t = translations.Program.ProgramForm;

  const columns: Column<OfferFormFragment>[] = [
    {
      slug: "slug",
      getCellContents: (survey) => <em>{survey.slug}</em>,
      ...surveyT.attributes.slug,
    },
    {
      slug: "title",
      title: surveyT.attributes.title,
    },
    {
      slug: "isActive",
      title: surveyT.attributes.isActive.title,
      getCellContents: (survey) => {
        let activityEmoji = survey.isActive ? "✅" : "❌";
        let message = "";

        // TODO(#436) proper handling of event & session time zones
        // Change untilTime(t: String): String to UntilTime(props: { children: ReactNode }): ReactNode
        // and init as <….UntilTime><FormattedDateTime … /></UntilTime>?
        if (survey.isActive) {
          if (survey.activeUntil) {
            message = surveyT.attributes.isActive.untilTime(
              formatDateTime(survey.activeUntil, locale),
            );
          } else {
            message = surveyT.attributes.isActive.untilFurtherNotice;
          }
        } else {
          if (
            survey.activeFrom &&
            Temporal.Instant.compare(
              Temporal.Instant.from(survey.activeFrom),
              Temporal.Now.instant(),
            ) > 0
          ) {
            activityEmoji = "⏳";
            message = surveyT.attributes.isActive.openingAt(
              formatDateTime(survey.activeFrom, locale),
            );
          } else {
            message = surveyT.attributes.isActive.closed;
          }
        }

        return `${activityEmoji} ${message}`;
      },
    },
    {
      slug: "countResponses",
      title: surveyT.attributes.countResponses,
    },
    {
      slug: "languages",
      title: surveyT.attributes.languages,
      getCellContents: (survey) =>
        survey.languages
          .map((language) => language.language.toLowerCase())
          .join(", "),
    },
    {
      slug: "actions",
      title: surveyT.attributes.actions,
      getCellContents: (offerForm) => {
        const fillInUrl = `/${eventSlug}/${offerForm.slug}`;
        const adminUrl = `/${eventSlug}/program-forms/${offerForm.slug}`;
        const absoluteUrl = `${publicUrl}${fillInUrl}`;
        return (
          <>
            {offerForm.isActive ? (
              <Link href={fillInUrl} className="btn btn-sm btn-outline-primary">
                {surveyT.actions.fillIn.title}…
              </Link>
            ) : (
              <button
                disabled
                className="btn btn-sm btn-outline-primary"
                title={surveyT.actions.fillIn.disabledTooltip}
              >
                {surveyT.actions.fillIn.title}…
              </button>
            )}{" "}
            <CopyButton
              className="btn btn-sm btn-outline-primary"
              data={absoluteUrl}
              messages={surveyT.actions.share}
            />{" "}
            <Link
              href={`${adminUrl}/edit`}
              className="btn btn-sm btn-outline-primary"
            >
              {surveyT.actions.editSurvey}…
            </Link>{" "}
            <Link
              href={`/${eventSlug}/program-offers/?form=${offerForm.slug}`}
              className="btn btn-sm btn-outline-primary"
            >
              {t.actions.viewOffers}…
            </Link>{" "}
          </>
        );
      },
    },
  ];

  const ProgramForms = data.event.forms.surveys;

  const createOfferFormFields: Field[] = [
    {
      slug: "slug",
      type: "SingleLineText",
      required: true,
      ...t.attributes.slug,
    },
  ];

  return (
    <ProgramAdminView
      translations={translations}
      event={data.event}
      active="programForms"
      queryString=""
      actions={
        <ModalButton
          className="btn btn-outline-primary"
          label={t.actions.createOfferForm.title + "…"}
          title={t.actions.createOfferForm.title}
          messages={t.actions.createOfferForm.modalActions}
          action={createProgramForm.bind(null, eventSlug)}
        >
          <SchemaForm
            fields={createOfferFormFields}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      }
    >
      <DataTable rows={ProgramForms} columns={columns}>
        <tfoot>
          <tr>
            <td colSpan={columns.length}>
              {t.tableFooter(ProgramForms.length)}
            </td>
          </tr>
        </tfoot>
      </DataTable>
    </ProgramAdminView>
  );
}
