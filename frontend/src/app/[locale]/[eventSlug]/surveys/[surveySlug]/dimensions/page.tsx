import { notFound } from "next/navigation";
import { ReactNode } from "react";

import SurveyEditorView from "../edit/SurveyEditorView";
import {
  createDimension,
  createDimensionValue,
  deleteDimension,
  deleteDimensionValue,
  updateDimension,
  updateDimensionValue,
} from "./actions";
import DimensionForm from "./DimensionForm";
import ValueForm from "./ValueForm";
import { graphql } from "@/__generated__";
import {
  DimensionRowGroupFragment,
  ValueFieldsFragment,
} from "@/__generated__/graphql";
import { getClient } from "@/apolloClient";
import { auth } from "@/auth";
import { makeColorTranslucent } from "@/components/dimensions/helpers";
import ModalButton from "@/components/ModalButton";
import SignInRequired from "@/components/SignInRequired";
import getPageTitle from "@/helpers/getPageTitle";
import { getTranslations } from "@/translations";

graphql(`
  fragment ValueFields on SurveyDimensionValueType {
    slug
    color
    isInitial
    canRemove
    title(lang: $locale)
    titleFi: title(lang: "fi")
    titleEn: title(lang: "en")
    titleSv: title(lang: "sv")
  }
`);

graphql(`
  fragment DimensionRowGroup on SurveyDimensionType {
    slug
    canRemove
    title(lang: $locale)
    isKeyDimension
    isMultiValue
    isShownToSubject
    titleFi: title(lang: "fi")
    titleEn: title(lang: "en")
    titleSv: title(lang: "sv")
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
          slug
          title(lang: $locale)
          canRemove
          languages {
            language
          }
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

  function DeleteButton({
    subject,
    action,
    children,
  }: {
    subject: {
      title?: string | null;
      slug: string;
      canRemove: boolean;
    };
    action: (formData: FormData) => void;
    children?: ReactNode;
  }) {
    return (
      <ModalButton
        className="btn btn-link btn-sm p-0 link-xsubtle me-1"
        title={t.actions.deleteDimension.title}
        label={subject.canRemove ? "❌" : "🔒"}
        messages={t.actions.deleteDimension.modalActions}
        action={action}
        submitButtonVariant="danger"
        disabled={!subject.canRemove}
      >
        {children}
      </ModalButton>
    );
  }

  function DimensionCells({
    dimension,
  }: {
    dimension: DimensionRowGroupFragment;
  }) {
    const rowspan = dimension.values.length + 1;
    return (
      <>
        <td rowSpan={rowspan} scope="rowgroup">
          <DeleteButton
            subject={dimension}
            action={deleteDimension.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
            )}
          >
            <p>
              {t.actions.deleteDimension.confirmation(
                dimension.title || dimension.slug,
              )}
            </p>
          </DeleteButton>

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
            <DimensionForm
              messages={{
                SchemaForm: translations.SchemaForm,
                Survey: translations.Survey,
              }}
              dimension={dimension}
            />
          </ModalButton>
        </td>
        <td rowSpan={rowspan} scope="rowgroup">
          {dimension.title}
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
          messages={t.editValueModal.actions}
          action={createDimensionValue.bind(
            null,
            eventSlug,
            surveySlug,
            dimension.slug,
          )}
        >
          {" "}
          <ValueForm
            messages={{
              SchemaForm: translations.SchemaForm,
              Survey: translations.Survey,
            }}
          />
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
          <DeleteButton
            subject={value}
            action={deleteDimensionValue.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
              value.slug,
            )}
          >
            <p>
              {t.actions.deleteDimensionValue.confirmation(
                dimension.title || dimension.slug,
                value.title || value.slug,
              )}
            </p>
          </DeleteButton>
          <ModalButton
            className="btn btn-link btn-sm p-0 link-xsubtle"
            title={t.actions.editDimensionValue}
            label={
              <>
                <span className="me-2">✏️</span>
                <code>{value.slug}</code>
              </>
            }
            messages={t.editValueModal.actions}
            action={updateDimensionValue.bind(
              null,
              eventSlug,
              surveySlug,
              dimension.slug,
              value.slug,
            )}
          >
            <ValueForm
              messages={{
                SchemaForm: translations.SchemaForm,
                Survey: translations.Survey,
              }}
              value={value}
            />
          </ModalButton>
        </td>
        <td style={{ backgroundColor }}>{value.title}</td>
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
    <SurveyEditorView params={params} survey={survey} activeTab="dimensions">
      <table className="table table-bordered">
        <thead>
          <tr>
            <th colSpan={2}>{t.attributes.dimensions}</th>
            <th colSpan={2}>{t.attributes.values}</th>
          </tr>
          <tr style={{ borderWidth: "1px 0 3px 0" }}>
            <th scope="col">{t.attributes.slug.title}</th>
            <th scope="col">{t.attributes.title}</th>
            <th scope="col">{t.attributes.slug.title}</th>
            <th scope="col">{t.attributes.title}</th>
          </tr>
        </thead>
        <tbody>
          {dimensions.map((dimension) => (
            <DimensionRowGroup key={dimension.slug} dimension={dimension} />
          ))}
          <tr>
            <td colSpan={4}>
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
                <DimensionForm
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
      <div className="mb-1">
        {t.dimensionTableFooter(dimensions.length, countValues)}
      </div>
    </SurveyEditorView>
  );
}
