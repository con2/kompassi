import Messages from "../errors/Messages";
import ViewContainer from "../ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "../ViewHeading";
import TicketsAdminTabs, { TicketsAdminTabsProps } from "./TicketsAdminTabs";
import { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  event: {
    name: string;
    slug: string;
  };
  searchParams?: Record<string, string>;
  children: React.ReactNode;
  actions?: React.ReactNode;
  active: TicketsAdminTabsProps["active"];
}

export default function TicketsAdminView({
  translations,
  event,
  searchParams = {},
  children,
  actions,
  active,
}: Props) {
  const t = translations.Tickets;

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.admin.title}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        {actions && <ViewHeadingActions>{actions}</ViewHeadingActions>}
      </ViewHeadingActionsWrapper>

      <Messages messages={t.admin.messages} searchParams={searchParams} />

      <TicketsAdminTabs
        eventSlug={event.slug}
        active={active}
        translations={translations}
        searchParams={searchParams}
      />

      {children}
    </ViewContainer>
  );
}
