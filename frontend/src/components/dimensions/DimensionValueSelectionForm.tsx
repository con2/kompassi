import AutoSubmitForm from "../AutoSubmitForm";
import { Choice, MultiSelect, SingleSelect } from "../forms/models";
import { SchemaForm } from "../forms/SchemaForm";
import SubmitButton from "../forms/SubmitButton";
import { Dimension } from "./models";
import type { Translations } from "@/translations/en";

export function buildDimensionChoices(
  dimension: Dimension,
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
  dimension: Dimension,
  cachedDimensions: Record<string, string[]>,
  technicalDimensions: "omit" | "readonly" | "editable" = "omit",
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

  const field: SingleSelect | MultiSelect =
    type === "SingleSelect"
      ? {
          slug: dimension.slug,
          type: "SingleSelect",
          presentation: "dropdown",
          title,
          choices: buildDimensionChoices(dimension),
          readOnly,
        }
      : {
          slug: dimension.slug,
          type: "MultiSelect",
          title,
          choices: buildDimensionChoices(dimension),
          readOnly,
        };

  return { field, value };
}

export type TechnicalDimensionsHandling = "omit" | "readonly" | "editable";

export function buildDimensionValueSelectionForm(
  dimensions: Dimension[],
  cachedDimensions: Record<string, string[]>,
  technicalDimensions: TechnicalDimensionsHandling = "omit",
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
    buildDimensionField(dimension, cachedDimensions, technicalDimensions),
  );
  const fields = fieldsValues.map(({ field }) => field);
  const values: Record<string, any> = {};
  fieldsValues.forEach(({ field, value }) => {
    values[field.slug] = value;
  });

  return { fields, values };
}

interface Props {
  dimensions: Dimension[];
  cachedDimensions: Record<string, string[]>;
  onChange(formData: FormData): Promise<void>;
  translations: Translations;
  readOnly?: boolean;
  technicalDimensions?: TechnicalDimensionsHandling;
  idPrefix?: string;
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
}: Props) {
  const { fields, values } = buildDimensionValueSelectionForm(
    dimensions,
    cachedDimensions,
    technicalDimensions,
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
