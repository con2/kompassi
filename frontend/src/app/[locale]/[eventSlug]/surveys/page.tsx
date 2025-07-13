import { Temporal } from "@js-temporal/polyfill";
import Link from "next/link";
import { notFound } from "next/navigation";

import ModalButton from "../../../../components/ModalButton";
import { createSurvey } from "./actions";
import getAnonymityDropdown from "./getAnonymityDropdown";
import { graphql } from "@/__generated__";
import { SurveyFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import CopyButton from "@/components/CopyButton";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/errors/SignInRequired";
import { formatDateTime } from "@/components/FormattedDateTime";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import { publicUrl } from "@/config";
import { getTranslations } from "@/translations";

graphql(`
  fragment Survey on FullSurveyType {
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
  query Surveys($eventSlug: String!, $locale: String) {
    profile {
      forms {
        surveys(relation: ACCESSIBLE) {
          event {
            slug
            name
          }
          slug
          title(lang: $locale)
        }
      }
    }

    event(slug: $eventSlug) {
      name

      forms {
        surveys(includeInactive: true, app: FORMS) {
          ...Survey
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
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { eventSlug, locale },
  });

  if (!data.event?.forms?.surveys) {
    notFound();
  }

  return {
    title: `${data.event.name}: ${t.listTitle} – Kompassi`,
  };
}

export const revalidate = 0;

export default async function SurveysPage({ params }: Props) {
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

  const t = translations.Survey;
  const columns: Column<SurveyFragment>[] = [
    {
      slug: "slug",
      getCellContents: (survey) => <em>{survey.slug}</em>,
      ...t.attributes.slug,
    },
    {
      slug: "title",
      title: t.attributes.title,
    },
    {
      slug: "isActive",
      title: t.attributes.isActive.title,
      getCellContents: (survey) => {
        let activityEmoji = survey.isActive ? "✅" : "❌";
        let message = "";

        // TODO(#436) proper handling of event & session time zones
        // Change untilTime(t: String): String to UntilTime(props: { children: ReactNode }): ReactNode
        // and init as <….UntilTime><FormattedDateTime … /></UntilTime>?
        if (survey.isActive) {
          if (survey.activeUntil) {
            message = t.attributes.isActive.untilTime(
              formatDateTime(survey.activeUntil, locale),
            );
          } else {
            message = t.attributes.isActive.untilFurtherNotice;
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
            message = t.attributes.isActive.openingAt(
              formatDateTime(survey.activeFrom, locale),
            );
          } else {
            message = t.attributes.isActive.closed;
          }
        }

        return `${activityEmoji} ${message}`;
      },
    },
    {
      slug: "countResponses",
      title: t.attributes.countResponses,
    },
    {
      slug: "languages",
      title: t.attributes.languages,
      getCellContents: (survey) =>
        survey.languages
          .map((language) => language.language.toLowerCase())
          .join(", "),
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCellContents: (survey) => {
        const fillInUrl = `/${eventSlug}/${survey.slug}`;
        const adminUrl = `/${eventSlug}/surveys/${survey.slug}`;
        const absoluteUrl = `${publicUrl}${fillInUrl}`;
        return (
          <>
            <Link href={fillInUrl} className="btn btn-sm btn-outline-primary">
              {t.actions.fillIn.title}…
            </Link>{" "}
            <CopyButton
              className="btn btn-sm btn-outline-primary"
              data={absoluteUrl}
              messages={t.actions.share}
            />{" "}
            <Link
              href={`${adminUrl}/edit`}
              className="btn btn-sm btn-outline-primary"
            >
              {t.actions.editSurvey}…
            </Link>{" "}
            <Link
              href={`${adminUrl}/responses`}
              className="btn btn-sm btn-outline-primary"
            >
              {t.actions.viewResponses}…
            </Link>{" "}
          </>
        );
      },
    },
  ];

  const surveys = data.event.forms.surveys;

  const createSurveyFields: Field[] = [
    {
      slug: "slug",
      type: "SingleLineText",
      required: true,
      ...t.attributes.slug,
    },
    getAnonymityDropdown(t),
    {
      slug: "copyFrom",
      type: "SingleSelect",
      presentation: "dropdown",
      required: false,
      choices: data.profile!.forms.surveys.map((survey) => ({
        slug: `${survey.event.slug}/${survey.slug}`,
        title: `${survey.event.name}: ${survey.title}`,
      })),
      ...t.attributes.cloneFrom,
    },
  ];

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.listTitle}
          <ViewHeading.Sub>{t.forEvent(data.event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            className="btn btn-outline-primary"
            label={t.actions.createSurvey + "…"}
            title={t.createSurveyModal.title}
            messages={t.createSurveyModal.actions}
            action={createSurvey.bind(null, locale, eventSlug)}
          >
            <SchemaForm
              fields={createSurveyFields}
              messages={translations.SchemaForm}
            />
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <DataTable rows={surveys} columns={columns} />
      <p>{t.tableFooter(surveys.length)}</p>
    </ViewContainer>
  );
}
