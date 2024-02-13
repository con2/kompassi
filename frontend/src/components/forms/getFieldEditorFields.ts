import { Field, FieldType } from "./models";
import type { Translations } from "@/translations/en";

export default function getFieldEditorFields(
  fieldType: FieldType,
  messages: Translations["FormEditor"]["editFieldForm"],
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
      type: "MultiLineText",
      slug: "helpText",
      required: false,
      ...t.helpText,
    },
    {
      type: "SingleCheckbox",
      slug: "required",
      required: false,
      ...t.required,
    },
  ];

  const choicesField: Field = {
    type: "MultiLineText",
    slug: "choices",
    required: true,
    ...t.choices,
  };

  switch (fieldType) {
    case "SingleSelect":
    case "MultiSelect":
    case "RadioMatrix":
      return baseFieldEditorFields.concat([choicesField]);
    case "Divider":
    case "Spacer":
      return [slugField];
    default:
      return baseFieldEditorFields;
  }
}
