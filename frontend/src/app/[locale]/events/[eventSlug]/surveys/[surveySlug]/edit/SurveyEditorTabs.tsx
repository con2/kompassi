import ModalButton from "../dimensions/ModalButton";
import { createSurveyLanguage } from "./actions";
import { Survey } from "./models";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ServerTabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  eventSlug: string;
  survey: Survey;
  active: string;
}

export default function SurveyEditorTabs({
  translations,
  eventSlug,
  survey,
  active,
}: Props) {
  const t = translations.Survey;
  const supportedLanguages: Record<string, string> =
    translations.LanguageSwitcher.supportedLanguages;

  const url = `/events/${eventSlug}/surveys/${survey.slug}/edit/`;
  const tabs: Tab[] = [
    {
      slug: "properties",
      title: t.tabs.properties,
      href: `${url}`,
    },
  ];

  for (const languageVersion of survey.languages) {
    // graphql enums are upper case :(
    const languageCode = languageVersion.language.toLowerCase();
    const languageName =
      supportedLanguages[languageCode] ?? languageVersion.language;

    tabs.push({
      slug: languageCode,
      title: t.tabs.languageVersion(languageName),
      href: `${url}/${languageCode}`,
    });
  }

  // languages that are not yet added to the survey
  const potentialLanguages = Object.entries(supportedLanguages).filter(
    ([languageCode, _]) =>
      !survey.languages.find(
        (form) => form.language.toLowerCase() === languageCode,
      ),
  );

  const addLanguageFields: Field[] = [
    {
      slug: "language",
      type: "SingleSelect",
      presentation: "dropdown",
      required: true,
      choices: potentialLanguages.map(([languageCode, language]) => ({
        slug: languageCode,
        title: language,
      })),
      ...t.addLanguageModal.language,
    },
  ];

  if (survey.languages.length > 0) {
    addLanguageFields.push({
      slug: "copyFrom",
      type: "SingleSelect",
      presentation: "dropdown",
      choices: survey.languages.map((form) => ({
        slug: form.language.toLowerCase(),
        title: supportedLanguages[form.language.toLowerCase()] ?? form.language,
      })),
      ...t.addLanguageModal.copyFrom,
    });
  }

  // prefill the form if there's only one option
  const addLanguageValues: Record<string, string> = {};
  if (potentialLanguages.length === 1) {
    addLanguageValues.language = potentialLanguages[0][0];
  }
  if (survey.languages.length === 1) {
    addLanguageValues.copyFrom = survey.languages[0].language.toLowerCase();
  }

  tabs.push({
    slug: "addLanguage",
    title: t.tabs.addLanguage,
    getTabHeader() {
      return (
        <ModalButton
          className="nav-link"
          title={t.tabs.addLanguage}
          label={`➕ ${t.tabs.addLanguage}…`}
          messages={t.addLanguageModal.actions}
          action={createSurveyLanguage.bind(null, eventSlug, survey.slug)}
          disabled={potentialLanguages.length === 0}
        >
          <SchemaForm
            fields={addLanguageFields}
            values={addLanguageValues}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      );
    },
  });

  return <ServerTabs tabs={tabs} active={active} />;
}
