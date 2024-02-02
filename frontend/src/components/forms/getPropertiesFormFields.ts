import { Field } from "./models";
import { Translations } from "@/translations/en";

export function getPropertiesFormFields(
  messages: Translations["FormEditor"]["FormPropertiesForm"],
): Field[] {
  return [
    {
      slug: "title",
      type: "SingleLineText",
      title: messages.title.title,
      helpText: messages.title.helpText,
    },
    {
      slug: "layout",
      type: "SingleSelect",
      title: messages.layout.title,
      helpText: messages.layout.helpText,
      choices: [
        {
          slug: "vertical",
          title: messages.layout.choices.vertical,
        },
        {
          slug: "horizontal",
          title: messages.layout.choices.horizontal,
        },
      ],
    },
  ];
}
