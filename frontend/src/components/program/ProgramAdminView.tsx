import { ReactNode } from "react";
import ProgramAdminTabs, {
  ProgramAdminTabsProps,
} from "@/components/program/ProgramAdminTabs";
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
  active: ProgramAdminTabsProps["active"];
  children?: ReactNode;
  queryString: string;
}

export default async function ProgramAdminView({
  translations,
  event,
  actions,
  active,
  children,
  queryString,
}: Props) {
  const surveyT = translations.Survey;
  const t = translations.Program.ProgramForm;

  return (
    <ViewContainer>
      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {translations.Program.admin.title}
          <ViewHeading.Sub>{surveyT.forEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>{actions}</ViewHeadingActions>
      </ViewHeadingActionsWrapper>
      <ProgramAdminTabs
        eventSlug={event.slug}
        translations={translations}
        active={active}
        queryString={queryString}
      />
      {children}
    </ViewContainer>
  );
}
