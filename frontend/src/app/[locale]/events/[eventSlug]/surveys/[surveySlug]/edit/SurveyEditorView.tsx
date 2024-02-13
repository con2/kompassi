import Link from "next/link";

import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { Survey } from "./models";
import SurveyEditorTabs from "./SurveyEditorTabs";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading from "@/components/ViewHeading";
import { getTranslations } from "@/translations";

interface Props {
  params: {
    locale: string; // UI language
    eventSlug: string;
    surveySlug: string;
  };

  survey: Survey;
  activeTab: string;
  children: ReactNode;
}

export default function SurveyEditorView({
  params,
  survey,
  activeTab,
  children,
}: Props) {
  const { locale, eventSlug } = params;
  const translations = getTranslations(locale);
  const t = translations.Survey;

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/events/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>

      <ViewHeading>
        {t.editSurveyPage.title}
        <ViewHeading.Sub>{survey.title || survey.slug}</ViewHeading.Sub>
      </ViewHeading>

      <SurveyEditorTabs
        eventSlug={eventSlug}
        survey={survey}
        translations={translations}
        active={activeTab}
      />
      <Card className="mb-2">
        <CardBody>{children}</CardBody>
      </Card>
    </ViewContainer>
  );
}
