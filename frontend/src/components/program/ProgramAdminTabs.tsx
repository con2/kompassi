import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

export interface ProgramAdminTabsProps {
  eventSlug: string;
  active:
    | "programForms"
    | "programOffers"
    | "programItems"
    | "programHosts"
    | "dimensions"
    | "preferences";
  translations: Translations;
  searchParams?: Record<string, string>;
}

export default function ProgramAdminTabs({
  eventSlug,
  translations,
  active,
  searchParams,
}: ProgramAdminTabsProps) {
  const t = translations.Program;

  // Strip non-dimension search parameters from the query string
  // to avoid passing them to the tabs, as they are not relevant there.
  const { success, error, ...forwardSearchParams } = searchParams || {};
  const queryString =
    Object.keys(forwardSearchParams).length > 0
      ? "?" + new URLSearchParams(forwardSearchParams).toString()
      : "";

  const tabs: Tab[] = [
    {
      slug: "programForms",
      title: t.ProgramForm.listTitle,
      href: `/${eventSlug}/program-forms`,
    },
    {
      slug: "programOffers",
      title: t.ProgramOffer.listTitle,
      href: `/${eventSlug}/program-offers${queryString}`,
    },
    {
      slug: "programItems",
      title: t.adminListTitle,
      href: `/${eventSlug}/program-admin${queryString}`,
    },
    {
      slug: "programHosts",
      title: t.ProgramHost.listTitle,
      href: `/${eventSlug}/program-hosts${queryString}`,
    },
    {
      slug: "dimensions",
      title: translations.Dimension.listTitle,
      href: `/${eventSlug}/program-dimensions`,
    },
    {
      slug: "preview",
      title: t.actions.preview,
      href: `/${eventSlug}/program${queryString}`,
      // Program view has no admin controls, so treat it as external for now
      external: true,
    },
    {
      slug: "preferences",
      title: t.actions.preferences,
      href: `/${eventSlug}/program-preferences`,
      disabled: true,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
