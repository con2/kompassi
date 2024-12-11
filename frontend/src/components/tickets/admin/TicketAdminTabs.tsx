import Tabs, { Tab } from "@/components/ServerTabs";
import { kompassiBaseUrl } from "@/config";
import { Translations } from "@/translations/en";

interface Props {
  eventSlug: string;
  active: "dashboard" | "orders" | "products" | "quotas" | "ticketControl";
  translations: Translations;
}

export default function TicketAdminTabs(props: Props) {
  const { eventSlug, translations, active } = props;
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
      href: `/${eventSlug}/tickets-admin/orders`,
    },
    {
      slug: "ticketControl",
      title: t.tabs.ticketControl,
      href: `${kompassiBaseUrl}/events/${eventSlug}/ticket-control`,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
