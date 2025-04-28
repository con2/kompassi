import Link from "next/link";
import { ReactNode } from "react";
import Card from "react-bootstrap/Card";
import CardBody from "react-bootstrap/CardBody";
import SurveyEditorTabs from "../../../surveys/[surveySlug]/edit/SurveyEditorTabs";
import { deleteProgramForm } from "./actions";
import { Survey } from "./models";
import ModalButton from "@/components/ModalButton";
import ProgramAdminView from "@/components/program/ProgramAdminView";
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
  survey: Survey;
  activeTab: string;
  children: ReactNode;
}

/// TODO could this / should this be a layout?
export default function ProgramFormEditorView({
  translations,
  event,
  survey,
  activeTab,
  children,
}: Props) {
  const t = translations.Program.ProgramForm;

  return (
    <ViewContainer>
      <Link className="link-subtle" href={`/${event.slug}/program-forms`}>
        &lt; {t.actions.returnToProgramFormList(event.name)}
      </Link>

      <ViewHeadingActionsWrapper>
        <ViewHeading>
          {survey.title || survey.slug}
          <ViewHeading.Sub>{t.programFormForEvent(event.name)}</ViewHeading.Sub>
        </ViewHeading>
        <ViewHeadingActions>
          <ModalButton
            title={t.actions.deleteProgramForm.title}
            messages={t.actions.deleteProgramForm.modalActions}
            className="btn btn-outline-danger"
            submitButtonVariant="danger"
            action={deleteProgramForm.bind(null, event.slug, survey.slug)}
            disabled={!survey.canRemove}
            // TODO disabledMessage={t.actions.deleteSurvey.cannotRemove}
          >
            {t.actions.deleteProgramForm.confirmation(
              survey.title || survey.slug,
            )}
          </ModalButton>
        </ViewHeadingActions>
      </ViewHeadingActionsWrapper>
      <SurveyEditorTabs
        eventSlug={event.slug}
        survey={survey}
        translations={translations}
        active={activeTab}
        mode="program-forms"
      />
      <Card className="mb-2">
        <CardBody>{children}</CardBody>
      </Card>
    </ViewContainer>
  );
}
