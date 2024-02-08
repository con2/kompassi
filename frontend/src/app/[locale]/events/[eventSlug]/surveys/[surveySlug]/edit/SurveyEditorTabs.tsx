import ModalButton from "../dimensions/ModalButton";
import { EditSurveyPageFragment } from "@/__generated__/graphql";
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
  const tabs: Tab[] = [
    {
      slug: "properties",
      title: t.tabs.properties,
      href: "/edit",
    },
  ];

  tabs.push({
    slug: "addLanguage",
    title: `➕ ${t.tabs.addLanguage}…`,
    getTabHeader() {
      return (
        <ModalButton
          className="nav-link"
          title={this.title}
          messages={t.addLanguageModal.actions}
        >
          TODO
        </ModalButton>
      );
    },
  });
  return <ServerTabs tabs={tabs} active={active} />;
}
