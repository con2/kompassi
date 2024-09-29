import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

export type ProgramTab = "cards" | "table";
export const programTabs: ProgramTab[] = ["cards", "table"];

interface Props {
  eventSlug: string;
  searchParams: Record<string, string>;
  active: ProgramTab;
  translations: Translations;
}

export default function ProgramTabs(props: Props) {
  const { eventSlug, translations, active, searchParams } = props;
  const t = translations.Program;
  const href = (display: ProgramTab) => {
    const query = new URLSearchParams(searchParams);
    query.set("display", display);
    return `/${eventSlug}/program?${query.toString()}`;
  };
  const tabs: Tab[] = programTabs.map((display) => ({
    slug: display,
    title: t.tabs[display],
    href: href(display),
  }));

  return <Tabs tabs={tabs} active={active} />;
}
