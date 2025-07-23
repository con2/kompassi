import AutoSubmitForm from "../AutoSubmitForm";
import { Choice, MultiSelect, SingleSelect } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import SubmitButton from "../forms/SubmitButton";
import { graphql } from "@/__generated__";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";
import type { Translations } from "@/translations/en";

graphql(`
  fragment DimensionValueSelect on FullDimensionType {
    slug
    title(lang: $locale)
    isTechnical
    isMultiValue

    values(lang: $locale) {
      slug
      title(lang: $locale)
    }
  }
`);

export function buildDimensionChoices(
  dimension: DimensionValueSelectFragment,
  includeEmptyChoice: boolean = false,
): Choice[] {
  const choices = dimension.values.map((value) => ({
    slug: value.slug,
    title: value.title ?? value.slug,
  }));

  if (includeEmptyChoice) {
    choices.unshift({
      slug: "",
      title: "",
    });
  }

  return choices;
}

export function buildDimensionField(
  dimension: DimensionValueSelectFragment,
  cachedDimensions: Record<string, string[]>,
  technicalDimensions: "omit" | "readonly" | "editable" = "omit",
  slugPrefix: string = "",
): { field: SingleSelect | MultiSelect; value: string | string[] } {
  const valueList = cachedDimensions[dimension.slug] ?? [];
  let type = dimension.isMultiValue ? "MultiSelect" : "SingleSelect";
  if (type === "SingleSelect" && valueList.length > 1) {
    console.warn(
      "SingleSelect was requested but multiple values were already set.",
      { dimension, cachedDimensions },
    );
    type = "MultiSelect";
  }

  const value = type === "SingleSelect" ? valueList[0] ?? "" : valueList;
  const readOnly = technicalDimensions === "readonly" && dimension.isTechnical;

  const title = dimension.title || dimension.slug;
  const slug = slugPrefix ? `${slugPrefix}.${dimension.slug}` : dimension.slug;

  const field: SingleSelect | MultiSelect =
    type === "SingleSelect"
      ? {
          slug,
          type: "SingleSelect",
          presentation: "dropdown",
          title,
          choices: buildDimensionChoices(dimension),
          readOnly,
        }
      : {
          slug,
          type: "MultiSelect",
          title,
          choices: buildDimensionChoices(dimension),
          readOnly,
        };

  return { field, value };
}

export type TechnicalDimensionsHandling = "omit" | "readonly" | "editable";

export function buildDimensionValueSelectionForm(
  dimensions: DimensionValueSelectFragment[],
  cachedDimensions: Record<string, string[]>,
  technicalDimensions: TechnicalDimensionsHandling = "omit",
  slugPrefix: string = "",
) {
  if (technicalDimensions === "omit") {
    dimensions = dimensions.filter((dimension) => !dimension.isTechnical);
  } else if (technicalDimensions === "readonly") {
    dimensions = dimensions.filter(
      (dimension) =>
        !dimension.isTechnical ||
        (cachedDimensions[dimension.slug] ?? []).length,
    );
  }

  const fieldsValues = dimensions.map((dimension) =>
    buildDimensionField(
      dimension,
      cachedDimensions,
      technicalDimensions,
      slugPrefix,
    ),
  );
  const fields = fieldsValues.map(({ field }) => field);
  const values: Record<string, any> = {};
  fieldsValues.forEach(({ field, value }) => {
    values[field.slug] = value;
  });

  return { fields, values };
}

interface Props {
  dimensions: DimensionValueSelectFragment[];
  cachedDimensions: Record<string, string[]>;
  onChange(formData: FormData): Promise<void>;
  translations: Translations;
  readOnly?: boolean;
  technicalDimensions?: TechnicalDimensionsHandling;
  idPrefix?: string;
  namePrefix?: string;
}

/// A form to select values for dimensions.
export default function DimensionValueSelectionForm({
  dimensions,
  cachedDimensions,
  onChange,
  translations,
  readOnly = false,
  technicalDimensions = "omit",
  idPrefix,
  namePrefix,
}: Props) {
  // TODO Robustify SchemaForm.namePrefix and use it instead?
  const { fields, values } = buildDimensionValueSelectionForm(
    dimensions,
    cachedDimensions,
    technicalDimensions,
    namePrefix,
  );
  const t = translations.Survey;

  return (
    <AutoSubmitForm action={onChange}>
      <SchemaForm
        fields={fields}
        values={values}
        messages={translations.SchemaForm}
        readOnly={readOnly}
        idPrefix={idPrefix}
        highlightReadOnlyFields={true}
      />
      <noscript>
        <SubmitButton>{t.actions.saveDimensions}</SubmitButton>
      </noscript>
    </AutoSubmitForm>
  );
}
