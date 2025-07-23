import { ReactNode } from "react";
import Messages from "../errors/Messages";
import InvolvementAdminTabs, {
  InvolvementAdminTabsProps,
} from "./InvolvementAdminTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import type { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  event: {
    name: string;
    slug: string;
  };
  actions?: ReactNode;
  active: InvolvementAdminTabsProps["active"];
  searchParams: Record<string, string>;
  children?: ReactNode;
}

export default async function InvolvementAdminView({
  translations,
  event,
  actions,
  active,
  children,
  searchParams,
}: Props) {
  const t = translations.Involvement;

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.adminTitle}
          <ViewHeading.Sub>{t.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>{actions}</ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <Messages
        messages={translations.Involvement.messages}
        searchParams={searchParams}
      />

      <InvolvementAdminTabs
        eventSlug={event.slug}
        translations={translations}
        active={active}
        searchParams={searchParams}
      />
      {children}
    </ViewContainer>
  );
}
