import { ValueFieldsFragment } from "@/__generated__/graphql";
import { SchemaForm } from "@/components/SchemaForm";
import { Field, Layout } from "@/components/SchemaForm/models";
import { supportedLanguages } from "@/translations";
import type { Translations } from "@/translations/en";

interface Props {
  messages: {
    SchemaForm: Translations["SchemaForm"];
    Survey: Translations["Survey"];
  };
  value?: ValueFieldsFragment;
}

const headingLevel = "h5";

/// Value form society. Value form life.
export default function ValueForm({ messages, value }: Props) {
  const t = messages.Survey.editValueModal;
  const fields: Field[] = [
    {
      type: "SingleLineText",
      slug: "slug",
      required: typeof value === "undefined",
      readOnly: typeof value !== "undefined",
      ...t.attributes.slug,
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
  if (value) {
    values = {
      slug: value.slug,
      // TODO hard-coded languages
      "title.fi": value.titleFi,
      "title.en": value.titleEn,
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
