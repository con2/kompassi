import { Anonymity, ProfileSurveyFragment } from "@/__generated__/graphql";
import { Field, SingleSelect } from "@/components/forms/models";
import type { Translations } from "@/translations/en";

export function getAnonymityDropdown(
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

export function getCopyFromDropdown(
  t: Translations["Survey"],
  surveys: ProfileSurveyFragment[],
): SingleSelect {
  return {
    slug: "copyFrom",
    type: "SingleSelect",
    presentation: "dropdown",
    required: false,
    choices: surveys.map((survey) => ({
      slug: `${survey.event.slug}/${survey.slug}`,
      title: `${survey.event.name}: ${survey.title}`,
    })),
    ...t.attributes.cloneFrom,
  };
}
