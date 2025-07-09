import Tabs, { Tab } from "@/components/ServerTabs";
import { kompassiBaseUrl } from "@/config";
import { Translations } from "@/translations/en";

interface Props {
  eventSlug: string;
  active: "dashboard" | "orders" | "products" | "quotas" | "ticketControl";
  translations: Translations;
  queryString?: string;
}

export default function TicketAdminTabs({
  eventSlug,
  translations,
  active,
  queryString,
}: Props) {
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
