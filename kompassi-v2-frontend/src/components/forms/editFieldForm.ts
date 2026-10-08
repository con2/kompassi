import { Choice, DimensionUniverse, Field, FieldType, Values } from "./models";
import processFormData from "./processFormData";
import { DimensionValueSelectFragment } from "@/__generated__/graphql";

export type FormEditorContext = "survey" | "program" | "involvement";

/// A dimension the editor offers to dimension fields. Program forms get the dimensions of
/// both universes of the event, each tagged with its universe; surveys get untagged ones.
export type EditorDimension = DimensionValueSelectFragment & {
  universe?: DimensionUniverse;
};

/// The universe a dimension field refers to, for looking it up among EditorDimensions.
/// Survey fields have no universe and match by slug alone.
export function getFieldDimensionUniverse(
  field: Field,
  defaultDimensionUniverse?: DimensionUniverse,
): DimensionUniverse | undefined {
  if (
    field.type !== "DimensionSingleSelect" &&
    field.type !== "DimensionMultiSelect" &&
    field.type !== "DimensionSingleCheckbox"
  ) {
    return undefined;
  }
  return field.dimensionUniverse ?? defaultDimensionUniverse;
}

export function findEditorDimension(
  dimensions: EditorDimension[],
  dimensionSlug: string,
  universe: DimensionUniverse | undefined,
): EditorDimension | undefined {
  return dimensions.find(
    (dimension) =>
      dimension.slug === dimensionSlug &&
      (universe === undefined || dimension.universe === universe),
  );
}

/// The dimension dropdown of the field editor encodes the universe into the choice slug
/// so that one dropdown can offer the dimensions of both universes.
function encodeDimensionChoice(dimension: EditorDimension): string {
  return dimension.universe
    ? `${dimension.universe}/${dimension.slug}`
    : dimension.slug;
}

function decodeDimensionChoice(value: string): {
  dimension: string;
  dimensionUniverse?: DimensionUniverse;
} {
  const separator = value.indexOf("/");
  if (separator === -1) {
    return { dimension: value };
  }
  return {
    dimensionUniverse: value.slice(0, separator) as DimensionUniverse,
    dimension: value.slice(separator + 1),
  };
}

export interface AnnotationOption {
  slug: string;
  title: string;
  isApplicableToProgramItems: boolean;
  isApplicableToInvolvements: boolean;
}

const annotationPropagatingTypes: FieldType[] = [
  "SingleLineText",
  "MultiLineText",
  "MarkdownText",
  "SingleCheckbox",
  "NumberField",
  "DecimalField",
  "DateField",
  "TimeField",
  "DateTimeField",
];

const dimensionFieldTypes: FieldType[] = [
  "DimensionSingleSelect",
  "DimensionMultiSelect",
  "DimensionSingleCheckbox",
];
import type { Translations } from "@/translations/en";

