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
  const fields: Field[] = [
    {
      type: "SingleLineText",
      slug: "slug",
      required: typeof dimension === "undefined",
      readOnly: typeof dimension !== "undefined",
      ...t.attributes.slug,
    },
    {
      type: "SingleCheckbox",
      slug: "is_key_dimension",
      title: t.attributes.isKeyDimension.title,
      helpText: t.attributes.isKeyDimension.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "is_multi_value",
      title: t.attributes.isMultiValue.title,
      helpText: t.attributes.isMultiValue.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "is_shown_to_subject",
      title: t.attributes.isShownToSubject.title,
      helpText: t.attributes.isShownToSubject.helpText,
    },
    {
      type: "StaticText",
      slug: "header",
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
  ];

  // TODO ugly
  let values: Record<string, unknown> = {};
  if (dimension) {
    values = {
      // NOTE SUPPORTED_LANGUAGES
      title_fi: dimension.titleFi,
      title_en: dimension.titleEn,
      title_sv: dimension.titleSv,
      ...dimension,
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
