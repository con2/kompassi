import { Field } from "@/components/forms/models";
import type { Translations } from "@/translations/en";

export default function getAnonymityDropdown(
  t: Translations["Survey"],
  readOnly: boolean = false,
): Field {
  return {
    slug: "anonymity",
    type: "SingleSelect",
    presentation: "dropdown",
    required: true,
    choices: [
      {
        slug: "HARD",
        title: t.attributes.anonymity.admin.choices.HARD,
      },
      {
        slug: "SOFT",
        title: t.attributes.anonymity.admin.choices.SOFT,
      },
      {
        slug: "NAME_AND_EMAIL",
        title: t.attributes.anonymity.admin.choices.NAME_AND_EMAIL,
      },
    ],
    title: t.attributes.anonymity.admin.title,
    helpText: t.attributes.anonymity.admin.helpText,
    readOnly,
  };
}
