import { Anonymity } from "@/__generated__/graphql";
import { Field } from "@/components/forms/models";
import type { Translations } from "@/translations/en";

export default function getAnonymityDropdown(
  t: Translations["Survey"],
  readOnly: boolean = false,
): Field {
  const anonymityOptions: Anonymity[] = [
    Anonymity.Hard,
    Anonymity.Soft,
    Anonymity.NameAndEmail,
  ];

  return {
    slug: "anonymity",
    type: "SingleSelect",
    // TODO: Long descriptions. Need a card-based radio button component.
    presentation: "dropdown",
    required: true,
    choices: anonymityOptions.map((option) => ({
      slug: option,
      title: `${t.attributes.anonymity.admin.choices[option]}: ${t.attributes.anonymity.thirdPerson.choices[option]}`,
    })),
    title: t.attributes.anonymity.admin.title,
    helpText: t.attributes.anonymity.admin.helpText,
    readOnly,
  };
}
