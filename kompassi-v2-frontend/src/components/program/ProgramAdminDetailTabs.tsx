import { ServerTabs as Tabs, Tab } from "@con2/components";
import { Translations } from "@/translations/en";

export type ProgramAdminTab =
  | "basicInfo"
  | "scheduleItems"
  | "programHosts"
  | "dimensions"
  | "annotations"
  | "preview";

export interface ProgramAdminTabsProps {
  eventSlug: string;
  programSlug: string;
  active: ProgramAdminTab;
  translations: Translations;
}

export default function ProgramAdminDetailTabs({
  eventSlug,
  programSlug,
  translations,
  active,
}: ProgramAdminTabsProps) {
  const t = translations.Program;

  const tabs: Tab[] = [
    {
      slug: "basicInfo",
      title: t.adminDetailTabs.basicInfo,
      href: `/${eventSlug}/program-admin/${programSlug}`,
    },
    {
      slug: "scheduleItems",
      title: t.adminDetailTabs.scheduleItems,
      href: `/${eventSlug}/program-admin/${programSlug}/schedule`,
    },
    {
      slug: "programHosts",
      title: t.adminDetailTabs.programHosts,
      href: `/${eventSlug}/program-admin/${programSlug}/hosts`,
    },
    {
      slug: "dimensions",
      title: t.adminDetailTabs.dimensions,
      href: `/${eventSlug}/program-admin/${programSlug}/dimensions`,
    },
    {
      slug: "annotations",
      title: t.adminDetailTabs.annotations,
      href: `/${eventSlug}/program-admin/${programSlug}/annotations`,
    },
    {
      slug: "preview",
      title: t.adminDetailTabs.preview,
      href: `/${eventSlug}/program-preview/${programSlug}`,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
