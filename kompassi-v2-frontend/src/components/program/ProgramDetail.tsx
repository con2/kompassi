import { Markdown, FormattedDateTimeRange } from "@con2/components";
import Link from "next/link";

import { markScheduleItemAsFavorite, unmarkAsFavorite } from "./actions";
import FavoriteButton from "./FavoriteButton";
import { FavoriteContextProvider } from "./FavoriteContext";
import { Scope } from "./models";
import ProgramLinkAnchor from "./ProgramLinkAnchor";
import { graphql } from "@/__generated__";
import {
  AnnotationDataType,
  ProgramDetailAnnotationFragment,
  ProgramDetailFragment,
} from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

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
graphql(`
  fragment ProgramDetail on FullProgramType {
    slug
    title
    description
    cachedHosts
    isCancelled

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
      links(ownOnly: true, lang: $locale) {
        type
        href
        title
      }
    }
  }
`);

interface Props {
  locale: string;
  event: Scope;
  program: ProgramDetailFragment;
  isLoggedIn: boolean;
  favoriteScheduleItemSlugs: string[];
  /// Base URL for dimension-badge filter links: `/${eventSlug}/program` or `/${eventSlug}/program-preview`.
  listUrl: string;
  translations: Translations;
}

function formatAnnotationValue(
  annotation: ProgramDetailAnnotationFragment,
  translations: Translations,
) {
  if (annotation.annotation.type === AnnotationDataType.Boolean) {
    return annotation.value
      ? translations.SchemaForm.boolean.true
      : translations.SchemaForm.boolean.false;
  }

  return annotation.value;
}

export default function ProgramDetail({
  locale,
  event,
  program,
  isLoggedIn,
  favoriteScheduleItemSlugs,
  listUrl,
  translations,
}: Props) {
  const t = translations.Program;

  return (
    <>
      {program.isCancelled && (
        <p className="text-danger fw-bold">
          ❌ {t.attributes.cancelled.message}
        </p>
      )}

      <div>
        {program.cachedHosts && <strong>{program.cachedHosts}</strong>}
        {program.scheduleItems.map((scheduleItem, index) => (
          <div key={index} className="fst-italic">
            {scheduleItem.subtitle && <>{scheduleItem.subtitle}: </>}
            {scheduleItem.location && <>{scheduleItem.location}, </>}
            <FormattedDateTimeRange
              locale={locale}
              timezone={event.timezone}
              key={index}
              start={scheduleItem.startTime}
              end={scheduleItem.endTime}
              includeDuration={true}
            />
            {isLoggedIn && (
              <FavoriteContextProvider
                slugs={favoriteScheduleItemSlugs}
                messages={t.favorites}
                markAsFavorite={markScheduleItemAsFavorite.bind(
                  null,
                  locale,
                  event.slug,
                )}
                unmarkAsFavorite={unmarkAsFavorite.bind(
                  null,
                  locale,
                  event.slug,
                )}
              >
                <FavoriteButton scheduleItem={scheduleItem} />
              </FavoriteContextProvider>
            )}
            {scheduleItem.links.map((link, linkIndex) => (
              <span key={linkIndex} className="ms-2 fst-normal">
                <ProgramLinkAnchor link={link} />
              </span>
            ))}
          </div>
        ))}
      </div>

      <div className="mb-3 mt-3">
        {program.links.map((link, index) => (
          <div key={index}>
            <ProgramLinkAnchor link={link} />
          </div>
        ))}
      </div>

      <article className="mb-3">
        <Markdown input={program.description} />
      </article>

      <div className="mb-3 mt-3">
        {program.annotations.map((annotation) => (
          <div key={annotation.annotation.slug}>
            <strong>{annotation.annotation.title}</strong>:{" "}
            {"" + formatAnnotationValue(annotation, translations)}
          </div>
        ))}
      </div>

      <div className="mb-3 mt-3">
        {program.dimensions.map((dimension) => (
          <Link
            key={`${dimension.dimension.slug}-${dimension.value.slug}`}
            href={`${listUrl}?${dimension.dimension.slug}=${dimension.value.slug}`}
          >
            <span className="badge text-bg-primary me-2">
              <strong>{dimension.dimension.title}</strong>:{" "}
              {dimension.value.title}
            </span>
          </Link>
        ))}
      </div>
    </>
  );
}
