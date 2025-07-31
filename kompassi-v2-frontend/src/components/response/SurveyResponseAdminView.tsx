import { ReactNode } from "react";
import Messages from "../errors/Messages";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
import type { Translations } from "@/translations/en";
import Link from "next/link";

interface Props {
  translations: Translations;
  event: {
    name: string;
    slug: string;
  };
  survey: {
    slug: string;
    title?: string | null; // ugh
  };
  alerts?: ReactNode;
  actions?: ReactNode;
  searchParams: Record<string, string>;
  children?: ReactNode;
}

export default async function SurveyResponseAdminView({
  translations,
  event,
  survey,
  alerts,
  actions,
  children,
  searchParams,
}: Props) {
  const t = translations.Survey;

  return (
    <ViewContainer>
      <Link
        className="link-subtle"
        href={`/${event.slug}/surveys/${survey.slug}/responses`}
      >
        &lt; {t.actions.returnToResponseList}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.responseListTitle}
          <ViewHeading.Sub>{survey.title}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>{actions}</ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      {alerts}
      <Messages
        messages={translations.Survey.messages}
        searchParams={searchParams}
      />

      {children}
    </ViewContainer>
  );
}
