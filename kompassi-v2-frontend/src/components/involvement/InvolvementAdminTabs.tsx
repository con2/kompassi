import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

export interface InvolvementAdminTabsProps {
  eventSlug: string;
  active: "people" | "dimensions" | "registries";
  translations: Translations;
  searchParams?: Record<string, string>;
}

export default function InvolvementAdminTabs({
  eventSlug,
  translations,
  active,
  searchParams,
}: InvolvementAdminTabsProps) {
  const t = translations.Involvement;
  const regisTry = translations.Registry;
  const dimensionT = translations.Dimension;

  // Strip non-dimension search parameters from the query string
  // to avoid passing them to the tabs, as they are not relevant there.
  const {
    success: _success, // eslint-disable-line @typescript-eslint/no-unused-vars
    error: _error, // eslint-disable-line @typescript-eslint/no-unused-vars
    ...forwardSearchParams
  } = searchParams || {};
  const queryString =
    Object.keys(forwardSearchParams).length > 0
      ? "?" + new URLSearchParams(forwardSearchParams).toString()
      : "";

  const tabs: Tab[] = [
    {
      slug: "people",
      title: t.listTitle,
      href: `/${eventSlug}/people?${queryString}`,
    },
    {
      slug: "dimensions",
      title: dimensionT.listTitle,
      href: `/${eventSlug}/involvement-dimensions`,
    },
    {
      slug: "registries",
      title: regisTry.listTitle,
      href: `/${eventSlug}/registries`,
      disabled: true,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
