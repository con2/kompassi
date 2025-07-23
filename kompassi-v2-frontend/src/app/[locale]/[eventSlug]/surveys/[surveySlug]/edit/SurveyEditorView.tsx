import Link from "next/link";

import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import { deleteSurvey } from "./actions";
import { Survey } from "./models";
import SurveyEditorTabs from "./SurveyEditorTabs";
import ModalButton from "@/components/ModalButton";
import ViewContainer from "@/components/ViewContainer";
import ViewHeading, {
  ViewHeadingActions,
  ViewHeadingActionsWrapper,
} from "@/components/ViewHeading";
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

/// TODO could this / should this be a layout?
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
      <Link className="link-subtle" href={`/${eventSlug}/surveys`}>
        &lt; {t.actions.returnToSurveyList}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {t.editSurveyPage.title}
          <ViewHeading.Sub>{survey.title || survey.slug}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.deleteSurvey.title}
            messages={t.actions.deleteSurvey.modalActions}
            className="btn btn-outline-danger"
            submitButtonVariant="danger"
            action={deleteSurvey.bind(null, eventSlug, survey.slug)}
            disabled={!survey.canRemove}
            // TODO disabledMessage={t.actions.deleteSurvey.cannotRemove}
          >
            {t.actions.deleteSurvey.confirmation(survey.title || survey.slug)}
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>

      <SurveyEditorTabs
        eventSlug={eventSlug}
        survey={survey}
        translations={translations}
        active={activeTab}
        mode="surveys"
      />
      <Card className="mb-2">
        <CardBody>{children}</CardBody>
      </Card>
    </ViewContainer>
  );
}
