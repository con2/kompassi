import { DimensionRowGroupFragment } from "@/__generated__/graphql";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import { supportedLanguages } from "@/translations";
import type { Translations } from "@/translations/en";

interface Props {
  messages: {
    SchemaForm: Translations["SchemaForm"];
    Survey: Translations["Survey"];
  };
  dimension?: DimensionRowGroupFragment;
}

const headingLevel = "h5";

export default function DimensionForm({ messages, dimension }: Props) {
  const t = messages.Survey.editDimensionModal;
  // NOTE python_case for slugs!
  // "is_public",
  // "is_key_dimension",
  // "is_multi_value",
  // "is_list_filter",
  // "is_shown_in_detail",
  // "is_negative_selection",
  // "value_ordering",
  const fields: Field[] = [
    {
      type: "SingleLineText",
      slug: "slug",
      required: typeof dimension === "undefined",
      readOnly: typeof dimension !== "undefined",
      ...t.attributes.slug,
    },
    {
      type: "SingleSelect",
      slug: "valueOrdering",
      title: t.attributes.valueOrdering.title,
      helpText: t.attributes.valueOrdering.helpText,
      presentation: "dropdown",
      required: true,
      choices: [
        {
          slug: "MANUAL",
          title: t.attributes.valueOrdering.choices.MANUAL,
        },
        {
          slug: "TITLE",
          title: t.attributes.valueOrdering.choices.TITLE,
        },
        {
          slug: "SLUG",
          title: t.attributes.valueOrdering.choices.SLUG,
        },
      ],
    },
    {
      type: "StaticText",
      slug: "localizedTitleHeader",
      ...t.attributes.localizedTitleHeader,
    },
    ...supportedLanguages.map(
      (locale) =>
        ({
          type: "SingleLineText",
          slug: `title_${locale}`,
          title: t.attributes.title[locale],
        }) as Field,
    ),
    {
      type: "StaticText",
      slug: "behaviourFlagsHeader",
      ...t.attributes.behaviourFlagsHeader,
    },
    {
      type: "SingleCheckbox",
      slug: "isPublic",
      ...t.attributes.isPublic,
    },
    {
      type: "SingleCheckbox",
      slug: "isKeyDimension",
      ...t.attributes.isKeyDimension,
    },
    {
      type: "SingleCheckbox",
      slug: "isMultiValue",
      ...t.attributes.isMultiValue,
    },
    {
      type: "SingleCheckbox",
      slug: "isListFilter",
      ...t.attributes.isListFilter,
    },
    {
      type: "SingleCheckbox",
      slug: "isShownInDetail",
      ...t.attributes.isShownInDetail,
    },
    {
      type: "SingleCheckbox",
      slug: "isNegativeSelection",
      ...t.attributes.isNegativeSelection,
    },
  ];

  // TODO ugly
  let values: Record<string, unknown> = {};
  if (dimension) {
    values = {
      ...dimension,
      // NOTE SUPPORTED_LANGUAGES
      title_fi: dimension.titleFi,
      title_en: dimension.titleEn,
      title_sv: dimension.titleSv,
    };
  } else {
    values = {
      valueOrdering: "TITLE",
      isPublic: true,
      isListFilter: true,
      isShownInDetail: true,
    };
  }

  return (
    <SchemaForm
      fields={fields}
      messages={messages.SchemaForm}
      headingLevel={headingLevel}
      values={values}
    ></SchemaForm>
  );
}
