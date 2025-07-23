import { createProgramFormLanguage } from "../../../program-forms/[surveySlug]/edit/actions";
import { createSurveyLanguage } from "./actions";
import { Survey } from "./models";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ModalButton from "@/components/ModalButton";
import ServerTabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  eventSlug: string;
  survey: Survey;
  active: string;
  mode: "surveys" | "program-forms";
}

export default function SurveyEditorTabs({
  translations,
  eventSlug,
  survey,
  active,
  mode,
}: Props) {
  const t = translations.Survey;
  const supportedLanguages: Record<string, string> =
    translations.LanguageSwitcher.supportedLanguages;

  const url = `/${eventSlug}/${mode}/${survey.slug}`;
  const tabs: Tab[] = [
    {
      slug: "properties",
      title: t.tabs.properties,
      href: `${url}/edit`,
    },
  ];

  if (mode === "surveys") {
    tabs.push({
      slug: "dimensions",
      title: t.attributes.dimensions,
      href: `${url}/dimensions`,
    });
  }

  tabs.push({
    slug: "dimensionDefaults",
    title: t.attributes.dimensionDefaults.title,
    href: `${url}/dimension-defaults`,
  });

  for (const languageVersion of survey.languages) {
    // graphql enums are upper case :(
    const languageCode = languageVersion.language.toLowerCase();
    const languageName =
      supportedLanguages[languageCode] ?? languageVersion.language;

    tabs.push({
      slug: `texts-${languageCode}`,
      title: t.tabs.texts(languageName),
      href: `${url}/edit/${languageCode}`,
    });

    // TODO un-hide the field editor when it works
    tabs.push({
      slug: `fields-${languageCode}`,
      title: t.tabs.fields(languageName),
      href: `${url}/edit/${languageCode}/fields`,
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

  const addLanguageAction = (
    mode === "program-forms" ? createProgramFormLanguage : createSurveyLanguage
  ).bind(null, eventSlug, survey.slug);

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
          action={addLanguageAction}
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
