import { Field } from "./models";
import { Translations } from "@/translations/en";

export function getPropertiesFormFields(
  messages: Translations["FormEditor"]["formPropertiesForm"],
): Field[] {
  const rows = 3;
  return [
    {
      slug: "title",
      type: "SingleLineText",
      ...messages.title,
    },
    {
      slug: "description",
      type: "MultiLineText",
      rows,
      ...messages.description,
    },
    {
      slug: "thankYouMessage",
      type: "MultiLineText",
      rows,
      ...messages.thankYouMessage,
    },
  ];
}
