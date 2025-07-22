import Link from "next/link";
import { notFound } from "next/navigation";

import {
  markScheduleItemAsFavorite,
  unmarkAsFavorite,
} from "../../program/actions";
import FavoriteButton from "../../program/FavoriteButton";
import { FavoriteContextProvider } from "../../program/FavoriteContext";
import { graphql } from "@/__generated__";
import {
  AnnotationDataType,
  ProgramDetailAnnotationFragment,
  ProgramLinkType,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import FormattedDateTimeRange from "@/components/FormattedDateTimeRange";
import Paragraphs from "@/components/helpers/Paragraphs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { publicUrl } from "@/config";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ProgramDetailAnnotation on ProgramAnnotationType {
    annotation {
      slug
      type
      title(lang: $locale)
    }
    value(lang: $locale)
  }
`);

// TODO(Japsu) Deterministic order of dimensions & values
// See https://con2.slack.com/archives/C3ZGNGY48/p1718446605681339
const query = graphql(`
  query ProgramDetailQuery(
    $eventSlug: String!
    $programSlug: String!
    $locale: String
  ) {
    profile {
      program {
        scheduleItems(eventSlug: $eventSlug) {
          slug
        }
      }
    }

    event(slug: $eventSlug) {
      name
      slug
      timezone

      program {
        calendarExportLink

        program(slug: $programSlug) {
          title
          description
          cachedHosts

          links(lang: $locale) {
            type
            href
            title
          }

          annotations(isShownInDetail: true) {
            ...ProgramDetailAnnotation
          }

          dimensions(isShownInDetail: true, publicOnly: true) {
            dimension {
              slug
              title(lang: $locale)
            }
            value {
              slug
              title(lang: $locale)
            }
          }
          scheduleItems {
            slug
            subtitle
            location(lang: $locale)
            startTime
            endTime
          }
        }
      }
    }
  }
`);

interface Props {
  params: Promise<{
    locale: string;
    eventSlug: string;
    programSlug: string;
  }>;
}

export const revalidate = 5;

export async function generateMetadata(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const { data, errors } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const title = getPageTitle({
    translations,
    event: data.event,
    viewTitle: translations.Program.singleTitle,
    subject: data?.event?.program?.program?.title,
  });
  const description = data?.event?.program?.program?.description;
  return { title, description };
}

function getLinkEmoji(type: ProgramLinkType) {
  switch (type) {
    case ProgramLinkType.Calendar:
      return "📅";
    case ProgramLinkType.Signup:
      return "✍️";
    case ProgramLinkType.Feedback:
      return "📝";
    case ProgramLinkType.Recording:
      return "🎥";
    case ProgramLinkType.Remote:
      return "🌐";
    case ProgramLinkType.Reservation:
    case ProgramLinkType.Tickets:
      return "🎟️";
    case ProgramLinkType.Other:
    default:
      return "🔗";
  }
}

export default async function NewProgramPage(props: Props) {
  const params = await props.params;
  const { locale, eventSlug, programSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Program;
  const { data } = await getClient().query({
    query,
    variables: { eventSlug, programSlug, locale },
  });
  const { event } = data;
  if (!event?.program?.program) {
    notFound();
  }

  const program = event.program.program;
  const favoriteScheduleItemSlugs =
    data.profile?.program?.scheduleItems?.map(
      (scheduleItem) => scheduleItem.slug,
    ) ?? [];

  function formatAnnotationValue(annotation: ProgramDetailAnnotationFragment) {
    if (annotation.annotation.type === AnnotationDataType.Boolean) {
      return annotation.value
        ? translations.SchemaForm.boolean.true
        : translations.SchemaForm.boolean.false;
    }

    return annotation.value;
  }

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${eventSlug}/program`}>
        &lt; {t.actions.returnToProgramList(event.name)}
      </Link>

      <ViewHeading>{program.title}</ViewHeading>

      <div>
        {program.cachedHosts && <strong>{program.cachedHosts}</strong>}
        {program.scheduleItems.map((scheduleItem, index) => (
          <div key={index} className="fst-italic">
            {scheduleItem.subtitle && <>{scheduleItem.subtitle}: </>}
            {scheduleItem.location && <>{scheduleItem.location}, </>}
            <FormattedDateTimeRange
              locale={locale}
              scope={event}
              session={null}
              key={index}
              start={scheduleItem.startTime}
              end={scheduleItem.endTime}
              includeDuration={true}
            />
            {data.profile && (
              <FavoriteContextProvider
                slugs={favoriteScheduleItemSlugs}
                messages={t.favorites}
                markAsFavorite={markScheduleItemAsFavorite.bind(
                  null,
                  locale,
                  eventSlug,
                )}
                unmarkAsFavorite={unmarkAsFavorite.bind(
                  null,
                  locale,
                  eventSlug,
                )}
              >
                <FavoriteButton scheduleItem={scheduleItem} />
              </FavoriteContextProvider>
            )}
          </div>
        ))}
      </div>

      <div className="mb-3 mt-3">
        {program.links.map((link, index) => (
          <div key={index}>
            {link.href.startsWith(publicUrl) ? (
              <Link
                href={link.href.slice(publicUrl.length)}
                className="link-subtle"
              >
                {getLinkEmoji(link.type) + " "}
                {link.title}…
              </Link>
            ) : (
              <a
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                className="link-subtle"
              >
                {getLinkEmoji(link.type) + " "}
                {link.title}…
              </a>
            )}
          </div>
        ))}
      </div>

      <article className="mb-3">
        <Paragraphs text={program.description} />
      </article>

      <div className="mb-3 mt-3">
        {program.annotations.map((annotation) => (
          <div key={annotation.annotation.slug}>
            <strong>{annotation.annotation.title}</strong>:{" "}
            {"" + formatAnnotationValue(annotation)}
          </div>
        ))}
      </div>

      <div className="mb-3 mt-3">
        {program.dimensions.map((dimension) => (
          <Link
            key={dimension.dimension.slug}
            href={`/${eventSlug}/program?${dimension.dimension.slug}=${dimension.value.slug}`}
          >
            <span className="badge text-bg-primary me-2">
              <strong>{dimension.dimension.title}</strong>:{" "}
              {dimension.value.title}
            </span>
          </Link>
        ))}
      </div>
    </ViewContainer>
  );
}
