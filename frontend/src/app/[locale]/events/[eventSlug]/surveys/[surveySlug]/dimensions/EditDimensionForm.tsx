import { HeadingLevel } from "@/components/helpers/Heading";
import { SchemaForm } from "@/components/SchemaForm";
import { Field, Layout } from "@/components/SchemaForm/models";
import { supportedLanguages } from "@/translations";
import type { Translations } from "@/translations/en";

interface Props {
  headingLevel: HeadingLevel;
  messages: {
    SchemaForm: Translations["SchemaForm"];
    Survey: Translations["Survey"];
  };
}

export default function EditDimensionForm({ messages, headingLevel }: Props) {
  const t = messages.Survey.editDimensionModal;
  const fields: Field[] = [
    {
      type: "SingleLineText",
      slug: "slug",
      required: true,
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

  return (
    <SchemaForm
      fields={fields}
      layout={Layout.Vertical}
      messages={messages.SchemaForm}
      headingLevel={headingLevel}
    ></SchemaForm>
  );
}
