import { DimensionRowGroupFragment } from "@/__generated__/graphql";
import { Field, Layout } from "@/components/forms/models";
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
      slug: "isKeyDimension",
      title: t.attributes.isKeyDimension.title,
      helpText: t.attributes.isKeyDimension.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "isMultiValue",
      title: t.attributes.isMultiValue.title,
      helpText: t.attributes.isMultiValue.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "isShownToRespondent",
      title: t.attributes.isShownToRespondent.title,
      helpText: t.attributes.isShownToRespondent.helpText,
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
          slug: `title.${locale}`,
          title: t.attributes.title[locale],
        }) as Field,
    ),
  ];

  // TODO ugly
  let values: Record<string, unknown> = {};
  if (dimension) {
    values = {
      slug: dimension.slug,
      isKeyDimension: dimension.isKeyDimension,
      isMultiValue: dimension.isMultiValue,
      isShownToRespondent: dimension.isShownToRespondent,
      // TODO hard-coded languages
      "title.fi": dimension.titleFi,
      "title.en": dimension.titleEn,
    };
  }

  return (
    <SchemaForm
      fields={fields}
      layout={Layout.Vertical}
      messages={messages.SchemaForm}
      headingLevel={headingLevel}
      values={values}
    ></SchemaForm>
  );
}
