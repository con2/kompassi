import Tabs, { Tab } from "@/components/ServerTabs";
import { kompassiBaseUrl } from "@/config";
import { Translations } from "@/translations/en";

export interface TicketsAdminTabsProps {
  eventSlug: string;
  active: "dashboard" | "orders" | "products" | "quotas" | "ticketControl";
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
    success: _success,
    error: _error,
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
      href: `/${eventSlug}/orders-admin${queryString ? `?${queryString}` : ""}`,
    },
    {
      slug: "ticketControl",
      title: t.tabs.ticketControl,
      href: `${kompassiBaseUrl}/events/${eventSlug}/pos`,
      getTabHeader() {
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
