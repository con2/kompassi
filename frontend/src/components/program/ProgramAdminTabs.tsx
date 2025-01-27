import Tabs, { Tab } from "@/components/ServerTabs";
import { Translations } from "@/translations/en";

interface Props {
  eventSlug: string;
  active: "offerForms" | "offers" | "dimensions";
  translations: Translations;
  queryString?: string;
}

export default function ProgramAdminTabs({
  eventSlug,
  translations,
  active,
  queryString,
}: Props) {
  const t = translations.Program;
  queryString = queryString ? "?" + queryString : "";

  const tabs: Tab[] = [
    {
      slug: "offerForms",
      title: t.OfferForm.listTitle,
      href: `/${eventSlug}/offer-forms`,
    },
    {
      slug: "offers",
      title: t.Offer.listTitle,
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
    {
      slug: "preferences",
      title: t.actions.preferences,
      href: `/${eventSlug}/program-preferences`,
    },
  ];

  return <Tabs tabs={tabs} active={active} />;
}
