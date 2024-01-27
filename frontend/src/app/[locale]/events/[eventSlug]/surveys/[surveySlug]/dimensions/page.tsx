import Link from "next/link";
import { notFound } from "next/navigation";
import {
  createDimension,
  createDimensionValue,
  deleteDimension,
  deleteDimensionValue,
  updateDimension,
  updateDimensionValue,
} from "./actions";
import EditDimensionForm from "./EditDimensionForm";
import ModalButton from "./ModalButton";
import { graphql } from "@/__generated__";
import {
  DimensionRowGroupFragment,
  ValueFieldsFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { makeColorTranslucent } from "@/components/dimensions/helpers";
import SignInRequired from "@/components/SignInRequired";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ValueFields on SurveyDimensionValueType {
    slug
    color
    titleFi: title(lang: "fi")
    titleEn: title(lang: "en")
  }
`);

graphql(`
  fragment DimensionRowGroup on SurveyDimensionType {
    slug
    titleFi: title(lang: "fi")
    titleEn: title(lang: "en")
    values {
      ...ValueFields
    }
  }
`);

const query = graphql(`
  query DimensionsList(
    $eventSlug: String!
    $surveySlug: String!
    $locale: String!
  ) {
    event(slug: $eventSlug) {
      name
      forms {
        survey(slug: $surveySlug) {
          title(lang: $locale)
          dimensions {
            ...DimensionRowGroup
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

  const countColumns = 6;

  function DimensionCells({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    const rowspan = dimension.values.length + 1;
    return (
      <>
        <td rowSpan={rowspan} scope="rowgroup">
          <form
            className="d-inline me-2"
            action={deleteDimension.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
            )}
          >
            <button
              type="submit"
              className="btn btn-link btn-sm p-0 link-xsubtle"
              title={t.actions.deleteDimension}
            >
              ❌
            </button>
          </form>
          <ModalButton
            className="btn btn-link btn-sm p-0 link-xsubtle me-1"
            title={t.actions.editDimension}
            label={
              <>
                <span className="me-2">✏️</span>
                <code>{dimension.slug}</code>
              </>
            }
            messages={t.editDimensionModal.actions}
            action={updateDimension.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
            )}
          >
            <p>TODO</p>
          </ModalButton>
        </td>
        <td rowSpan={rowspan} scope="rowgroup">
          {dimension.titleFi}
        </td>
        <td rowSpan={rowspan} scope="rowgroup">
          {dimension.titleEn}
        </td>
      </>
    );
  }

  function AddValueCell({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    return (
      <td colSpan={3}>
        <ModalButton
          className="btn btn-link btn-sm p-0 link-xsubtle"
          title={t.actions.addDimensionValue}
          label={
            <>
              <span className="me-2">➕</span>
              {t.actions.addDimensionValue}
            </>
          }
          messages={t.editDimensionModal.actions}
          action={createDimensionValue.bind(
            null,
            eventSlug,
            surveySlug,
            dimension.slug,
          )}
        >
          <p>TODO</p>
        </ModalButton>
      </td>
    );
  }

  function ValueCells({
    value,
    dimension,
  }: {
    value: ValueFieldsFragment;
    dimension: DimensionRowGroupFragment;
  }) {
    const backgroundColor = value.color && makeColorTranslucent(value.color);

    return (
      <>
        <td style={{ backgroundColor }}>
          <form
            className="d-inline me-2"
            action={deleteDimensionValue.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
              value.slug,
            )}
          >
            <button
              type="submit"
              className="btn btn-link btn-sm p-0 link-xsubtle"
              title={t.actions.deleteDimensionValue}
            >
              ❌
            </button>
          </form>
          <ModalButton
            className="btn btn-link btn-sm p-0 link-xsubtle"
            title={t.actions.editDimensionValue}
            label={
              <>
                <span className="me-2">✏️</span>
                <code>{value.slug}</code>
              </>
            }
            messages={t.editDimensionModal.actions}
            action={updateDimensionValue.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
              value.slug,
            )}
          >
            <p>TODO</p>
          </ModalButton>
        </td>
        <td style={{ backgroundColor }}>{value.titleFi}</td>
        <td style={{ backgroundColor }}>{value.titleEn}</td>
      </>
    );
  }

  function DimensionRowGroup({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    if (dimension.values.length === 0) {
      return (
        <tr style={{ borderWidth: "3px 0 3px 0" }}>
          <DimensionCells dimension={dimension} />
          <AddValueCell dimension={dimension} />
        </tr>
      );
    }

    return (
      <>
        {dimension.values.map((value, valueIndex) => {
          return (
            <tr key={`${dimension.slug}.${value.slug}`}>
              {valueIndex === 0 && <DimensionCells dimension={dimension} />}
              <ValueCells dimension={dimension} value={value} />
            </tr>
          );
        })}
        <tr>
          <AddValueCell dimension={dimension} />
        </tr>
      </>
    );
  }

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/events/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>
      <ViewHeading>
        {t.attributes.dimensions}
        <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
      </ViewHeading>

      <table className="table table-bordered">
        <thead>
          <tr style={{ borderWidth: "1px 0 3px 0" }}>
            <th scope="col">{t.attributes.dimension}</th>
            <th scope="col">{t.attributes.dimension} (fi)</th>
            <th scope="col">{t.attributes.dimension} (en)</th>
            <th scope="col">{t.attributes.value}</th>
            <th scope="col">{t.attributes.value} (fi)</th>
            <th scope="col">{t.attributes.value} (en)</th>
          </tr>
        </thead>
        <tbody>
          {dimensions.map((dimension) => (
            <DimensionRowGroup key={dimension.slug} dimension={dimension} />
          ))}
          <tr>
            <td colSpan={countColumns}>
              <ModalButton
                className="btn btn-link btn-sm p-0 link-xsubtle"
                title={t.actions.addDimension}
                label={
                  <>
                    <span className="me-2">➕</span>
                    {t.actions.addDimension}
                  </>
                }
                messages={t.editDimensionModal.actions}
                action={createDimension.bind(null, eventSlug, surveySlug)}
              >
                <EditDimensionForm
                  headingLevel="h5"
                  messages={{
                    SchemaForm: translations.SchemaForm,
                    Survey: translations.Survey,
                  }}
                />
              </ModalButton>
            </td>
          </tr>
        </tbody>
      </table>
      <p>{t.dimensionTableFooter(dimensions.length, countValues)}</p>
    </ViewContainer>
  );
}
