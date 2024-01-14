import Link from "next/link";
import { notFound } from "next/navigation";

import { gql } from "@/__generated__";
import { SurveyFragment } from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import CopyButton from "@/components/CopyButton";
import { Column, DataTable } from "@/components/DataTable";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { publicUrl } from "@/config";
import { getTranslations } from "@/translations";

// this fragment is just to give a name to the type so that we can import it from generated
gql(`
  fragment Survey on SurveyType {
    slug
    title(lang: $locale)
    isActive
    activeFrom
    activeUntil

    languages {
      language
    }
  }
`);

const query = gql(`
  query Surveys($eventSlug:String!, $locale:String) {
    event(slug: $eventSlug) {
      name

      forms {
        surveys {
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
      title: t.attributes.slug,
      getCell: (survey) => <em>{survey.slug}</em>,
    },
    {
      slug: "title",
      title: t.attributes.title,
    },
    {
      slug: "isActive",
      title: t.attributes.isActive.title,
      getCell: (survey) => {
        let activityEmoji = survey.isActive ? "✅" : "❌";
        let message = "";

        if (survey.isActive) {
          if (survey.activeUntil) {
            message = t.attributes.isActive.untilTime(
              new Date(survey.activeUntil),
            );
          } else {
            message = t.attributes.isActive.untilFurtherNotice;
          }
        } else {
          if (survey.activeFrom) {
            activityEmoji = "⏳";
            message = t.attributes.isActive.openingAt(
              new Date(survey.activeFrom),
            );
          } else {
            message = t.attributes.isActive.closed;
          }
        }

        return `${activityEmoji} ${message}`;
      },
    },
    {
      slug: "languages",
      title: t.attributes.languages,
      getCell: (survey) =>
        survey.languages
          .map((language) => language.language.toLowerCase())
          .join(", "),
    },
    {
      slug: "actions",
      title: t.attributes.actions,
      getCell: (survey) => {
        const url = `/events/${eventSlug}/surveys/${survey.slug}`;
        const absoluteUrl = `${publicUrl}${url}`;
        return (
          <>
            {survey.isActive ? (
              <Link href={url} className="btn btn-sm btn-outline-primary">
                {t.actions.fillIn.title}…
              </Link>
            ) : (
              <button
                disabled
                className="btn btn-sm btn-outline-primary"
                title={t.actions.fillIn.disabledTooltip}
              >
                {t.actions.fillIn.title}…
              </button>
            )}{" "}
            <CopyButton
              className="btn btn-sm btn-outline-primary"
              data={absoluteUrl}
              messages={t.actions.share}
            />{" "}
            <Link
              href={`${url}/responses`}
              className="btn btn-sm btn-outline-primary"
            >
              {t.actions.viewResponses}…
            </Link>
          </>
        );
      },
    },
  ];

  const surveys = data.event.forms.surveys;

  return (
    <ViewContainer>
      <ViewHeading>
        {t.listTitle}
        <ViewHeading.Sub>{t.forEvent(data.event.name)}</ViewHeading.Sub>
      </ViewHeading>
      <DataTable rows={surveys} columns={columns} />
      <p>{t.tableFooter(surveys.length)}</p>
    </ViewContainer>
  );
}
