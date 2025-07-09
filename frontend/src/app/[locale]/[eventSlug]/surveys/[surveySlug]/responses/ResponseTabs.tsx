import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

interface Props {
  eventSlug: string;
  surveySlug: string;
  searchParams: Record<string, string>;
  active: "responses" | "summary";
  translations: Translations;
}

export default function ResponseTabs(props: Props) {
  const { eventSlug, surveySlug, translations, active, searchParams } = props;
  const t = translations.Survey;
  const query = new URLSearchParams(searchParams).toString();
  const tabs: Tab[] = [
    {
      slug: "responses",
      title: t.tabs.responses,
      href: `/${eventSlug}/surveys/${surveySlug}/responses?${query}`,
    },
    {
      slug: "summary",
      title: t.tabs.summary,
      href: `/${eventSlug}/surveys/${surveySlug}/responses/summary?${query}`,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
