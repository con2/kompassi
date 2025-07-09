import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

export type ProgramAdminTab =
  | "basicInfo"
  | "scheduleItems"
  | "programHosts"
  | "dimensions"
  | "annotations";

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
      disabled: true,
    },
    {
      slug: "preview",
      title: t.adminDetailTabs.preview,
      href: `/${eventSlug}/programs/${programSlug}`,
      getTabHeader() {
        // Program view has no admin controls, so treat it as external for now
        return (
          <a
            className="nav-link"
            href={this.href}
            target="_blank"
            rel="noopener noreferrer"
          >
            {this.title}…
          </a>
        );
      },
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
