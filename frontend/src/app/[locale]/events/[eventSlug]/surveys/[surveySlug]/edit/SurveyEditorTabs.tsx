import ModalButton from "../dimensions/ModalButton";
import { addLanguageVersion } from "./actions";
import { EditSurveyPageFragment } from "@/__generated__/graphql";
import { Field } from "@/components/forms/models";
import { SchemaForm } from "@/components/forms/SchemaForm";
import ServerTabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  eventSlug: string;
  survey: EditSurveyPageFragment;
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

  const tabs: Tab[] = [
    {
      slug: "properties",
      title: t.tabs.properties,
      href: "/edit",
    },
  ];
  for (const languageVersion of survey.languages) {
    // graphql enums are upper case :(
    const languageCode = languageVersion.language.toLowerCase();

    tabs.push({
      slug: languageCode,
      title: supportedLanguages[languageCode] ?? languageVersion.language,
      href: `/events/${eventSlug}/surveys/${survey.slug}/edit/${languageCode}`,
    });
  }

  const addLanguageFields: Field[] = [
    {
      slug: "language",
      type: "SingleSelect",
      title: t.addLanguageModal.language,
      choices: Object.entries(supportedLanguages).map(
        ([languageCode, language]) => ({
          slug: languageCode,
          title: language,
        }),
      ),
    },
  ];

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
          action={addLanguageVersion.bind(null, eventSlug, survey.slug)}
        >
          <SchemaForm
            fields={addLanguageFields}
            messages={translations.SchemaForm}
          />
        </ModalButton>
      );
    },
  });
  return <ServerTabs tabs={tabs} active={active} />;
}
