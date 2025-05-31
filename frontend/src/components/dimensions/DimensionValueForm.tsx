import colors from "./colors";
import { ValueFieldsFragment } from "@/__generated__/graphql";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
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
export default function DimensionValueForm({ messages, value }: Props) {
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
      type: "SingleSelect",
      presentation: "dropdown",
      slug: "color",
      choices: colors.map((color) => ({
        slug: color.toLowerCase(),
        title: color,
      })),
      ...t.attributes.color,
    },
    {
      type: "SingleCheckbox",
      slug: "isSubjectLocked",
      ...t.attributes.isSubjectLocked,
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
  if (value) {
    values = {
      // NOTE SUPPORTED_LANGUAGES
      title_fi: value.titleFi,
      title_en: value.titleEn,
      title_sv: value.titleSv,
      ...value,
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
