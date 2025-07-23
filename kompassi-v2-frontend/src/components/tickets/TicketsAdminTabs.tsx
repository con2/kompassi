import Tabs, { Tab } from "@/components/ServerTabs";
import { kompassiBaseUrl } from "@/config";
import { Translations } from "@/translations/en";

export interface TicketsAdminTabsProps {
  eventSlug: string;
  active:
    | "dashboard"
    | "orders"
    | "products"
    | "quotas"
    | "reports"
    | "ticketControl";
  translations: Translations;
  searchParams: Record<string, string>;
}

export default function TicketsAdminTabs({
  eventSlug,
  translations,
  active,
  searchParams,
}: TicketsAdminTabsProps) {
  const {
    success: _success, // eslint-disable-line @typescript-eslint/no-unused-vars
    error: _error, // eslint-disable-line @typescript-eslint/no-unused-vars
    ...passedSearchParams
  } = searchParams;
  const queryString = new URLSearchParams(passedSearchParams).toString();
  const t = translations.Tickets.admin;
  const tabs: Tab[] = [
    {
      slug: "products",
      title: t.tabs.products,
      href: `/${eventSlug}/products`,
    },
    {
      slug: "quotas",
      title: t.tabs.quotas,
      href: `/${eventSlug}/quotas`,
    },
    {
      slug: "orders",
      title: t.tabs.orders,
      href: `/${eventSlug}/orders-admin${queryString ? "?" + queryString : ""}`,
    },
    {
      slug: "reports",
      title: t.tabs.reports,
      href: `/${eventSlug}/tickets-reports`,
    },
    {
      slug: "webShop",
      title: t.tabs.webShop,
      href: `/${eventSlug}/tickets`,
      external: true,
    },
    {
      slug: "ticketControl",
      title: t.tabs.ticketControl,
      href: `${kompassiBaseUrl}/events/${eventSlug}/pos`,
      external: true,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