export function getFieldEditorFields(
  fieldType: FieldType,
  messages: Translations["FormEditor"]["editFieldForm"],
  dimensions: EditorDimension[],
  annotations: AnnotationOption[] = [],
  formContext: FormEditorContext = "survey",
): Field[] {
  const t = messages;
  const slugField: Field = {
    type: "SingleLineText",
    slug: "slug",
    required: true,
    ...t.slug,
  };

  const baseFieldEditorFields: Field[] = [
    slugField,
    {
      type: "SingleLineText",
      slug: "title",
      required: false,
      ...t.title,
    },
    {
      type: "MarkdownText",
      slug: "helpText",
      required: false,
      rows: 3,
      ...t.helpText,
    },
  ];

  const editableFieldFields: Field[] = baseFieldEditorFields.concat([
    {
      type: "SingleCheckbox",
      slug: "required",
      required: false,
      ...t.required,
    },
    {
      type: "SingleCheckbox",
      slug: "isKeyField",
      required: false,
      ...t.isKeyField,
    },
  ]);

  const propagationFields: Field[] = [];
  // survey responses have no target object to pass values forward to
  if (formContext !== "survey") {
    if (dimensionFieldTypes.includes(fieldType)) {
      propagationFields.push(
        {
          type: "SingleCheckbox",
          slug: "propagateDimensionOnCreate",
          required: false,
          title: t.propagateDimensionOnCreate.title,
          helpText: t.propagateDimensionOnCreate.helpText[formContext],
        },
        {
          type: "SingleCheckbox",
          slug: "propagateDimensionOnEdit",
          required: false,
          title: t.propagateDimensionOnEdit.title,
          helpText: t.propagateDimensionOnEdit.helpText[formContext],
        },
      );
    } else if (annotationPropagatingTypes.includes(fieldType)) {
      const applicable = annotations.filter((annotation) =>
        formContext === "involvement"
          ? annotation.isApplicableToInvolvements
          : annotation.isApplicableToProgramItems,
      );
      propagationFields.push(
        {
          type: "SingleSelect",
          slug: "propagateToAnnotation",
          required: false,
          presentation: "dropdown",
          choices: [
            { slug: "", title: t.propagateToAnnotation.none },
            ...applicable.map(({ slug, title }) => ({ slug, title })),
          ],
          title: t.propagateToAnnotation.title,
          helpText: t.propagateToAnnotation.helpText[formContext],
        },
        {
          type: "SingleCheckbox",
          slug: "propagateToAnnotationOnEdit",
          required: false,
          ...t.propagateToAnnotationOnEdit,
        },
      );
    }
  }

  const choicesField: Field = {
    type: "MultiLineText",
    slug: "choices",
    required: true,
    ...t.choices,
  };

  const questionsField: Field = {
    type: "MultiLineText",
    slug: "questions",
    required: true,
    ...t.questions,
  };

  const dimensionField: Field = {
    type: "SingleSelect",
    slug: "dimension",
    required: true,
    presentation: "dropdown",
    choices: dimensions.map((dimension) => {
      const title = dimension.title || dimension.slug;
      return {
        slug: encodeDimensionChoice(dimension),
        title: dimension.universe
          ? `${t.dimensionUniverse[dimension.universe]}: ${title}`
          : title,
      };
    }),
    ...t.dimension,
  };

  const maxLengthField: Field = {
    type: "NumberField",
    slug: "maxLength",
    required: false,
    ...t.maxLength,
  };

  // const encryptTo: Field = {
  //   type: "MultiLineText",
  //   slug: "encryptTo",
  //   required: false,
  //   rows: 3,
  //   ...t.encryptTo,
  // };

  const fields = getTypeSpecificFields();
  return fields.concat(propagationFields);

  function getTypeSpecificFields(): Field[] {
    switch (fieldType) {
      case "SingleSelect":
      case "MultiSelect":
        return editableFieldFields.concat([choicesField]); // , encryptTo]);
      case "DimensionSingleSelect":
      case "DimensionMultiSelect":
      case "DimensionSingleCheckbox":
        return editableFieldFields.concat([dimensionField]); // , encryptTo]);
      case "RadioMatrix":
        return editableFieldFields.concat([
          questionsField,
          choicesField,
          // encryptTo,
        ]);
      case "MultiLineText":
      case "MarkdownText":
        return editableFieldFields.concat([maxLengthField]);
      case "Divider":
      case "Spacer":
        return [slugField];
      case "StaticText":
        return baseFieldEditorFields;
      default:
        // TODO implement encryption
        return editableFieldFields;
      // default:
      //   return baseFieldEditorFields.concat([encryptTo]);
    }
  }
}

function formatChoices(choices: Choice[]): string {
  return (
    choices?.map((choice) => `${choice.slug}: ${choice.title}`).join("\n") ?? ""
  );
}

export function fieldToValues(
  field: Field,
  defaultDimensionUniverse?: DimensionUniverse,
): Record<string, any> {
  let choices: string | undefined = undefined;
  let questions: string | undefined = undefined;
  let dimension: string | undefined = undefined;

  const encryptTo = field.encryptTo ? field.encryptTo.join("\n") : "";

  switch (field.type) {
    case "SingleSelect":
    case "MultiSelect":
      choices = formatChoices(field.choices);
      break;
    case "RadioMatrix":
      choices = formatChoices(field.choices);
      questions = formatChoices(field.questions);
      break;
    case "DimensionSingleSelect":
    case "DimensionMultiSelect":
    case "DimensionSingleCheckbox": {
      const universe = getFieldDimensionUniverse(
        field,
        defaultDimensionUniverse,
      );
      dimension =
        universe && field.dimension
          ? `${universe}/${field.dimension}`
          : field.dimension;
      break;
    }
  }

  return { ...field, choices, questions, encryptTo, dimension };
}

function parseChoices(choices: string): Choice[] {
  return choices
    .split("\n")
    .map((line) => {
      const [slug, ...titleParts] = line.split(": ");
      const title = titleParts.join(": ");
      return { slug, title };
    })
    .filter((choice) => choice.slug && choice.title);
}

export function formDataToField(
  fields: Field[],
  initialValues: Field,
  formData: FormData,
): Field {
  const values: Values = {
    ...processFormData(fields, formData),
    encryptTo: ((formData.get("encryptTo") as string) || "").split("\n"),
  };

  // the backend rejects "on edit" without an annotation to pass forward to
  if (
    "propagateToAnnotationOnEdit" in values &&
    !values.propagateToAnnotation
  ) {
    values.propagateToAnnotationOnEdit = false;
  }

  switch (initialValues.type) {
    case "SingleSelect":
    case "MultiSelect":
      return {
        ...initialValues,
        ...values,
        choices: parseChoices(values.choices as string),
      };
    case "RadioMatrix":
      return {
        ...initialValues,
        ...values,
        choices: parseChoices(values.choices as string),
        questions: parseChoices(values.questions as string),
      };
    case "DimensionSingleSelect":
    case "DimensionMultiSelect":
    case "DimensionSingleCheckbox":
      // an unqualified choice must clear a qualifier the field had before
      return {
        ...initialValues,
        ...values,
        dimensionUniverse: undefined,
        ...decodeDimensionChoice(String(values.dimension ?? "")),
      } as Field;
    default:
      return { ...initialValues, ...values };
  }
}
