import Link from "next/link";
import { notFound } from "next/navigation";
import { Fragment } from "react";
import { gql } from "@/__generated__";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { makeColorTranslucent } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

const query = gql(`
  query DimensionsList(
    $eventSlug: String!,
    $surveySlug: String!,
    $locale: String!,
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          dimensions {
            slug
            titleFi: title(lang: "fi")
            titleEn: title(lang: "en")
            values {
              slug
              color
              titleFi: title(lang: "fi")
              titleEn: title(lang: "en")
            }
          }
        }
      }
    }
  }
`);

interface Props {
  params: {
    locale: string;
    eventSlug: string;
    surveySlug: string;
  };
}

export async function generateMetadata({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return translations.SignInRequired.metadata;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey) {
    notFound();
  }

  const title = getPageTitle({
    translations,
    event: data.event,
    subject: data.event.forms.survey.title,
    viewTitle: t.attributes.dimensions,
  });

  return { title };
}

export default async function SurveyDimensionsPage({ params }: Props) {
  const { locale, eventSlug, surveySlug } = params;
  const translations = getTranslations(locale);

  // TODO encap
  const session = await auth();
  if (!session) {
    return <SignInRequired messages={translations.SignInRequired} />;
  }

  const t = translations.Survey;

  const { data } = await getClient().query({
    query,
    variables: { locale, eventSlug, surveySlug },
  });

  if (!data.event?.forms?.survey?.dimensions) {
    notFound();
  }

  const survey = data.event.forms.survey;
  const dimensions = data.event.forms.survey.dimensions;

  const countValues = dimensions.reduce(
    (acc, dimension) => acc + dimension.values.length,
    0,
  );

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/events/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>
      <ViewHeading>
        {t.attributes.dimensions}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>

      <table className="table table-striped table-bordered">
        <thead>
          <tr>
            <th>{t.attributes.dimension}</th>
            <th>{t.attributes.dimension} (fi)</th>
            <th>{t.attributes.dimension} (en)</th>
            <th>{t.attributes.value}</th>
            <th>{t.attributes.value} (fi)</th>
            <th>{t.attributes.value} (en)</th>
          </tr>
        </thead>
        <tbody>
          {dimensions.map((dimension, dimensionIndex) => (
            <Fragment key={dimension.slug}>
              {dimension.values.map((value, valueIndex) => {
                const backgroundColor =
                  value.color && makeColorTranslucent(value.color);
                return (
                  <tr key={`${dimension.slug}.${value.slug}`}>
                    {valueIndex === 0 && (
                      <>
                        <td rowSpan={dimension.values.length} scope="rowgroup">
                          <code>{dimension.slug}</code>
                        </td>
                        <td rowSpan={dimension.values.length} scope="rowgroup">
                          {dimension.titleFi}
                        </td>
                        <td rowSpan={dimension.values.length} scope="rowgroup">
                          {dimension.titleEn}
                        </td>
                      </>
                    )}
                    <td style={{ backgroundColor }}>
                      <code>{value.slug}</code>
                    </td>
                    <td style={{ backgroundColor }}>{value.titleFi}</td>
                    <td style={{ backgroundColor }}>{value.titleEn}</td>
                  </tr>
                );
              })}
            </Fragment>
          ))}
        </tbody>
      </table>
      <p>{t.dimensionTableFooter(dimensions.length, countValues)}</p>
    </ViewContainer>
  );
}
