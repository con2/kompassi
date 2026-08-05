import {
  Messages,
  ViewContainer,
  ViewHeading,
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@con2/components";
import { ReactNode } from "react";
import ProgramAdminTabs, {
  ProgramAdminTabsProps,
} from "@/components/program/ProgramAdminTabs";
import type { Translations } from "@/translations/en";

interface Props {
  translations: Translations;
  event: {
    name: string;
    slug: string;
  };
  alerts?: ReactNode;
  actions?: ReactNode;
  active: ProgramAdminTabsProps["active"];
  searchParams: Record<string, string>;
  children?: ReactNode;
}

export default async function ProgramAdminView({
  translations,
  event,
  alerts,
  actions,
  active,
  children,
  searchParams,
}: Props) {
  const surveyT = translations.Survey;

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Program.admin.title}
          <ViewHeading.Sub>{surveyT.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>{actions}</ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      {alerts}
      <Messages
        messages={translations.Program.messages}
        searchParams={searchParams}
      />

      <ProgramAdminTabs
        eventSlug={event.slug}
        translations={translations}
        active={active}
        searchParams={searchParams}
      />
      {children}
    </ViewContainer>
  );
}
